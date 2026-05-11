import pandas as pd
import numpy as np

def preprocess_card_data(file_path, output_path=None):
    """
    Preprocess the Incheon e-Eum card usage data.
    
    Parameters:
    - file_path: str, path to the raw CSV file.
    - output_path: str, path to save the preprocessed CSV file (optional).
    
    Returns:
    - df: pandas.DataFrame, preprocessed dataframe.
    """
    print(f"Loading data from {file_path}...")
    # The notebook uses cp949 or utf-8-sig depending on the file. 
    # We'll try utf-8-sig first as it's more standard for Korean CSVs saved from Excel,
    # but fallback to cp949 if needed.
    try:
        df = pd.read_csv(file_path, encoding='utf-8-sig')
    except UnicodeDecodeError:
        df = pd.read_csv(file_path, encoding='cp949')
    
    # List of columns to convert to numeric
    numeric_cols = [
        "문화_취미_영화관", "숙박", "약국", "연료",
        "유통업영리_편의점", "일반휴게음식", "학원", "기타", "전체금액"
    ]
    
    # Convert to numeric after removing commas
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', ''), errors='coerce')
            
    # Clean region column
    if "지역" in df.columns:
        df["지역"] = df["지역"].astype(str).str.strip()
        # Filter out ETC and 기타 as done in the notebook
        df = df[~df["지역"].isin(["ETC", "기타"])].copy()
        
    # Convert date column
    if "일자" in df.columns:
        df["일자"] = pd.to_datetime(df["일자"], errors="coerce")
        df = df.dropna(subset=["일자"])
        
    # Fill missing total amount by summing other categories
    calc_cols = [col for col in numeric_cols if col != "전체금액"]
    available_calc_cols = [col for col in calc_cols if col in df.columns]
    
    if "전체금액" in df.columns and available_calc_cols:
        df["전체금액"] = df["전체금액"].fillna(df[available_calc_cols].sum(axis=1))
    
    # Fill remaining NaN with 0 in numeric columns
    for col in numeric_cols:
        if col in df.columns:
            df[col] = df[col].fillna(0)
            
    if output_path:
        df.to_csv(output_path, index=False, encoding='utf-8-sig')
        print(f"Saved preprocessed data to {output_path}")
        
    return df

if __name__ == "__main__":
    # This block allows running the script standalone for testing
    import sys
    if len(sys.argv) > 2:
        preprocess_card_data(sys.argv[1], sys.argv[2])
    elif len(sys.argv) > 1:
        preprocess_card_data(sys.argv[1])
    else:
        print("Usage: python data_preprocessing.py <input_file> [<output_file>]")
