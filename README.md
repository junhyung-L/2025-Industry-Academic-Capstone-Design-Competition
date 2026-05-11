# 🎓 2025 Industry-Academic Capstone Design Competition

## 📌 Project: Incheon e-Eum Local Currency Data Analysis & Prediction

This repository contains the project files for the 2025 Industry-Academic Capstone Design Competition. The project focuses on analyzing the usage data of "Incheon e-Eum" (local currency in Incheon, South Korea), predicting spending patterns, and conducting ROI analysis to evaluate and optimize the effect of cashback policies.

### 👥 Team
- **산경만지회**

### 🎯 Project Vision
To analyze the impact of local currency policies (specifically cashback rates) on consumer spending behavior and provide data-driven insights for policy optimization using machine learning.

### 🛠️ Key Implementation

#### 1. Data Pipeline & Feature Engineering
- **Data Concatenation**: Merging multi-source datasets (transaction data, population distribution, store counts).
- **Advanced Feature Engineering**: 
  - Application of **Low-Pass Filter (LPF)** to extract clean spending trends.
  - Calculation of trend slopes, deviations, and seasonality (cyclical sin/cos features).
  - Analysis of cashback rate change points and their maintenance duration.

#### 2. Machine Learning Prediction
- **Model**: `CatBoostRegressor`
- **Approach**: Region-specific modeling to predict total spending amounts based on policy variables and historical trends.
- **Evaluation**: Achieved low MAPE on validation sets across various regions.

#### 3. Policy & ROI Analysis
- Analysis of Return on Investment (ROI) for different cashback scenarios.
- Clustering analysis to group regions with similar spending behaviors.

---

### 📂 Repository Structure

```text
├── notebooks/                   # Jupyter Notebooks (Sequential Pipeline)
│   ├── 01_data_concatenation.ipynb
│   ├── 02_data_preprocessing.ipynb
│   ├── 03_feature_engineering.ipynb
│   ├── 04_eda.ipynb
│   ├── 05_prediction.ipynb
│   ├── 06_roi_analysis.ipynb
│   ├── 06_roi_analysis_v2.ipynb
│   ├── 07_clustering.ipynb
│   └── 08_visualization.ipynb
│
├── src/                         # Structured Python Modules (Derived from Notebooks)
│   ├── data_preprocessing.py    # Data cleaning and type conversion
│   ├── feature_engineering.py   # LPF, trend, and prediction features
│   └── model_training.py        # CatBoost training pipeline
│
└── reports/                     # Competition Reports
    ├── 2025년 산학 캡스톤디자인 발표자료_산경만지회.pdf
    └── 2025년 산학 캡스톤디자인 최종 결과보고서_산경만지회.pdf
```

---
*This repository has been structured and refined for the professional [Data Analyst Portfolio](https://github.com/junhyung-L).*
