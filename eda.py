
import pandas as pd
import matplotlib.pyplot as plt
import os

# Load daily sales data
df = pd.read_csv("processed/daily_sales.csv")
df["Date"] = pd.to_datetime(df["Date"])

# Create output folder
os.makedirs("reports/plots", exist_ok=True)

# Extract date features
df["Month"] = df["Date"].dt.month_name()
df["DayOfWeek"] = df["Date"].dt.day_name()

print("=" * 60)
print("EXPLORATORY DATA ANALYSIS")
print("=" * 60)

# 1. Daily revenue trend
plt.figure(figsize=(14, 5))
plt.plot(df["Date"], df["Revenue"])
plt.title("Daily Revenue Trend")
plt.xlabel("Date")
plt.ylabel("Revenue (£)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("reports/plots/daily_revenue.png")
plt.show()

# 2. Monthly revenue
monthly = df.groupby(
    df["Date"].dt.to_period("M")
)["Revenue"].sum()

plt.figure(figsize=(12, 5))
monthly.plot(kind="bar")
plt.title("Monthly Revenue")
plt.xlabel("Month")
plt.ylabel("Revenue (£)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("reports/plots/monthly_revenue.png")
plt.show()

# 3. Weekly sales pattern
weekly = df.groupby("DayOfWeek")["Revenue"].mean()

day_order = [
    "Monday", "Tuesday", "Wednesday",
    "Thursday", "Friday", "Saturday", "Sunday"
]

weekly = weekly.reindex(day_order)

plt.figure(figsize=(10, 5))
weekly.plot(kind="bar")
plt.title("Average Revenue by Day of Week")
plt.xlabel("Day")
plt.ylabel("Average Revenue (£)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("reports/plots/weekly_pattern.png")
plt.show()

# 4. Top 10 sales days
top_days = df.nlargest(10, "Revenue")

print("\nTOP 10 SALES DAYS")
print(top_days[["Date", "Revenue"]].to_string(index=False))

# 5. Lowest 10 days with recorded sales
nonzero_days = df[df["Revenue"] > 0]
lowest_days = nonzero_days.nsmallest(10, "Revenue")

print("\nLOWEST 10 DAYS WITH RECORDED SALES")
print(lowest_days[["Date", "Revenue"]].to_string(index=False))

# 6. Monthly revenue summary
print("\nMONTHLY REVENUE SUMMARY")
print(monthly)

# 7. Zero-sales days
print("\nZERO SALES DAYS")
print("Number of zero-sales days:", (df["Revenue"] == 0).sum())

# 8. Overall statistics
print("\nOVERALL DAILY REVENUE STATISTICS")
print(df["Revenue"].describe())

print("\nEDA COMPLETED SUCCESSFULLY!")
print("Charts saved in reports/plots/")
