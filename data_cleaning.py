
import pandas as pd
import os

# Load original dataset
df = pd.read_excel("data/Online Retail.xlsx")

print("=" * 60)
print("RETAIL DATA CLEANING")
print("=" * 60)

print("Original records:", len(df))

# Step 1: Remove exact duplicate records
df = df.drop_duplicates()
print("After removing duplicates:", len(df))

# Step 2: Remove cancelled invoices
df = df[
    ~df["InvoiceNo"].astype(str).str.startswith("C")
]

print("After removing cancelled invoices:", len(df))

# Step 3: Retain only positive quantities
df = df[df["Quantity"] > 0]

print("After removing non-positive quantities:", len(df))

# Step 4: Retain only positive prices
df = df[df["UnitPrice"] > 0]

print("After removing non-positive prices:", len(df))

# Step 5: Calculate revenue
df["Revenue"] = df["Quantity"] * df["UnitPrice"]

# Step 6: Sort transactions by date
df = df.sort_values("InvoiceDate")

# Step 7: Create processed folder
os.makedirs("processed", exist_ok=True)

# Step 8: Save cleaned dataset
df.to_csv(
    "processed/cleaned_transactions.csv",
    index=False
)

# Step 9: Display cleaning results
print("\n" + "=" * 60)
print("DATA CLEANING SUMMARY")
print("=" * 60)

print("Original records: 541909")
print("Cleaned records:", len(df))
print("Removed records:", 541909 - len(df))
print("Remaining missing CustomerIDs:", df["CustomerID"].isnull().sum())
print("Remaining missing Descriptions:", df["Description"].isnull().sum())
print("Remaining duplicates:", df.duplicated().sum())

print("\nRevenue statistics:")
print(df["Revenue"].describe())

print("\nCleaned dataset saved successfully!")
print("Location: processed/cleaned_transactions.csv")

print("\nDATA CLEANING COMPLETED")
