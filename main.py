
import pandas as pd

df = pd.read_excel("data/Online Retail.xlsx")

# 1. Investigate cancelled invoices
print("\n1. CANCELLED INVOICES")
cancelled = df[df["InvoiceNo"].astype(str).str.startswith("C")]
print("Cancelled invoice records:", len(cancelled))
print(cancelled[["InvoiceNo", "Quantity", "UnitPrice"]].head(10))

# 2. Investigate negative quantities
print("\n2. NEGATIVE QUANTITY EXAMPLES")
negative_qty = df[df["Quantity"] < 0]
print(negative_qty[[
    "InvoiceNo", "StockCode", "Description",
    "Quantity", "UnitPrice"
]].head(10))

# 3. Investigate zero-price transactions
print("\n3. ZERO PRICE EXAMPLES")
zero_price = df[df["UnitPrice"] == 0]
print(zero_price[[
    "InvoiceNo", "StockCode", "Description",
    "Quantity", "UnitPrice"
]].head(10))

# 4. Investigate negative prices
print("\n4. NEGATIVE PRICE EXAMPLES")
negative_price = df[df["UnitPrice"] < 0]
print(negative_price[[
    "InvoiceNo", "StockCode", "Description",
    "Quantity", "UnitPrice"
]])

# 5. Investigate duplicates
print("\n5. DUPLICATE RECORD EXAMPLES")
duplicates = df[df.duplicated(keep=False)]
print(duplicates.head(10))

# 6. Calculate original transaction revenue
df["Revenue"] = df["Quantity"] * df["UnitPrice"]

print("\n6. REVENUE SUMMARY")
print(df["Revenue"].describe())

print("\nINVESTIGATION COMPLETED")
