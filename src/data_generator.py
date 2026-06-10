import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def generate_synthetic_data(num_days=730, output_dir='data'):
    """
    Generates synthetic daily sales data for a retail store over a given number of days.
    Simulates multiple product categories, seasonality, and random demand fluctuations.
    """
    print("Generating synthetic retail data...")
    
    # Store settings
    categories = ['Electronics', 'Clothing', 'Groceries', 'Furniture', 'Toys']
    products_per_category = 10
    
    # Generate Product IDs
    products = []
    for cat in categories:
        for i in range(1, products_per_category + 1):
            products.append({
                'Product_ID': f"{cat[:3].upper()}_{i:03d}",
                'Category': cat,
                'Base_Price': np.random.uniform(10.0, 500.0),
                'Base_Demand': np.random.randint(5, 50)
            })
    
    product_df = pd.DataFrame(products)
    
    # Time settings - Last 2 years
    end_date = datetime.now()
    start_date = end_date - timedelta(days=num_days)
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    
    sales_data = []
    
    # Generate daily sales
    for date in date_range:
        # Determine day of week and month for seasonality
        day_of_week = date.weekday()
        month = date.month
        
        # Weekend multiplier (higher sales on weekends)
        weekend_mult = 1.3 if day_of_week >= 5 else 1.0
        
        # Holiday seasonality (e.g., Nov-Dec bump)
        holiday_mult = 1.5 if month in [11, 12] else 1.0
        
        for _, prod in product_df.iterrows():
            # Add random noise
            noise = np.random.normal(0, 0.2)
            
            # Calculate daily demand
            demand_multiplier = weekend_mult * holiday_mult * (1 + noise)
            units_sold = max(0, int(prod['Base_Demand'] * demand_multiplier))
            
            # Random occasional stockouts (0 sales)
            if np.random.random() < 0.02: # 2% chance of stockout
                units_sold = 0
                
            discount = np.random.choice([0, 0.1, 0.2], p=[0.7, 0.2, 0.1])
            selling_price = prod['Base_Price'] * (1 - discount)
            
            revenue = units_sold * selling_price
            
            sales_data.append({
                'Date': date.strftime('%Y-%m-%d'),
                'Product_ID': prod['Product_ID'],
                'Category': prod['Category'],
                'Units_Sold': units_sold,
                'Unit_Price': round(selling_price, 2),
                'Total_Revenue': round(revenue, 2),
                'Discount_Applied': discount
            })
            
    sales_df = pd.DataFrame(sales_data)
    
    # Save to CSV
    os.makedirs(output_dir, exist_ok=True)
    out_path = os.path.join(output_dir, 'raw_sales_data.csv')
    sales_df.to_csv(out_path, index=False)
    
    print(f"Data generated successfully! Shape: {sales_df.shape}")
    print(f"File saved to {out_path}")
    
    return sales_df

if __name__ == "__main__":
    generate_synthetic_data()
