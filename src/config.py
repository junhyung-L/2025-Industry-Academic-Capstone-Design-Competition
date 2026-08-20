"""Portable paths and defaults for the e-Eum forecasting workflow."""

from __future__ import annotations

import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = Path(os.getenv("EEUM_DATA_DIR", PROJECT_ROOT / "data"))
RESULTS_DIR = Path(os.getenv("EEUM_RESULTS_DIR", PROJECT_ROOT / "results"))
RANDOM_SEED = 42
VALIDATION_FRACTION = 0.20


def result_path(filename: str) -> Path:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    return RESULTS_DIR / filename
