import pandas as pd
import numpy as np
import os

def preprocess_and_feature_engineer(input_path='data/raw_sales_data.csv', output_path='data/processed_sales_data.csv'):
    """
    Cleans the raw data and creates time-series features necessary for forecasting models.
    """
    print("Loading and preprocessing data...")
    try:
        df = pd.read_csv(input_path)
    except FileNotFoundError:
        print(f"Error: Could not find {input_path}")
        return None
        
    # Convert dates
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Sort chronologically
    df = df.sort_values(by=['Product_ID', 'Date']).reset_index(drop=True)
    
    # Feature Engineering
    print("Engineering time-based features...")
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month
    df['DayOfWeek'] = df['Date'].dt.dayofweek
    df['IsWeekend'] = df['DayOfWeek'].apply(lambda x: 1 if x >= 5 else 0)
    
    # Lag features (Past sales to predict future sales)
    # Group by product and compute shift
    df['Sales_Lag_1Day'] = df.groupby('Product_ID')['Units_Sold'].shift(1)
    df['Sales_Lag_7Day'] = df.groupby('Product_ID')['Units_Sold'].shift(7)
    
    # Rolling averages
    df['Rolling_Mean_7Day'] = df.groupby('Product_ID')['Units_Sold'].transform(lambda x: x.rolling(window=7, min_periods=1).mean())
    df['Rolling_Mean_30Day'] = df.groupby('Product_ID')['Units_Sold'].transform(lambda x: x.rolling(window=30, min_periods=1).mean())
    
    # Drop NAs created by lagging
    df = df.dropna().reset_index(drop=True)
    
    # Save the processed data
    df.to_csv(output_path, index=False)
    print(f"Preprocessing complete. Processed data saved to {output_path}")
    
    return df

if __name__ == "__main__":
    preprocess_and_feature_engineer()
