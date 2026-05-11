import pandas as pd
import numpy as np
from catboost import CatBoostRegressor, Pool
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib

def train_and_evaluate_by_region(df, target_col="전체금액", date_col="일자", output_model_dir=None):
    """
    Train a CatBoost model for each region and evaluate performance.
    Logic extracted from 05_prediction.ipynb.
    """
    # Ensure date column is datetime
    df[date_col] = pd.to_datetime(df[date_col])
    
    regions = df['지역'].unique()
    trained_models = {}
    
    for region in regions:
        data = df[df['지역'] == region].copy()
        data = data.sort_values(date_col)
        
        # Features are all columns except target and metadata
        exclude_cols = [target_col, '지역', 'value_combination', 'lpf_trend', '금액_deviation_30', '평년_월별_차이', date_col]
        features = [col for col in data.columns if col not in exclude_cols]
        
        # Categorical features
        categorical_features = [col for col in data.select_dtypes(include='object').columns if col in features]
        
        if len(data) < 10 or data[target_col].nunique() <= 1:
            print(f"[{region}] ❌ Skipping due to insufficient data.")
            continue
            
        # Data split (80% train, 20% valid)
        split_idx = int(len(data) * 0.8)
        X_train, X_valid = data[features].iloc[:split_idx], data[features].iloc[split_idx:]
        y_train, y_valid = data[target_col].iloc[:split_idx], data[target_col].iloc[split_idx:]
        
        print(f"[{region}] Training with {len(X_train)} samples, validating with {len(X_valid)} samples...")
        
        train_pool = Pool(X_train, y_train, cat_features=categorical_features)
        valid_pool = Pool(X_valid, y_valid, cat_features=categorical_features)
        
        model = CatBoostRegressor(
            iterations=1000,
            learning_rate=0.03,
            depth=6,
            loss_function='RMSE',
            eval_metric='RMSE',
            random_seed=42,
            early_stopping_rounds=50,
            verbose=100
        )
        
        model.fit(train_pool, eval_set=valid_pool)
        trained_models[region] = model
        
        # Predict and evaluate
        y_pred = model.predict(X_valid)
        rmse = np.sqrt(mean_squared_error(y_valid, y_pred))
        
        # Calculate MAPE (handling zero division)
        non_zero_idx = y_valid != 0
        if non_zero_idx.sum() > 0:
            mape = np.mean(np.abs((y_valid[non_zero_idx] - y_pred[non_zero_idx]) / y_valid[non_zero_idx])) * 100
        else:
            mape = np.nan
            
        print(f"[{region}] ✅ Validation RMSE: {rmse:.2f}, MAPE: {mape:.2f}%")
        
        # Save model if directory provided
        if output_model_dir:
            import os
            os.makedirs(output_model_dir, exist_ok=True)
            model.save_model(os.path.join(output_model_dir, f"catboost_{region}.cbm"))
            
    return trained_models

def plot_predictions(y_true, y_pred, dates, title="Actual vs Predicted"):
    """
    Helper function to plot predictions.
    """
    plt.figure(figsize=(10, 6))
    plt.plot(dates, y_true, label='Actual', marker='o')
    plt.plot(dates, y_pred, label='Predicted', marker='x')
    plt.title(title)
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    print("Model training module loaded.")
