
import pandas as pd
import os

# Load cleaned transaction data
df = pd.read_csv(
    "processed/cleaned_transactions.csv",
    dtype={"InvoiceNo": "string"}
)

df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

# Create output directory
os.makedirs("processed", exist_ok=True)


def create_daily_sales(data, filename):

    data = data.copy()

    # Extract transaction date
    data["Date"] = data["InvoiceDate"].dt.normalize()

    # Aggregate daily sales
    daily = data.groupby("Date").agg(
        Revenue=("Revenue", "sum"),
        Transactions=("InvoiceNo", "nunique"),
        ItemsSold=("Quantity", "sum")
    )

    # Include all calendar days
    daily = daily.asfreq("D", fill_value=0)

    daily = daily.reset_index()

    # Save dataset
    daily.to_csv(
        f"processed/{filename}",
        index=False
    )

    return daily


# MODEL A: All transactions
baseline = create_daily_sales(
    df,
    "daily_sales_baseline.csv"
)

# MODEL B: Exclude exceptional invoice
sensitivity_df = df[
    df["InvoiceNo"] != "581483"
]

sensitivity = create_daily_sales(
    sensitivity_df,
    "daily_sales_sensitivity.csv"
)

# Display comparison
print("=" * 60)
print("FORECASTING DATASET PREPARATION")
print("=" * 60)

print("\nMODEL A - ALL TRANSACTIONS")
print("Total Revenue:", round(baseline["Revenue"].sum(), 2))
print("Daily Records:", len(baseline))

print("\nMODEL B - EXCLUDING INVOICE 581483")
print("Total Revenue:", round(sensitivity["Revenue"].sum(), 2))
print("Daily Records:", len(sensitivity))

print("\nDECEMBER 9 COMPARISON")

date = pd.Timestamp("2011-12-09")

print("Model A:",
      baseline.loc[baseline["Date"] == date, "Revenue"].iloc[0])

print("Model B:",
      sensitivity.loc[sensitivity["Date"] == date, "Revenue"].iloc[0])

print("\nBoth forecasting datasets saved successfully!")
print("FORECASTING DATA PREPARATION COMPLETED")
