# Incheon e-Eum Cashback Policy Simulation: Comparing 66 Budget-Constrained Policies

[English](PORTFOLIO.md) | [한국어](PORTFOLIO.ko.md)

## Overview

This Gold Prize capstone project forecasts regional e-Eum card spending and
compares cashback policies when only two months can receive an increase under
a KRW 200 billion annual budget.

## Approach

Regional spending is combined with demographic, category-spending, interest
rate, CSI, policy, charging, and payment variables. LPF separates short-term
noise; calendar features represent seasonality. Hurst values of 0.79–0.86
support the presence of persistent regional time-series patterns.

Separate LightGBM models represent 5% and 10% cashback conditions. The report
uses 2020–2023 data with an 80/20 train/test split, then evaluates all
C(12,2)=66 choices for the two higher-cashback months.

## Results

The report describes MAPE mostly in the 10–15% range, with important regional
exceptions such as 44.26% for Yeonsu-gu under one 10% condition. ROI compares
predicted consumption uplift with cashback spending and remaining budget.

## Limitations

This is an observational simulation, not causal policy evidence. Complete
versioned inputs and a counterfactual design are needed before policy use.

## Evidence

- Final report in `reports/`
- [`docs/PROJECT_REVIEW.md`](docs/PROJECT_REVIEW.md)

## Why this is a scenario tool rather than an average policy effect

Cashback may not behave identically by district or month. The report therefore keeps separate LightGBM models for 5% and 10% conditions instead of treating rate as one simple linear input. LPF, seasonal sin/cos features, holidays, demographics, category spend, and macro indicators describe the surrounding context rather than presume a uniform response.

Hurst values of 0.79–0.86 are supporting evidence of persistent consumption patterns, not evidence that cashback caused them. Forecast error also varies: many segments fall near 10–15% MAPE, while Yeonsu under the 10% condition reaches 44.26%. The 66 ranked combinations are consequently candidate policies under explicit assumptions, not a proven optimum.

Each scenario compares expected consumption increase, cashback outlay, and budget left over. This avoids choosing only the month with the highest predicted spend. The report’s holiday-focused and district-differentiated suggestions are policy hypotheses from this comparison, not measured causal effects after a real policy change.
