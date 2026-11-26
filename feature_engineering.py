
import pandas as pd
import os

os.makedirs("processed", exist_ok=True)


def create_features(input_file, output_file):

    # Load daily sales dataset
    df = pd.read_csv(input_file)
    df["Date"] = pd.to_datetime(df["Date"])

    # Sort chronologically
    df = df.sort_values("Date").reset_index(drop=True)

    # Calendar features
    df["Day"] = df["Date"].dt.day
    df["DayOfWeek"] = df["Date"].dt.day_of_week
    df["Month"] = df["Date"].dt.month
    df["Quarter"] = df["Date"].dt.quarter
    df["IsWeekend"] = (df["DayOfWeek"] >= 5).astype(int)

    # Historical revenue features
    df["Lag_1"] = df["Revenue"].shift(1)
    df["Lag_7"] = df["Revenue"].shift(7)
    df["Lag_14"] = df["Revenue"].shift(14)

    # Rolling averages using previous days only
    df["Rolling_Mean_7"] = (
        df["Revenue"].shift(1).rolling(window=7).mean()
    )

    df["Rolling_Mean_14"] = (
        df["Revenue"].shift(1).rolling(window=14).mean()
    )

    # Remove rows without sufficient historical data
    df = df.dropna().reset_index(drop=True)

    # Save engineered dataset
    df.to_csv(output_file, index=False)

    return df


print("=" * 65)
print("FEATURE ENGINEERING")
print("=" * 65)

# Model A
baseline = create_features(
    "processed/daily_sales_baseline.csv",
    "processed/features_baseline.csv"
)

# Model B
sensitivity = create_features(
    "processed/daily_sales_sensitivity.csv",
    "processed/features_sensitivity.csv"
)

print("\nMODEL A - BASELINE")
print("Shape:", baseline.shape)
print("Features:", baseline.columns.tolist())

print("\nMODEL B - SENSITIVITY")
print("Shape:", sensitivity.shape)

print("\nFIRST 5 ENGINEERED RECORDS")
print(baseline.head().to_string(index=False))

print("\nMISSING VALUES")
print(baseline.isnull().sum())

print("\nFiles saved successfully:")
print("processed/features_baseline.csv")
print("processed/features_sensitivity.csv")

print("\nFEATURE ENGINEERING COMPLETED")
