
import pandas as pd

# Load cleaned transaction data
df = pd.read_csv(
    "processed/cleaned_transactions.csv",
    dtype={"InvoiceNo": "string"}
)

df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

# Calculate revenue
df["Revenue"] = df["Quantity"] * df["UnitPrice"]

# Investigate December 9, 2011
target_date = pd.Timestamp("2011-12-09")

day_data = df[df["InvoiceDate"].dt.date == target_date.date()]

print("=" * 65)
print("REVENUE SPIKE INVESTIGATION")
print("=" * 65)

print("\n1. DECEMBER 9 TRANSACTION SUMMARY")

print("Transaction lines:", len(day_data))
print("Unique invoices:", day_data["InvoiceNo"].nunique())
print("Total quantity:", day_data["Quantity"].sum())
print("Total revenue:", round(day_data["Revenue"].sum(), 2))

# 2. Top 10 invoices by revenue
invoice_sales = day_data.groupby("InvoiceNo").agg(
    Revenue=("Revenue", "sum"),
    ItemsSold=("Quantity", "sum")
).sort_values("Revenue", ascending=False)

print("\n2. TOP 10 INVOICES ON DECEMBER 9")
print(invoice_sales.head(10).round(2).to_string())

# 3. Top 10 transaction lines
print("\n3. TOP 10 INDIVIDUAL TRANSACTION LINES")

print(
    day_data.nlargest(10, "Revenue")[
        ["InvoiceNo", "StockCode", "Description",
         "Quantity", "UnitPrice", "Revenue"]
    ].to_string(index=False)
)

# 4. Overall daily revenue outliers
daily = pd.read_csv("processed/daily_sales.csv")

print("\n4. DAILY REVENUE OUTLIER THRESHOLDS")

q1 = daily["Revenue"].quantile(0.25)
q3 = daily["Revenue"].quantile(0.75)
iqr = q3 - q1

upper_limit = q3 + 1.5 * iqr

print("Q1:", round(q1, 2))
print("Q3:", round(q3, 2))
print("IQR:", round(iqr, 2))
print("Upper outlier threshold:", round(upper_limit, 2))

outliers = daily[daily["Revenue"] > upper_limit]

print("\nNumber of high-revenue outlier days:", len(outliers))
print(outliers.sort_values("Revenue", ascending=False).head(10).to_string(index=False))

print("\nOUTLIER INVESTIGATION COMPLETED")
