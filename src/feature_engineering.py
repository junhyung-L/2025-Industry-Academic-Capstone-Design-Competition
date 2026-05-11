import pandas as pd
import numpy as np
from scipy.signal import butter, filtfilt

def apply_lpf(series, cutoff=0.05):
    """
    Apply Low-Pass Filter to a series to extract trend.
    """
    b, a = butter(N=2, Wn=cutoff, btype='low')
    return filtfilt(b, a, series.ffill())

def create_trend_features(df, target_col="업종별_인천e음카드_데이터(월별)_전체금액"):
    """
    Create trend features using LPF and rolling windows.
    """
    if target_col not in df.columns:
        print(f"Warning: {target_col} not found in DataFrame. Skipping trend features.")
        return df
        
    trend_features = []
    
    for region, sub_df in df.groupby("지역"):
        temp = sub_df.copy()
        
        # (1) LPF based trend
        temp["lpf_trend"] = apply_lpf(temp[target_col])
        
        # (2) Monthly trend diff
        temp["trend_diff"] = temp["lpf_trend"].diff()
        
        # (3) 3-month slope
        temp["slope_3"] = temp["lpf_trend"].rolling(3).apply(
            lambda x: np.polyfit(range(3), x, 1)[0] if not x.isnull().any() else np.nan,
            raw=False
        )
        
        # (4) 6-month slope
        temp["slope_6"] = temp["lpf_trend"].rolling(6).apply(
            lambda x: np.polyfit(range(6), x, 1)[0] if not x.isnull().any() else np.nan,
            raw=False
        )
        
        # (5) Deviation from trend
        temp["trend_deviation"] = temp[target_col] - temp["lpf_trend"]
        
        trend_features.append(temp)
        
    return pd.concat(trend_features, ignore_index=True)

def create_seasonality_features(df, date_col="일자"):
    """
    Create cyclical seasonality features (sin/cos of month).
    """
    df = df.copy()
    if date_col in df.columns:
        df[date_col] = pd.to_datetime(df[date_col])
        df["month"] = df[date_col].dt.month
        df["month_sin"] = np.sin(2 * np.pi * df["month"] / 12)
        df["month_cos"] = np.cos(2 * np.pi * df["month"] / 12)
        
        # Also add the classification of year period
        def classify_year_period(month):
            if month <= 3:
                return "Y_E"  # Early year
            elif month <= 9:
                return "Y_M"  # Mid year
            else:
                return "Y_T"  # Year end
        
        df["연초말_EMT"] = df["month"].apply(classify_year_period)
        
    return df

def create_cashback_features(df, cashback_col='인천e음카드_월별_캐시백비율_연매출 3억~30억원'):
    """
    Analyze cashback effect on spending.
    """
    df = df.copy()
    if cashback_col not in df.columns:
        print(f"Warning: {cashback_col} not found. Skipping cashback features.")
        return df
        
    df['일자'] = pd.to_datetime(df['일자'])
    df = df.sort_values(by=['지역', '일자'])
    
    # Calculate diff in cashback
    df['캐시백_변화'] = df.groupby('지역')[cashback_col].diff()
    
    def get_change_direction(x):
        if pd.isna(x):
            return 0
        elif x > 0:
            return 1   # Increase
        elif x < 0:
            return -1  # Decrease
        else:
            return 0   # No change
            
    df['캐시백_상하향_더미'] = df['캐시백_변화'].apply(get_change_direction)
    
    # Extract change points
    change_points = df[df['캐시백_상하향_더미'] != 0].copy()
    change_points["캐시백_유지개월"] = 0
    
    # Calculate how many months the new rate was maintained
    for idx, row in change_points.iterrows():
        region = row['지역']
        base_date = row['일자']
        base_rate = row[cashback_col]
        
        after_df = df[(df['지역'] == region) & (df['일자'] > base_date)].copy()
        
        maintain_months = 0
        for _, r in after_df.iterrows():
            if r[cashback_col] == base_rate:
                maintain_months += 1
            else:
                break
                
        change_points.at[idx, "캐시백_유지개월"] = maintain_months
        
    # Merge back
    df = pd.merge(
        df,
        change_points[["지역", "일자", "캐시백_유지개월"]],
        on=["지역", "일자"],
        how="left"
    )
    
    return df

def create_spending_change_rate(df, target_col="업종별_인천e음카드_데이터(월별)_전체금액"):
    """
    Create MoM change rate and deviation from 3-month moving average.
    """
    df = df.copy()
    if target_col not in df.columns:
        return df
        
    df["전월대비_변화율"] = df.groupby("지역")[target_col].pct_change()
    df["금액_ma_3"] = df.groupby("지역")[target_col].transform(lambda x: x.rolling(3, min_periods=1).mean())
    df["금액_deviation_3"] = df[target_col] - df["금액_ma_3"]
    
    return df

def create_prediction_features(df, target_col="전체금액", date_col="일자"):
    """
    Create features specific for prediction (rolling windows, lags, time features).
    This logic is extracted from 05_prediction.ipynb.
    """
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col])
    df = df.sort_values(by=['지역', date_col])
    
    processed_dfs = []
    for region, data in df.groupby('지역'):
        temp = data.copy()
        
        # Rolling features
        temp['ma_7'] = temp[target_col].rolling(window=7, min_periods=1).mean()
        # Note: Original code used window=15 for 'ma_30' and window=30 for 'ma_90'
        # Preserving this behavior but adding comments
        temp['ma_30'] = temp[target_col].rolling(window=15, min_periods=1).mean() 
        temp['ma_90'] = temp[target_col].rolling(window=30, min_periods=1).mean()
        temp['std_7'] = temp[target_col].rolling(window=7, min_periods=1).std()
        temp['range_7'] = temp[target_col].rolling(window=7).max() - temp[target_col].rolling(window=7).min()
        
        # Lag features
        temp['lag_1'] = temp[target_col].shift(1)
        temp['lag_3'] = temp[target_col].shift(3)
        temp['lag_30'] = temp[target_col].shift(30)
        
        # Change rate
        temp['change_rate'] = temp[target_col].pct_change().fillna(0)
        
        # Time features
        temp['month'] = temp[date_col].dt.month
        temp['day_of_week'] = temp[date_col].dt.dayofweek
        temp['is_weekend'] = temp['day_of_week'].isin([5, 6]).astype(int)
        
        processed_dfs.append(temp)
        
    return pd.concat(processed_dfs, ignore_index=True).fillna(0)

if __name__ == "__main__":
    print("Feature engineering module loaded.")
