"""Cached inference helper for the offline-trained XGBoost model."""

from functools import lru_cache
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / "models" / "xgb_performance_model.json"
FEATURE_ORDER = ["difficulty", "importance", "performance", "study_hours"]


@lru_cache(maxsize=1)
def get_model():
    """Load the model once per Flask process; never train during a request."""
    from xgboost import XGBRegressor

    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            "The XGBoost model is unavailable. Run: python -m ml.train_model"
        )
    model = XGBRegressor()
    model.load_model(MODEL_PATH)
    return model


def predict_performance(subjects: list[dict]) -> list[float]:
    """Predict bounded scores using each subject's optimized study hours."""
    import numpy as np
    import pandas as pd

    features = pd.DataFrame(
        [
            {
                "difficulty": subject["difficulty"],
                "importance": subject["importance"],
                "performance": subject["performance"],
                "study_hours": subject["optimized_hours"],
            }
            for subject in subjects
        ],
        columns=FEATURE_ORDER,
    )
    predictions = get_model().predict(features)
    return [round(float(np.clip(prediction, 0, 100)), 2) for prediction in predictions]
