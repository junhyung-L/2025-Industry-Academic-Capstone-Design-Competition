"""CLI for reproducible e-Eum regional spending-model holdout runs."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

from src.config import DATA_DIR, result_path
from src.model_training import train_and_evaluate_by_region


def read_csv(path: Path) -> pd.DataFrame:
    for encoding in ("utf-8-sig", "cp949", "utf-8"):
        try:
            return pd.read_csv(path, encoding=encoding)
        except UnicodeDecodeError:
            continue
    raise ValueError(f"Unable to decode CSV: {path}")


def add_time_features(data: pd.DataFrame, region_col: str, date_col: str, target_col: str) -> pd.DataFrame:
    frame = data.copy()
    frame[date_col] = pd.to_datetime(frame[date_col], errors="coerce")
    frame[target_col] = pd.to_numeric(frame[target_col].astype(str).str.replace(",", ""), errors="coerce")
    frame = frame.dropna(subset=[region_col, date_col, target_col]).sort_values([region_col, date_col])
    frame["month"] = frame[date_col].dt.month
    frame["month_sin"] = np.sin(2 * np.pi * frame["month"] / 12)
    frame["month_cos"] = np.cos(2 * np.pi * frame["month"] / 12)
    grouped = frame.groupby(region_col)[target_col]
    frame["lag_1"] = grouped.shift(1)
    frame["lag_3"] = grouped.shift(3)
    frame["rolling_mean_3"] = grouped.transform(lambda series: series.shift(1).rolling(3, min_periods=1).mean())
    return frame.dropna(subset=["lag_1"])


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Train chronological regional e-Eum spending models.")
    parser.add_argument("--input-csv", type=Path, required=True, help="Merged source CSV; data is not included in this repository.")
    parser.add_argument("--region-col", required=True)
    parser.add_argument("--date-col", required=True)
    parser.add_argument("--target-col", required=True)
    parser.add_argument("--models-dir", type=Path, default=result_path("models"))
    parser.add_argument("--metrics-csv", type=Path, default=result_path("regional_metrics.csv"))
    parser.add_argument("--features-csv", type=Path, default=result_path("model_features.csv"))
    return parser


def main(args: argparse.Namespace) -> None:
    if not args.input_csv.is_file():
        raise FileNotFoundError(f"Input CSV not found: {args.input_csv}. Place it under {DATA_DIR} or pass its path explicitly.")
    raw = read_csv(args.input_csv)
    required = {args.region_col, args.date_col, args.target_col}
    missing = required.difference(raw.columns)
    if missing:
        raise KeyError(f"Input CSV is missing required columns: {sorted(missing)}")
    features = add_time_features(raw, args.region_col, args.date_col, args.target_col)
    metrics = train_and_evaluate_by_region(features, region_col=args.region_col, date_col=args.date_col, target_col=args.target_col, output_model_dir=args.models_dir)
    for path, frame in ((args.features_csv, features), (args.metrics_csv, metrics)):
        path.parent.mkdir(parents=True, exist_ok=True)
        frame.to_csv(path, index=False, encoding="utf-8-sig")
    print(f"Saved features: {args.features_csv}")
    print(f"Saved metrics: {args.metrics_csv}")


if __name__ == "__main__":
    parser = build_parser()
    try:
        main(parser.parse_args())
    except (FileNotFoundError, KeyError, ImportError, ValueError) as exc:
        parser.error(str(exc))
