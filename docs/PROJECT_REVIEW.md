# Project Review

| Area | Assessment | Evidence and caveat |
|---|---:|---|
| Problem framing | 7/10 | The cashback/spending policy question is explicit. |
| Feature engineering | 7/10 | LPF, rolling, lag, seasonality, and cashback-change features are implemented. |
| Modelling | 6/10 | Per-region time-ordered CatBoost validation with early stopping is implemented. |
| Evaluation | 3/10 | One retained actual-versus-predicted chart displays MAPE 5.66% for its shown configuration (`images/05_20.png`), but raw data, a backtest table, and causal counterfactual design are absent. |
| Reproducibility | 3/10 | Modules exist, but paths, dependencies, raw inputs, and an end-to-end runner are incomplete. |

## Priorities

1. Add a schema/fixture and a configuration-driven runner that writes metrics and scenario artifacts.
2. Retain date-based backtests by region and an explicit naive baseline.
3. Separate demand forecasting from causal claims about cashback-policy effects.
