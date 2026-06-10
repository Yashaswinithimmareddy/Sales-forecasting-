"""
Retail Sales Forecasting & Inventory Optimization System
Main Execution Script

This script acts as the orchestrator to run the entire pipeline:
1. Synthetic Data Generation
2. Preprocessing & Feature Engineering
3. Machine Learning Forecasting
4. Inventory Optimization Logic
"""

import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from data_generator import generate_synthetic_data
from preprocessing import preprocess_and_feature_engineer
from forecasting import train_and_forecast
from inventory_logic import calculate_inventory_metrics

def main():
    print("=" * 60)
    print(" RETAIL SALES FORECASTING & INVENTORY OPTIMIZATION SYSTEM ")
    print("=" * 60)
    
    # Ensure directories exist
    os.makedirs('data', exist_ok=True)
    os.makedirs('outputs', exist_ok=True)
    os.makedirs('images', exist_ok=True)
    
    # Step 1: Data Generation
    print("\n--- STEP 1: Generative Simulation ---")
    raw_df = generate_synthetic_data(num_days=730, output_dir='data')
    
    # Step 2: Preprocessing
    print("\n--- STEP 2: Preprocessing & Feature Engineering ---")
    proc_df = preprocess_and_feature_engineer(input_path='data/raw_sales_data.csv', 
                                              output_path='data/processed_sales_data.csv')
    
    # Step 3: Forecasting
    if proc_df is not None:
        print("\n--- STEP 3: ML Sales Forecasting ---")
        forecast_df = train_and_forecast(input_path='data/processed_sales_data.csv', 
                                         output_path='outputs/forecast_results.csv',
                                         img_dir='images')
        
        # Step 4: Inventory Logic
        print("\n--- STEP 4: Inventory Optimization Logic ---")
        inventory_df = calculate_inventory_metrics(forecast_path='outputs/forecast_results.csv',
                                                   hist_path='data/processed_sales_data.csv',
                                                   output_path='outputs/inventory_recommendations.csv')
                                                   
        print("\n" + "=" * 60)
        print(" PIPELINE COMPLETED SUCCESSFULLY! ")
        print(" Please check 'data', 'outputs', and 'images' folders. ")
        print("=" * 60)
    else:
        print("Pipeline failed during preprocessing. Please check your data.")

if __name__ == "__main__":
    main()
