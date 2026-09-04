"""Fair, reproducible comparison of the project's five regression models."""

import json
import time
from pathlib import Path

import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor

from ml.simulate_data import RANDOM_STATE
from ml.train_model import MODEL_CONFIG


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "simulated_academic_data.csv"
REPORT_PATH = ROOT / "reports" / "model_comparison.json"
FEATURES = ["difficulty", "importance", "performance", "study_hours"]
TARGET = "academic_performance_score"


def model_factories():
    """Return fresh estimators so every model has an independent fit."""
    return {
        "Linear Regression": lambda: LinearRegression(),
        "Decision Tree Regressor": lambda: DecisionTreeRegressor(
            random_state=RANDOM_STATE
        ),
        "Random Forest Regressor": lambda: RandomForestRegressor(
            n_estimators=200, random_state=RANDOM_STATE, n_jobs=1
        ),
        "Gradient Boosting Regressor": lambda: GradientBoostingRegressor(
            random_state=RANDOM_STATE
        ),
        "XGBoost Regressor": lambda: XGBRegressor(**MODEL_CONFIG),
    }


def ranking_key(result):
    """Higher R², then lower RMSE, then lower MAE; failed models rank last."""
    if result.get("status") != "success":
        return (float("inf"), float("inf"), float("inf"))
    return (-result["r2"], result["rmse"], result["mae"])


def compare_models() -> dict:
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found at {DATA_PATH}. Run: python -m ml.simulate_data"
        )

    dataset = pd.read_csv(DATA_PATH)
    required = set(FEATURES + [TARGET, "data_source"])
    missing = required.difference(dataset.columns)
    if missing:
        raise ValueError(f"Dataset is missing columns: {sorted(missing)}")
    if set(dataset["data_source"].dropna().unique()) != {"simulated"}:
        raise ValueError("Comparison requires a dataset labelled simulated.")

    X = dataset[FEATURES]
    y = dataset[TARGET].clip(0, 100)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_STATE
    )

    results = []
    for name, factory in model_factories().items():
        started = time.perf_counter()
        try:
            model = factory()
            model.fit(X_train, y_train)
            predictions = model.predict(X_test)
            results.append(
                {
                    "name": name,
                    "status": "success",
                    "mae": round(float(mean_absolute_error(y_test, predictions)), 6),
                    "rmse": round(
                        float(mean_squared_error(y_test, predictions) ** 0.5), 6
                    ),
                    "r2": round(float(r2_score(y_test, predictions)), 6),
                    "training_time_seconds": round(
                        time.perf_counter() - started, 6
                    ),
                }
            )
        except Exception as error:  # Keep one model failure from hiding others.
            results.append(
                {
                    "name": name,
                    "status": "failed",
                    "error": str(error),
                    "training_time_seconds": round(
                        time.perf_counter() - started, 6
                    ),
                }
            )

    results.sort(key=ranking_key)
    successful = [item for item in results if item["status"] == "success"]
    for rank, result in enumerate(successful, 1):
        result["rank"] = rank
    for result in results:
        result.setdefault("rank", None)

    report = {
        "dataset_source": "simulated",
        "dataset_rows": len(dataset),
        "features": FEATURES,
        "target": TARGET,
        "test_size": 0.2,
        "train_rows": len(X_train),
        "test_rows": len(X_test),
        "random_state": RANDOM_STATE,
        "ranking_method": "Highest R², then lowest RMSE, then lowest MAE",
        "models": results,
        "best_model": successful[0]["name"] if successful else None,
        "best_r2": successful[0]["r2"] if successful else None,
    }
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report


if __name__ == "__main__":
    report = compare_models()
    print(json.dumps(report, indent=2))
