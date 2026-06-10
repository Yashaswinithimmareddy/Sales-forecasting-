# Retail Sales Forecasting & Inventory Optimization System

## 📌 Project Overview
This project is an end-to-end Machine Learning solution designed to predict retail sales demand and optimize inventory management. Using theoretical retail data, it simulates historical sales, applies a Random Forest regression model for demand forecasting, and uses industry-standard logic (Safety Stock, Reorder Point) to generate automated inventory purchase recommendations.

---

## 🎯 Problem Statement
In retail, ordering too much stock leads to dead capital and warehouse costs (overstocking), while ordering too little leads to lost sales and unhappy customers (stockouts). 

## 💡 Business Value
By accurately forecasting demand and programmatically calculating safety stock, this system helps retailers:
- Minimize holding costs by optimizing inventory levels.
- Maximize revenue by preventing out-of-stock scenarios.
- Automate the supply chain decision-making process.

---

## 🛠 Tech Stack
* **Language:** Python
* **Data Processing & Feature Engineering:** Pandas, NumPy
* **Machine Learning Model:** Scikit-Learn (RandomForestRegressor)
* **Visualization:** Matplotlib, Seaborn

---

## 🏗 Architecture
1. **Data Generator Module:** Simulates 2 years of daily retail data across various categories with seasonality and noise.
2. **Preprocessing Module:** Cleans data and engineers time-series features (Rolling Means, Lags, Day-of-Week).
3. **Forecasting Module:** Trains a Random Forest model and predicts the next 7 days of demand.
4. **Inventory Optimization Module:** Calculates Safety Stock, Lead Time demand, and triggers Reorder Points.

---

## 📁 Folder Structure
```text
Retail-Sales-Forecasting-Inventory-Optimization/
│
├── data/
│   ├── raw_sales_data.csv        (Generated synthetic data)
│   └── processed_sales_data.csv  (Cleaned data)
├── src/
│   ├── data_generator.py         (Step 1: Simulator for demand)
│   ├── preprocessing.py          (Step 2: Cleaning & EDA hooks)
│   ├── forecasting.py            (Step 3: ML model training & prediction)
│   └── inventory_logic.py        (Step 4: Safety stock, reorder point)
├── outputs/
│   ├── inventory_recommendations.csv
│   └── forecast_results.csv
├── images/                       (Generated graphs)
│   ├── forecast_vs_actual.png
│   └── inventory_alerts.png
├── docs/
│   └── Project_Guide.md          (Extensive Interview & Concept Guide)
├── requirements.txt
├── README.md
└── main.py                       (Orchestrator script)
```

---

## ⚡ How to Run the Project

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Full Pipeline
```bash
python main.py
```

### Expected Output
The script will run the 4 steps sequentially. Ensure you review the `outputs/inventory_recommendations.csv` for the final actionable supply chain data.

---

## 📈 Results & Visuals
*(Insert screenshots from the `images/` directory here once uploaded to GitHub)*
- Forecasting Trend
- Inventory Alert Status

---

## 🚀 Future Improvements
- Implement separate forecasting models per category / product.
- Add external regressors like holidays and macro-economic factors.
- Connect an interactive web dashboard (e.g., Streamlit / PowerBI).
- Implement deep learning (LSTMs) for complex temporal dependencies.

---

## 🧑‍💻 Author
Built as a professional portfolio project demonstrating applied data science in Supply Chain & Retail Analytics.
