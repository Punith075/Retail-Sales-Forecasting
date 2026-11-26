
import pandas as pd
import numpy as np
import os

os.makedirs("reports", exist_ok=True)

# 1. Load cleaned transaction data
df = pd.read_csv(
    "processed/cleaned_transactions.csv",
    dtype={"InvoiceNo": "string"}
)

df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
df["Date"] = df["InvoiceDate"].dt.normalize()

df = df.dropna(subset=["StockCode", "Description"])

# 2. Product-level summary
product_summary = df.groupby(
    ["StockCode", "Description"]
).agg(
    Total_Units_Sold=("Quantity", "sum"),
    Total_Revenue=("Revenue", "sum"),
    Total_Transactions=("InvoiceNo", "nunique"),
    Average_Unit_Price=("UnitPrice", "mean")
).reset_index()

# 3. Define analysis period
start_date = df["Date"].min()
end_date = df["Date"].max()

all_dates = pd.date_range(
    start=start_date,
    end=end_date,
    freq="D"
)

total_days = len(all_dates)

# 4. Calculate average daily demand
product_summary["Average_Daily_Demand"] = (
    product_summary["Total_Units_Sold"] / total_days
)

# 5. Aggregate sales by product and date
daily_product_sales = (
    df.groupby(["StockCode", "Date"])["Quantity"]
    .sum()
    .reset_index(name="Daily_Quantity")
)

# 6. Calculate daily demand variability
product_std = []

for stock_code in product_summary["StockCode"]:

    product_data = daily_product_sales[
        daily_product_sales["StockCode"] == stock_code
    ]

    # Grouping guarantees unique dates for each product
    daily_values = (
        product_data
        .set_index("Date")["Daily_Quantity"]
        .reindex(all_dates, fill_value=0)
    )

    product_std.append(daily_values.std())

product_summary["Daily_Demand_Std"] = product_std

# 7. Inventory planning assumptions
LEAD_TIME_DAYS = 7
REVIEW_PERIOD_DAYS = 7
SERVICE_LEVEL_Z = 1.65

# 8. Calculate safety stock
product_summary["Safety_Stock"] = (
    SERVICE_LEVEL_Z
    * product_summary["Daily_Demand_Std"]
    * np.sqrt(LEAD_TIME_DAYS)
)

# 9. Calculate reorder point
product_summary["Reorder_Point"] = (
    product_summary["Average_Daily_Demand"]
    * LEAD_TIME_DAYS
    + product_summary["Safety_Stock"]
)

# 10. Calculate target stock
product_summary["Target_Stock"] = (
    product_summary["Average_Daily_Demand"]
    * (LEAD_TIME_DAYS + REVIEW_PERIOD_DAYS)
    + product_summary["Safety_Stock"]
)

# 11. Recommended replenishment quantity
product_summary["Recommended_Reorder_Qty"] = np.ceil(
    product_summary["Target_Stock"]
).astype(int)

# 12. Rank products by revenue
product_summary = product_summary.sort_values(
    "Total_Revenue",
    ascending=False
)

# 13. Save complete inventory report
product_summary.to_csv(
    "reports/inventory_optimization.csv",
    index=False
)

# 14. Display top 10 products
print("\nTOP 10 PRODUCTS BY REVENUE")
print("=" * 80)

columns = [
    "StockCode",
    "Description",
    "Total_Units_Sold",
    "Total_Revenue",
    "Average_Daily_Demand",
    "Safety_Stock",
    "Reorder_Point",
    "Recommended_Reorder_Qty"
]

print(
    product_summary[columns]
    .head(10)
    .round(2)
    .to_string(index=False)
)

# 15. Save top 10 products
product_summary.head(10).to_csv(
    "reports/top_10_products.csv",
    index=False
)

# 16. Summary
print("\nINVENTORY SUMMARY")
print("=" * 40)
print("Products analyzed:", len(product_summary))
print("Analysis period:", start_date.date(), "to", end_date.date())
print("Total days:", total_days)
print("Lead time:", LEAD_TIME_DAYS, "days")
print("Review period:", REVIEW_PERIOD_DAYS, "days")

print("\nInventory optimization results saved successfully!")
print("INVENTORY OPTIMIZATION COMPLETED!")
