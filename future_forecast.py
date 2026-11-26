
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

os.makedirs("reports/plots", exist_ok=True)

# Load historical daily sales
df = pd.read_csv("processed/daily_sales_baseline.csv")
df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values("Date").reset_index(drop=True)

# Historical revenue
history = df[["Date", "Revenue"]].copy()

# Forecast settings
FORECAST_DAYS = 30
LAST_DATE = history["Date"].max()

forecast_records = []

for i in range(1, FORECAST_DAYS + 1):

    future_date = LAST_DATE + pd.Timedelta(days=i)
    weekday = future_date.day_of_week

    # Get historical sales for the same weekday
    same_weekday = history[
        history["Date"].dt.day_of_week == weekday
    ].tail(8)

    # Use median to reduce the effect of unusual sales spikes
    predicted_revenue = same_weekday["Revenue"].median()

    if pd.isna(predicted_revenue):
        predicted_revenue = history["Revenue"].median()

    predicted_revenue = max(0, predicted_revenue)

    forecast_records.append({
        "Date": future_date,
        "Day": future_date.day_name(),
        "Predicted_Revenue": predicted_revenue
    })

# Create forecast dataframe
forecast_df = pd.DataFrame(forecast_records)

# Save forecast
forecast_df.to_csv(
    "reports/next_30_days_forecast.csv",
    index=False
)

# Display forecast
print("\nIMPROVED 30-DAY SALES FORECAST")
print(forecast_df.to_string(index=False))

print("\nFORECAST SUMMARY")
print(
    "Total predicted revenue: £",
    round(forecast_df["Predicted_Revenue"].sum(), 2)
)
print(
    "Average daily revenue: £",
    round(forecast_df["Predicted_Revenue"].mean(), 2)
)

# Plot forecast
plt.figure(figsize=(14, 6))

plt.plot(
    forecast_df["Date"],
    forecast_df["Predicted_Revenue"],
    marker="o",
    label="Weekday Median Forecast"
)

plt.title("Improved 30-Day Retail Sales Forecast")
plt.xlabel("Date")
plt.ylabel("Predicted Revenue (£)")
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()

plt.savefig(
    "reports/plots/next_30_days_forecast.png",
    dpi=300
)

plt.close()

print("\nForecast saved successfully!")
print("30-DAY FORECAST COMPLETED!")
