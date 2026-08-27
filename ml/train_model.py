"""Train and evaluate the experimental XGBoost regression model offline."""

import json
from pathlib import Path

import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor

from ml.simulate_data import RANDOM_STATE


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "simulated_academic_data.csv"
MODEL_PATH = ROOT / "models" / "xgb_performance_model.json"
METADATA_PATH = ROOT / "models" / "xgb_model_metadata.json"
REPORT_PATH = ROOT / "reports" / "xgb_evaluation.json"
FEATURES = ["difficulty", "importance", "performance", "study_hours"]
TARGET = "academic_performance_score"

MODEL_CONFIG = {
    "objective": "reg:squarederror",
    "n_estimators": 300,
    "max_depth": 4,
    "learning_rate": 0.05,
    "subsample": 0.8,
    "colsample_bytree": 0.8,
    "random_state": RANDOM_STATE,
}


def train_and_evaluate() -> dict:
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found at {DATA_PATH}. Run: python -m ml.simulate_data"
        )

    dataset = pd.read_csv(DATA_PATH)
    required_columns = set(FEATURES + [TARGET, "data_source"])
    missing = required_columns.difference(dataset.columns)
    if missing:
        raise ValueError(f"Dataset is missing columns: {sorted(missing)}")
    if set(dataset["data_source"].dropna().unique()) != {"simulated"}:
        raise ValueError("Training dataset must be explicitly labelled simulated.")

    X = dataset[FEATURES]
    y = dataset[TARGET].clip(0, 100)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_STATE
    )

    model = XGBRegressor(**MODEL_CONFIG)
    model.fit(X_train, y_train)
    predictions = model.predict(X_test).clip(0, 100)
    metrics = {
        "MAE": round(float(mean_absolute_error(y_test, predictions)), 4),
        "RMSE": round(float(mean_squared_error(y_test, predictions) ** 0.5), 4),
        "R2": round(float(r2_score(y_test, predictions)), 4),
    }

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    model.save_model(MODEL_PATH)

    metadata = {
        "feature_order": FEATURES,
        "target": TARGET,
        "random_state": RANDOM_STATE,
        "dataset_source": "simulated",
        "target_bounds": [0, 100],
        "train_test_split": {"test_size": 0.2, "random_state": RANDOM_STATE},
        "model_config": MODEL_CONFIG,
        "xgboost_version": __import__("xgboost").__version__,
        "sklearn_version": __import__("sklearn").__version__,
        "pandas_version": pd.__version__,
    }
    METADATA_PATH.write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    REPORT_PATH.write_text(
        json.dumps(
            {
                "metrics": metrics,
                "dataset_source": "simulated",
                "rows": len(dataset),
                "train_rows": len(X_train),
                "test_rows": len(X_test),
                "random_state": RANDOM_STATE,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    return metrics


if __name__ == "__main__":
    print(json.dumps(train_and_evaluate(), indent=2))
