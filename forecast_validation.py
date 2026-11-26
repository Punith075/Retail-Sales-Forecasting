
import pandas as pd
import numpy as np
import os

from sklearn.metrics import mean_absolute_error, mean_squared_error

os.makedirs("reports", exist_ok=True)

# Load test data
test = pd.read_csv("processed/baseline_test.csv")
test["Date"] = pd.to_datetime(test["Date"])

# Load Random Forest predictions
rf_predictions = pd.read_csv("reports/baseline_predictions.csv")
rf_predictions["Date"] = pd.to_datetime(rf_predictions["Date"])

# Merge predictions with test data
test = test.merge(
    rf_predictions[["Date", "Random_Forest"]],
    on="Date",
    how="left"
)

# Check for missing predictions
if test["Random_Forest"].isna().any():
    raise ValueError("Missing Random Forest predictions after merging.")

# Load historical sales
history = pd.read_csv("processed/daily_sales_baseline.csv")
history["Date"] = pd.to_datetime(history["Date"])

# Generate weekday median predictions
weekday_predictions = []

for _, row in test.iterrows():

    forecast_date = row["Date"]
    weekday = forecast_date.day_of_week

    previous_sales = history[
        (history["Date"] < forecast_date) &
        (history["Date"].dt.day_of_week == weekday)
    ].tail(8)

    prediction = previous_sales["Revenue"].median()

    if pd.isna(prediction):
        prediction = history["Revenue"].median()

    weekday_predictions.append(prediction)

test["Weekday_Median"] = weekday_predictions

# Evaluation function
def evaluate_model(name, actual, predicted):

    mae = mean_absolute_error(actual, predicted)
    rmse = np.sqrt(mean_squared_error(actual, predicted))

    non_zero = actual != 0

    if non_zero.any():
        mape = np.mean(
            np.abs(
                (actual[non_zero] - predicted[non_zero])
                / actual[non_zero]
            )
        ) * 100
    else:
        mape = np.nan

    return {
        "Model": name,
        "MAE": mae,
        "RMSE": rmse,
        "MAPE (%)": mape
    }


# Evaluate models
actual = test["Revenue"]

results = [
    evaluate_model(
        "Naive Forecast",
        actual,
        test["Lag_1"]
    ),
    evaluate_model(
        "Random Forest",
        actual,
        test["Random_Forest"]
    ),
    evaluate_model(
        "Weekday Median",
        actual,
        test["Weekday_Median"]
    )
]

results_df = pd.DataFrame(results)

# Display results
print("\nFORECAST MODEL VALIDATION")
print("=" * 60)
print(results_df.round(2).to_string(index=False))

# Best model
best_model = results_df.loc[
    results_df["RMSE"].idxmin()
]

print("\nBEST MODEL BASED ON RMSE:")
print(best_model["Model"])
print("RMSE:", round(best_model["RMSE"], 2))

# Save evaluation results
results_df.to_csv(
    "reports/forecast_validation_results.csv",
    index=False
)

# Save prediction comparison
test[
    [
        "Date",
        "Revenue",
        "Lag_1",
        "Random_Forest",
        "Weekday_Median"
    ]
].to_csv(
    "reports/forecast_validation_predictions.csv",
    index=False
)

print("\nValidation results saved successfully!")
print("FORECAST VALIDATION COMPLETED!")
