
import pandas as pd
import numpy as np
import os

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error

os.makedirs("reports", exist_ok=True)

# Features used for forecasting
FEATURES = [
    "Day",
    "DayOfWeek",
    "Month",
    "Quarter",
    "IsWeekend",
    "Lag_1",
    "Lag_7",
    "Lag_14",
    "Rolling_Mean_7",
    "Rolling_Mean_14"
]

TARGET = "Revenue"


def evaluate_model(name, actual, predicted):
    mae = mean_absolute_error(actual, predicted)
    rmse = np.sqrt(mean_squared_error(actual, predicted))

    # Calculate MAPE only for days with non-zero actual revenue
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


def train_models(prefix):
    print("\n" + "=" * 45)
    print(f"{prefix.upper()} MODEL TRAINING")
    print("=" * 45)

    # Load training and testing datasets
    train = pd.read_csv(f"processed/{prefix}_train.csv")
    test = pd.read_csv(f"processed/{prefix}_test.csv")

    X_train = train[FEATURES]
    y_train = train[TARGET]

    X_test = test[FEATURES]
    y_test = test[TARGET]

    results = []

    # Model 1: Naive Forecast
    naive_predictions = test["Lag_1"]

    results.append(
        evaluate_model(
            "Naive Forecast",
            y_test,
            naive_predictions
        )
    )

    # Model 2: Linear Regression
    linear_model = LinearRegression()

    linear_model.fit(X_train, y_train)

    linear_predictions = linear_model.predict(X_test)

    results.append(
        evaluate_model(
            "Linear Regression",
            y_test,
            linear_predictions
        )
    )

    # Model 3: Random Forest
    random_forest = RandomForestRegressor(
        n_estimators=200,
        max_depth=10,
        min_samples_split=5,
        random_state=42,
        n_jobs=-1
    )

    random_forest.fit(X_train, y_train)

    rf_predictions = random_forest.predict(X_test)

    results.append(
        evaluate_model(
            "Random Forest",
            y_test,
            rf_predictions
        )
    )

    # Display model comparison
    results_df = pd.DataFrame(results)

    print("\nMODEL PERFORMANCE:")
    print(results_df.round(2).to_string(index=False))

    # Save model evaluation results
    results_df.to_csv(
        f"reports/{prefix}_model_results.csv",
        index=False
    )

    # Save predictions for visualization
    predictions_df = pd.DataFrame({
        "Date": test["Date"],
        "Actual_Revenue": y_test,
        "Naive_Prediction": naive_predictions,
        "Linear_Regression": linear_predictions,
        "Random_Forest": rf_predictions
    })

    predictions_df.to_csv(
        f"reports/{prefix}_predictions.csv",
        index=False
    )

    # Identify best model using RMSE
    best_model = results_df.loc[
        results_df["RMSE"].idxmin()
    ]

    print(f"\nBest model by RMSE: {best_model['Model']}")
    print(f"Best RMSE: {best_model['RMSE']:.2f}")

    print(f"\nResults saved for {prefix} dataset.")


# Train and evaluate both datasets
train_models("baseline")
train_models("sensitivity")

print("\n" + "=" * 45)
print("MODEL TRAINING COMPLETED SUCCESSFULLY!")
print("=" * 45)
