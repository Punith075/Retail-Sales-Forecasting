
import pandas as pd
import os

os.makedirs("processed", exist_ok=True)

def split_dataset(input_file, prefix):

    df = pd.read_csv(input_file)
    df["Date"] = pd.to_datetime(df["Date"])

    # Chronological 80/20 split
    split_index = int(len(df) * 0.8)

    train = df.iloc[:split_index].copy()
    test = df.iloc[split_index:].copy()

    train.to_csv(
        f"processed/{prefix}_train.csv",
        index=False
    )

    test.to_csv(
        f"processed/{prefix}_test.csv",
        index=False
    )

    print(f"\n{prefix.upper()} DATASET")
    print("Training records:", len(train))
    print("Testing records:", len(test))
    print("Training period:", train["Date"].min(), "to", train["Date"].max())
    print("Testing period:", test["Date"].min(), "to", test["Date"].max())

# Model A
split_dataset(
    "processed/features_baseline.csv",
    "baseline"
)

# Model B
split_dataset(
    "processed/features_sensitivity.csv",
    "sensitivity"
)

print("\nTRAIN/TEST SPLIT COMPLETED")
