import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt

def calculate_inventory_metrics(forecast_path='outputs/forecast_results.csv', 
                                hist_path='data/processed_sales_data.csv',
                                output_path='outputs/inventory_recommendations.csv'):
    """
    Calculates essential inventory optimization metrics:
    - Safety Stock = Z * sqrt( (LeadTime * CurrentDemandStdDev^2) )
    - Reorder Point (ROP) = (LeadTime * AvgDailyDemand) + SafetyStock
    """
    print("Calculating Inventory Optimization Metrics...")
    
    forecast_df = pd.read_csv(forecast_path)
    hist_df = pd.read_csv(hist_path)
    
    # Aggregate Historical Metrics
    # Calculate Mean Daily Demand and Std Dev per product
    hist_stats = hist_df.groupby('Product_ID').agg(
        Avg_Daily_Demand=('Units_Sold', 'mean'),
        StdDev_Demand=('Units_Sold', 'std')
    ).reset_index()
    
    # For future demand, use the sum of 7-day forecast
    # We treat Lead Time as 3 days
    LEAD_TIME = 3
    Z_SCORE = 1.65 # 95% Service Level
    
    recommendations = []
    
    # We will simulate a current stock level for each product
    current_stocks = {}
    
    for _, row in hist_stats.iterrows():
        prod_id = row['Product_ID']
        avg_demand = row['Avg_Daily_Demand']
        std_demand = row['StdDev_Demand']
        
        # Simulated Current Stock Level
        # between 0.5x to 2x of weekly demand
        current_stock = int(np.random.uniform(0.5, 2.0) * avg_demand * 7)
        
        # Calculate Safety Stock
        # Rule of thumb formula: Z * std_demand * sqrt(LeadTime)
        safety_stock = Z_SCORE * std_demand * np.sqrt(LEAD_TIME)
        
        # Calculate Reorder Point
        reorder_point = (avg_demand * LEAD_TIME) + safety_stock
        
        # Recommendation Logic
        status = "Healthy"
        reorder_amount = 0
        
        if current_stock <= reorder_point:
            status = "Reorder Needed"
            # Reorder up to 14 days of average demand
            target_stock = avg_demand * 14 + safety_stock
            reorder_amount = max(0, target_stock - current_stock)
        
        recommendations.append({
            'Product_ID': prod_id,
            'Current_Stock': current_stock,
            'Avg_Daily_Demand': round(avg_demand, 2),
            'Safety_Stock': round(safety_stock, 0),
            'Reorder_Point': round(reorder_point, 0),
            'Status': status,
            'Recommended_Order_Qty': round(reorder_amount, 0)
        })
        
    rec_df = pd.DataFrame(recommendations)
    rec_df.to_csv(output_path, index=False)
    print(f"Inventory recommendations saved to {output_path}")
    
    # Visualization: Stock Status Distribution
    plt.figure(figsize=(8, 6))
    status_counts = rec_df['Status'].value_counts()
    status_counts.plot(kind='bar', color=['skyblue', 'salmon'])
    plt.title('Inventory Status Across Products')
    plt.ylabel('Number of Products')
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig('images/inventory_alerts.png')
    plt.close()
    
    return rec_df

if __name__ == "__main__":
    calculate_inventory_metrics()
