
import pandas as pd
from pathlib import Path

project_path = Path(__file__).resolve().parents[1]

silver_path = project_path / "data" / "silver"
gold_path = project_path / "data" / "gold"

gold_path.mkdir(parents=True, exist_ok=True)

# Load cleaned orders
df = pd.read_csv(silver_path / "orders_clean.csv")

df["order_date"] = pd.to_datetime(df["order_date"])

# 1. Daily Sales
daily_sales = df.groupby(
    df["order_date"].dt.date
).agg(
    total_orders=("order_id", "count"),
    total_revenue=("order_amount", "sum"),
    average_order_value=("order_amount", "mean")
).reset_index()



daily_sales.to_csv(gold_path / "daily_sales.csv", index=False)

# 2. City Wise Sales
customers = pd.read_csv(
    project_path / "data" / "bronze" / "customers.csv"
)

city_orders = df.merge(
    customers[["customer_id", "city"]],
    on="customer_id",
    how="left"
)

city_wise_sales = city_orders.groupby("city").agg(
    total_orders=("order_id", "count"),
    total_revenue=("order_amount", "sum")
).reset_index()

city_wise_sales.to_csv(
    gold_path / "city_wise_sales.csv", index=False
)

# 3. Order Status Summary
status_summary = df.groupby("order_status").agg(
    total_orders=("order_id", "count"),
    total_revenue=("order_amount", "sum")
).reset_index()

status_summary.to_csv(
    gold_path / "order_status_summary.csv", index=False
)

print("========== GOLD LAYER CREATED ==========")
print("Daily Sales:", len(daily_sales), "records")
print("City Wise Sales:", len(city_wise_sales), "records")
print("Order Status Summary:", len(status_summary), "records")
print("\nGold Layer Files Created Successfully!")
