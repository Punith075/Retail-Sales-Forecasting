
import pandas as pd

# Load daily sales
df = pd.read_csv("processed/daily_sales.csv")
df["Date"] = pd.to_datetime(df["Date"])

print("=" * 65)
print("ADVANCED SALES AND SEASONALITY ANALYSIS")
print("=" * 65)

# 1. Top 10 revenue days
print("\n1. TOP 10 REVENUE DAYS")

top_days = df.nlargest(10, "Revenue")

print(
    top_days[["Date", "Revenue", "Transactions"]]
    .to_string(index=False)
)

# 2. Monthly revenue and transaction summary
print("\n2. MONTHLY PERFORMANCE")

df["Month"] = df["Date"].dt.to_period("M")

monthly = df.groupby("Month").agg(
    Revenue=("Revenue", "sum"),
    Transactions=("Transactions", "sum"),
    ItemsSold=("ItemsSold", "sum"),
    TradingDays=("Revenue", lambda x: (x > 0).sum())
)

print(monthly.round(2).to_string())

# 3. Weekday analysis
print("\n3. WEEKDAY PERFORMANCE")

df["Day"] = df["Date"].dt.day_name()

weekday = df.groupby("Day").agg(
    AverageRevenue=("Revenue", "mean"),
    TradingDayAverage=(
        "Revenue",
        lambda x: x[x > 0].mean()
    ),
    TradingDays=("Revenue", lambda x: (x > 0).sum()),
    TotalRevenue=("Revenue", "sum")
)

day_order = [
    "Monday", "Tuesday", "Wednesday",
    "Thursday", "Friday", "Saturday", "Sunday"
]

weekday = weekday.reindex(day_order)

print(weekday.round(2).to_string())

# 4. Zero revenue investigation
print("\n4. ZERO REVENUE DAYS")

zero_days = df[df["Revenue"] == 0]

print("Total zero revenue days:", len(zero_days))
print("Dates:")
print(zero_days["Date"].dt.strftime("%Y-%m-%d").to_list())

# 5. Overall performance
print("\n5. OVERALL PERFORMANCE")

print("Total revenue:", round(df["Revenue"].sum(), 2))
print("Average daily revenue:", round(df["Revenue"].mean(), 2))
print("Average trading-day revenue:",
      round(df.loc[df["Revenue"] > 0, "Revenue"].mean(), 2))

print("\nANALYSIS COMPLETED")
