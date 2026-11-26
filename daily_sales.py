
import pandas as pd
import os

# Load cleaned dataset
df = pd.read_csv(
    "processed/cleaned_transactions.csv",
    dtype={"InvoiceNo": "string"}
)

# Convert InvoiceDate to datetime
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

# Extract transaction date
df["Date"] = df["InvoiceDate"].dt.normalize()

# Aggregate transactions by date
daily_sales = df.groupby("Date").agg(
    Revenue=("Revenue", "sum"),
    Transactions=("InvoiceNo", "nunique"),
    ItemsSold=("Quantity", "sum")
)

# Include missing calendar dates
daily_sales = daily_sales.asfreq("D", fill_value=0)

# Reset index
daily_sales = daily_sales.reset_index()

# Save daily sales dataset
os.makedirs("processed", exist_ok=True)

daily_sales.to_csv(
    "processed/daily_sales.csv",
    index=False
)

# Display results
print("=" * 60)
print("DAILY SALES AGGREGATION")
print("=" * 60)

print("\nFirst 10 days:")
print(daily_sales.head(10))

print("\nDataset shape:", daily_sales.shape)

print("\nDate range:")
print("Start:", daily_sales["Date"].min())
print("End:", daily_sales["Date"].max())

print("\nDaily Revenue Statistics:")
print(daily_sales["Revenue"].describe())

print("\nTotal Revenue: £", round(daily_sales["Revenue"].sum(), 2))
print("Total Transactions:", daily_sales["Transactions"].sum())
print("Total Items Sold:", daily_sales["ItemsSold"].sum())

print("\nMissing values:")
print(daily_sales.isnull().sum())

print("\nDaily sales dataset saved successfully!")
print("Location: processed/daily_sales.csv")
