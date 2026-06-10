import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import train_test_split
from datetime import timedelta

def train_and_forecast(input_path='data/processed_sales_data.csv', output_path='outputs/forecast_results.csv', img_dir='images'):
    """
    Trains a Random Forest Regressor to forecast daily sales demand for the next 7 days.
    Generates forecasting plots as proof.
    """
    print("Training Forecasting Model...")
    df = pd.read_csv(input_path)
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Features & Target
    features = ['Unit_Price', 'Discount_Applied', 'Month', 'DayOfWeek', 'IsWeekend', 
                'Sales_Lag_1Day', 'Sales_Lag_7Day', 'Rolling_Mean_7Day', 'Rolling_Mean_30Day']
    target = 'Units_Sold'
    
    # We will train a single general model for all products to keep it beginner-friendly
    # Advanced extension: Train a separate model per product or category.
    
    X = df[features]
    y = df[target]
    
    # Train/Test Split (Time-based split is better for time series, but simple random split for baseline)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Initialize and train Model
    model = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)
    
    # Evaluate
    predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)
    rmse = np.sqrt(mean_squared_error(y_test, predictions))
    print(f"Model Performance -> MAE: {mae:.2f}, RMSE: {rmse:.2f}")
    
    # Generate Forecast for the Next 7 Days for each product
    print("Generating Future Forecasts...")
    last_date = df['Date'].max()
    future_dates = [last_date + timedelta(days=i) for i in range(1, 8)]
    
    # Get the latest known state for each product
    latest_state = df.sort_values('Date').groupby('Product_ID').tail(1).copy()
    
    forecast_results = []
    
    for _, row in latest_state.iterrows():
        product_id = row['Product_ID']
        category = row['Category']
        current_price = row['Unit_Price']
        
        # Simulate rolling features for the next 7 days
        current_lags = {
            '1Day': row['Units_Sold'],
            '7Day': row['Sales_Lag_7Day'] # Approximation
        }
        
        for i, f_date in enumerate(future_dates):
            # Create feature vector
            feat_dict = {
                'Unit_Price': current_price,
                'Discount_Applied': 0, # Assuming no discount in future for baseline
                'Month': f_date.month,
                'DayOfWeek': f_date.dayofweek,
                'IsWeekend': 1 if f_date.dayofweek >= 5 else 0,
                'Sales_Lag_1Day': current_lags['1Day'],
                'Sales_Lag_7Day': current_lags['7Day'],
                'Rolling_Mean_7Day': row['Rolling_Mean_7Day'], 
                'Rolling_Mean_30Day': row['Rolling_Mean_30Day']
            }
            
            f_df = pd.DataFrame([feat_dict])
            pred_demand = model.predict(f_df)[0]
            
            forecast_results.append({
                'Date': f_date.strftime('%Y-%m-%d'),
                'Product_ID': product_id,
                'Category': category,
                'Forecasted_Demand': round(pred_demand, 2)
            })
            
            # Update lag for next iteration (autoregressive step)
            current_lags['1Day'] = pred_demand
            
    forecast_df = pd.DataFrame(forecast_results)
    
    os.makedirs('outputs', exist_ok=True)
    forecast_df.to_csv(output_path, index=False)
    print(f"Forecasts saved to {output_path}")
    
    # Viz - Actual vs Predicted (Sample of test set)
    plt.figure(figsize=(10, 5))
    sample_y = list(y_test)[:100]
    sample_p = predictions[:100]
    plt.plot(sample_y, label='Actual Demand', color='blue', alpha=0.6)
    plt.plot(sample_p, label='Predicted Demand', color='orange', alpha=0.8)
    plt.title('Actual vs Predicted Demand (Sample)')
    plt.legend()
    plt.tight_layout()
    os.makedirs(img_dir, exist_ok=True)
    plt.savefig(os.path.join(img_dir, 'forecast_vs_actual.png'))
    plt.close()
    
    return forecast_df

if __name__ == "__main__":
    train_and_forecast()
