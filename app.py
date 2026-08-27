import math

from flask import Flask, render_template, request
from pulp import LpMaximize, LpProblem, LpStatus, LpVariable, PULP_CBC_CMD, lpSum, value
from pulp.apis.core import PulpSolverError

from ml.predict import predict_performance

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


def render_input_error(message):
    """Return the input form with a user-safe validation error."""
    return render_template("index.html", error=message), 400


@app.route("/submit", methods=["POST"])
def submit():

    # Student information
    student_name = request.form.get("student_name")
    study_hours = request.form.get("study_hours")
    exam_days = request.form.get("exam_days")

    try:
        available_study_hours = float(study_hours)
    except (TypeError, ValueError):
        return render_input_error(
            "Available study hours must be a valid positive number."
        )

    if not math.isfinite(available_study_hours) or available_study_hours <= 0:
        return render_input_error(
            "Available study hours must be a finite number greater than 0."
        )


    # Subject information
    subject_names = request.form.getlist("subject_name[]")

    difficulties = request.form.getlist("difficulty[]")

    importances = request.form.getlist("importance[]")

    performances = request.form.getlist("performance[]")

    min_hours = request.form.getlist("min_hours[]")

    max_hours = request.form.getlist("max_hours[]")


    subject_fields = {
        "subject names": subject_names,
        "difficulties": difficulties,
        "importances": importances,
        "performances": performances,
        "minimum study hours": min_hours,
        "maximum study hours": max_hours,
    }

    # Reject incomplete or deliberately malformed repeated form fields before
    # indexing them. This keeps invalid submissions from raising IndexError.
    if not subject_names:
        return render_input_error(
            "Please provide complete details for all five subjects."
        )

    expected_count = len(subject_names)
    if expected_count != 5:
        return render_input_error(
            "Exactly five complete subjects are required for this study-time optimizer."
        )

    if any(len(values) != expected_count for values in subject_fields.values()):
        return render_input_error(
            "Incomplete subject data was submitted. Please complete every subject field."
        )

    # Convert, validate, and combine subject data.
    subjects = []

    for i in range(expected_count):
        try:
            difficulty = int(difficulties[i])
            importance = int(importances[i])
            performance = int(performances[i])
            minimum_hours = float(min_hours[i])
            maximum_hours = float(max_hours[i])
        except (TypeError, ValueError):
            return render_input_error(
                f"Subject {i + 1} has invalid numeric input. Please use valid numbers."
            )

        if not subject_names[i].strip():
            return render_input_error(f"Subject {i + 1} must have a name.")

        if not all(1 <= value <= 5 for value in (difficulty, importance, performance)):
            return render_input_error(
                f"Subject {i + 1}: difficulty, importance, and performance "
                "must each be between 1 and 5."
            )

        if (
            not math.isfinite(minimum_hours)
            or not math.isfinite(maximum_hours)
            or minimum_hours < 0
            or maximum_hours <= 0
            or minimum_hours > maximum_hours
        ):
            return render_input_error(
                f"Subject {i + 1}: minimum hours must be at least 0, maximum "
                "hours must be greater than 0, and minimum hours cannot exceed maximum hours."
            )

        performance_gap = 6 - performance
        spi = round(
            (0.40 * difficulty)
            + (0.35 * importance)
            + (0.25 * performance_gap),
            2,
        )

        subject = {
            "name": subject_names[i],
            "difficulty": difficulty,
            "importance": importance,
            "performance": performance,
            "min_hours": minimum_hours,
            "max_hours": maximum_hours,
            "performance_gap": performance_gap,
            "spi": spi,
        }

        subjects.append(subject)

    total_minimum_hours = sum(subject["min_hours"] for subject in subjects)
    if total_minimum_hours > available_study_hours:
        return render_input_error(
            "Available study hours are insufficient to satisfy the combined minimum "
            f"requirement of {total_minimum_hours:.2f} hours."
        )

    # Maximize the total SPI-weighted daily study allocation within each
    # subject's bounds and the student's available daily study time.
    optimization_model = LpProblem("Study_Time_Allocation", LpMaximize)
    study_variables = [
        LpVariable(
            f"study_hours_{index + 1}",
            lowBound=subject["min_hours"],
            upBound=subject["max_hours"],
            cat="Continuous",
        )
        for index, subject in enumerate(subjects)
    ]

    optimization_model += lpSum(
        subject["spi"] * study_variable
        for subject, study_variable in zip(subjects, study_variables)
    )
    optimization_model += lpSum(study_variables) <= available_study_hours

    try:
        optimization_model.solve(PULP_CBC_CMD(msg=False))
    except (PulpSolverError, OSError) as error:
        return render_input_error(
            "The optimization solver could not complete the allocation. "
            f"Please try again. ({error})"
        )

    solver_status = LpStatus.get(optimization_model.status, "Unknown")
    if solver_status != "Optimal":
        return render_input_error(
            "The optimization model did not find an optimal allocation "
            f"(solver status: {solver_status})."
        )

    for subject, study_variable in zip(subjects, study_variables):
        optimized_hours = value(study_variable)
        if optimized_hours is None:
            return render_input_error(
                "The optimization solver returned an incomplete allocation."
            )
        subject["optimized_hours"] = round(optimized_hours, 2)

    objective_function_value = value(optimization_model.objective)
    if objective_function_value is None:
        return render_input_error(
            "The optimization solver did not return an objective value."
        )

    total_optimized_hours = round(
        sum(subject["optimized_hours"] for subject in subjects), 2
    )
    objective_function_value = round(objective_function_value, 2)

    # Predictive stage is deliberately sequential: it consumes the LP output
    # but never changes the LP objective or allocation.
    prediction_error = None
    try:
        predictions = predict_performance(subjects)
        for subject, prediction in zip(subjects, predictions):
            subject["predicted_performance"] = prediction
    except Exception as error:  # ML availability must not break LP results.
        prediction_error = "Prediction unavailable for this submission."
        print("XGBoost prediction unavailable:", error)
        for subject in subjects:
            subject["predicted_performance"] = None

    # Presentation-only dashboard data. These values are derived from the
    # completed LP/ML stages and do not feed back into either calculation.
    # Sort only the presentation copy; LP variables, predictions, and their
    # underlying calculations remain exactly as solved above.
    display_subjects = sorted(subjects, key=lambda item: item["spi"], reverse=True)
    ranked_subjects = display_subjects
    spi_ranks = {id(subject): rank for rank, subject in enumerate(ranked_subjects, 1)}
    allocation_explanations = []
    for subject in display_subjects:
        if abs(subject["optimized_hours"] - subject["max_hours"]) < 1e-6:
            allocation_state = "at its maximum allowed allocation"
        elif abs(subject["optimized_hours"] - subject["min_hours"]) < 1e-6:
            allocation_state = "at its minimum required allocation"
        else:
            allocation_state = "between its minimum and maximum bounds"

        allocation_explanations.append(
            {
                "name": subject["name"],
                "spi": subject["spi"],
                "optimized_hours": subject["optimized_hours"],
                "rank": spi_ranks[id(subject)],
                "state": allocation_state,
            }
        )

    dashboard_data = [
        {
            "name": subject["name"],
            "spi": subject["spi"],
            "optimized_hours": subject["optimized_hours"],
            "predicted_performance": subject["predicted_performance"],
        }
        for subject in display_subjects
    ]


    # Print data in terminal
    print("\n========== STUDENT DATA ==========")

    print("Name:", student_name)
    print("Available Study Hours:", available_study_hours)
    print("Days Until Exam:", exam_days)


    print("\n========== SUBJECT DATA ==========")

    for subject in subjects:

        print(subject)

    print("\n========== OPTIMIZATION SUMMARY ==========")
    print("Solver Status:", solver_status)
    print("Total Optimized Study Hours:", total_optimized_hours)
    print("Objective Function Value:", objective_function_value)


    # Return temporary confirmation
    return render_template(
        "results.html",
        student_name=student_name,
        study_hours=available_study_hours,
        exam_days=exam_days,
        subjects=display_subjects,
        solver_status=solver_status,
        total_optimized_hours=total_optimized_hours,
        objective_function_value=objective_function_value,
        prediction_error=prediction_error,
        dashboard_data=dashboard_data,
        allocation_explanations=allocation_explanations,
    )

if __name__ == "__main__":
    app.run(debug=True)
