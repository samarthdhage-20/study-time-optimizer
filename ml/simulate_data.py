"""Generate the clearly labelled synthetic data used by the prototype model.

The target is intentionally simulated rather than observed academic performance:
score = 35 + 8*performance + 3*importance - 2*difficulty
        + 3*study_hours + Gaussian noise (standard deviation 5), clipped to 0-100.
"""

from pathlib import Path

import numpy as np
import pandas as pd


RANDOM_STATE = 42
N_ROWS = 5000
OUTPUT_PATH = Path(__file__).resolve().parents[1] / "data" / "simulated_academic_data.csv"


def generate_dataset(
    n_rows: int = N_ROWS, random_state: int = RANDOM_STATE
) -> pd.DataFrame:
    """Generate bounded, reproducible subject-level academic observations."""
    rng = np.random.default_rng(random_state)
    performance = rng.integers(1, 6, size=n_rows)
    difficulty = rng.integers(1, 6, size=n_rows)
    importance = rng.integers(1, 6, size=n_rows)
    study_hours = rng.uniform(0, 8, size=n_rows).round(2)
    noise = rng.normal(0, 5, size=n_rows)

    score = (
        35
        + 8 * performance
        + 3 * importance
        - 2 * difficulty
        + 3 * study_hours
        + noise
    )

    return pd.DataFrame(
        {
            "student_id": [f"sim_student_{i // 5 + 1:04d}" for i in range(n_rows)],
            "subject_id": [f"subject_{i % 5 + 1}" for i in range(n_rows)],
            "difficulty": difficulty,
            "importance": importance,
            "performance": performance,
            "study_hours": study_hours,
            "academic_performance_score": np.clip(score, 0, 100).round(2),
            "data_source": "simulated",
        }
    )


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    dataset = generate_dataset()
    dataset.to_csv(OUTPUT_PATH, index=False)
    print(f"Generated {len(dataset)} rows at {OUTPUT_PATH}")
    print("Dataset source: simulated; random seed: 42; target range: 0-100")


if __name__ == "__main__":
    main()
