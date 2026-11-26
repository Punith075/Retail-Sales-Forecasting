
import pandas as pd

df = pd.read_csv(
    "processed/cleaned_transactions.csv",
    dtype={"InvoiceNo": "string"}
)

# Investigate invoice 581483
invoice = df[df["InvoiceNo"] == "581483"].copy()

print("=" * 60)
print("LARGE INVOICE INVESTIGATION")
print("=" * 60)

print("\n1. INVOICE DETAILS")

print("Invoice Number:", invoice["InvoiceNo"].iloc[0])
print("Invoice Date:", invoice["InvoiceDate"].iloc[0])
print("Customer ID:", invoice["CustomerID"].iloc[0])
print("Country:", invoice["Country"].iloc[0])

print("\n2. PRODUCT DETAILS")

print(invoice[[
    "StockCode",
    "Description",
    "Quantity",
    "UnitPrice"
]].to_string(index=False))

# Calculate invoice revenue
invoice_revenue = (
    invoice["Quantity"] * invoice["UnitPrice"]
).sum()

print("\n3. INVOICE REVENUE")
print("Total Quantity:", invoice["Quantity"].sum())
print("Total Revenue:", round(invoice_revenue, 2))

# Compare with December 9 revenue
day_data = df[
    pd.to_datetime(df["InvoiceDate"]).dt.date
    == pd.Timestamp("2011-12-09").date()
]

day_revenue = (
    day_data["Quantity"] * day_data["UnitPrice"]
).sum()

remaining_revenue = day_revenue - invoice_revenue

print("\n4. IMPACT ON DAILY REVENUE")
print("Actual daily revenue:", round(day_revenue, 2))
print("Invoice contribution:", round(invoice_revenue, 2))
print("Revenue excluding this invoice:", round(remaining_revenue, 2))

print("\nINVESTIGATION COMPLETED")
