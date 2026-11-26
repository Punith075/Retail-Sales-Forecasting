# RetailIQ – Retail Sales Forecasting & Inventory Optimization

A data science project that analyzes historical retail transactions, forecasts future sales, and generates data-driven inventory replenishment recommendations through an interactive Streamlit dashboard.

## Overview

Retail businesses need to understand sales patterns, anticipate future demand, and maintain appropriate inventory levels. RetailIQ addresses these challenges using Python-based data analysis, forecasting techniques, and inventory optimization.

The project uses the **UCI Online Retail dataset** to analyze transaction history, identify sales trends, compare forecasting methods, and estimate product-level reorder requirements.

## Key Features

- **Sales Analytics:** Explore revenue, transactions, units sold, and historical sales trends.
- **Sales Forecasting:** Generate a 30-day sales projection using historical weekday patterns.
- **Inventory Intelligence:** Analyze product demand, safety stock, reorder points, and recommended reorder quantities.
- **Model Evaluation:** Compare forecasting methods using MAE, RMSE, and MAPE.
- **Interactive Dashboard:** Explore business insights through a multi-page Streamlit application.
- **Data Export:** Download sales, forecast, and inventory reports as CSV files.

## Dataset

**Source:** UCI Machine Learning Repository – Online Retail

The dataset contains transactions from a UK-based online retail business between **1 December 2010 and 9 December 2011**.

It includes:
- Invoice number
- Stock code
- Product description
- Quantity
- Invoice date
- Unit price
- Customer ID
- Country

The original dataset contains 541,909 transaction records.

## Technologies Used

| Category | Tools |
|---|---|
| Programming | Python |
| Data Analysis | Pandas, NumPy |
| Machine Learning | Scikit-learn |
| Statistical Analysis | Statsmodels |
| Visualization | Plotly, Matplotlib, Seaborn |
| Dashboard | Streamlit |
| Data Storage | CSV, Excel |

## Project Workflow

1. **Data Cleaning:** Remove duplicate transactions, cancellations, and invalid quantity or price records.
2. **Exploratory Data Analysis:** Analyze daily and monthly revenue, transaction patterns, and seasonality.
3. **Feature Engineering:** Create calendar features, lag variables, and rolling averages.
4. **Model Development:** Train and compare Naive Forecast, Linear Regression, and Random Forest models.
5. **Forecast Validation:** Evaluate forecasting methods using a chronological train-test split.
6. **Inventory Optimization:** Calculate average demand, demand variability, safety stock, reorder points, and suggested replenishment quantities.
7. **Dashboard Development:** Present the results through an interactive Streamlit dashboard.

## Model Performance

The forecasting methods were evaluated on the same historical test period.

| Forecasting Method | MAE (£) | RMSE (£) | MAPE |
|---|---:|---:|---:|
| Naive Forecast | 25,438.90 | 33,581.24 | 43.24% |
| Random Forest | 14,336.56 | 24,428.11 | 28.23% |
| Weekday Median | 13,786.86 | 24,175.15 | 26.57% |

**Best validated method:** Weekday Median, based on the lowest RMSE on the historical test set.

## Inventory Optimization

The inventory module calculates:

- Average daily product demand
- Daily demand variability
- Safety stock
- Reorder point
- Target stock level
- Recommended reorder quantity

The initial analysis assumes a 7-day supplier lead time, a 7-day review period, and a service-level Z-score of 1.65.

These are illustrative replenishment estimates. Actual stock on hand and supplier-specific lead times are not available in the dataset.

## Dashboard Pages

1. Business Overview
2. Sales Analytics
3. Sales Forecast
4. Inventory Intelligence
5. Model Performance

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/Punith075/Retail-Sales-Forecasting.git
cd Retail-Sales-Forecasting
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Run the dashboard

```bash
python -m streamlit run app.py
```

The dashboard will open in your browser.

## Project Structure

```text
Retail-Sales-Forecasting/
│
├── data/
│   └── Online Retail.xlsx
│
├── processed/
│   ├── cleaned_transactions.csv
│   ├── daily_sales.csv
│   ├── daily_sales_baseline.csv
│   ├── daily_sales_sensitivity.csv
│   ├── features_baseline.csv
│   └── features_sensitivity.csv
│
├── reports/
│   ├── plots/
│   ├── baseline_model_results.csv
│   ├── forecast_validation_results.csv
│   ├── inventory_optimization.csv
│   ├── next_30_days_forecast.csv
│   └── top_10_products.csv
│
├── app.py
├── data_cleaning.py
├── daily_sales.py
├── eda.py
├── seasonality_analysis.py
├── prepare_forecasting.py
├── feature_engineering.py
├── train_test_split.py
├── model_training.py
├── visualization.py
├── future_forecast.py
├── forecast_validation.py
├── inventory_optimization.py
├── requirements.txt
└── README.md
```

## Important Notes

- The dataset is historical and ends on 9 December 2011. The 30-day forecast is an illustrative projection following that historical period, not a forecast of current retail sales.
- The inventory recommendations use assumed lead and review periods and do not account for actual inventory on hand.
- Forecast performance is evaluated on a chronological historical test set.

## Future Enhancements

- Integrate real-time retail sales data.
- Experiment with additional time-series forecasting models.
- Incorporate actual stock levels and supplier lead times.
- Add automated low-stock alerts.
- Deploy the dashboard to a cloud platform.

## Author

**Punith Reddy K S**

Computer Science and Engineering Student

GitHub: [Punith075](https://github.com/Punith075)

---

*Built with Python, Pandas, Scikit-learn, Plotly, and Streamlit.*