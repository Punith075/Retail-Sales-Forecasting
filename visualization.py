
import pandas as pd
import matplotlib.pyplot as plt
import os

os.makedirs("reports/plots", exist_ok=True)


def create_visualizations(prefix):
    print(f"\nCreating visualizations for {prefix.upper()} dataset...")

    # Load predictions
    df = pd.read_csv(f"reports/{prefix}_predictions.csv")
    df["Date"] = pd.to_datetime(df["Date"])

    # 1. Actual vs Predicted Revenue
    plt.figure(figsize=(14, 6))

    plt.plot(
        df["Date"],
        df["Actual_Revenue"],
        label="Actual Revenue",
        linewidth=2
    )

    plt.plot(
        df["Date"],
        df["Naive_Prediction"],
        label="Naive Forecast",
        alpha=0.8
    )

    plt.plot(
        df["Date"],
        df["Linear_Regression"],
        label="Linear Regression",
        alpha=0.8
    )

    plt.plot(
        df["Date"],
        df["Random_Forest"],
        label="Random Forest",
        linewidth=2
    )

    plt.title(f"Actual vs Predicted Daily Revenue - {prefix.title()}")
    plt.xlabel("Date")
    plt.ylabel("Revenue (£)")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.savefig(
        f"reports/plots/{prefix}_actual_vs_predicted.png",
        dpi=300
    )
    plt.close()

    # 2. Actual vs Random Forest
    plt.figure(figsize=(14, 6))

    plt.plot(
        df["Date"],
        df["Actual_Revenue"],
        label="Actual Revenue",
        linewidth=2
    )

    plt.plot(
        df["Date"],
        df["Random_Forest"],
        label="Random Forest Prediction",
        linewidth=2
    )

    plt.title(f"Random Forest Forecast vs Actual Revenue - {prefix.title()}")
    plt.xlabel("Date")
    plt.ylabel("Revenue (£)")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.savefig(
        f"reports/plots/{prefix}_random_forest_comparison.png",
        dpi=300
    )
    plt.close()

    print("Visualizations saved successfully.")


# Generate graphs for both datasets
create_visualizations("baseline")
create_visualizations("sensitivity")

print("\nALL VISUALIZATIONS COMPLETED!")


# 3. Model Performance Comparison
baseline = pd.read_csv("reports/baseline_model_results.csv")
sensitivity = pd.read_csv("reports/sensitivity_model_results.csv")

metrics = ["MAE", "RMSE"]

for metric in metrics:
    comparison = pd.DataFrame({
        "Model": baseline["Model"],
        "Baseline": baseline[metric],
        "Sensitivity": sensitivity[metric]
    })

    comparison.set_index("Model").plot(
        kind="bar",
        figsize=(10, 6)
    )

    plt.title(f"{metric} Comparison: Baseline vs Sensitivity")
    plt.ylabel(f"{metric} (£)")
    plt.xticks(rotation=0)
    plt.tight_layout()

    plt.savefig(
        f"reports/plots/{metric.lower()}_comparison.png",
        dpi=300
    )
    plt.close()

print("Model performance comparison graphs saved!")
