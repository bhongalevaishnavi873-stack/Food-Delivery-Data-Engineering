
import pandas as pd
from pathlib import Path

project_path = Path(__file__).resolve().parents[1]
gold_path = project_path / "data" / "gold"

daily = pd.read_csv(gold_path / "daily_sales.csv")
city = pd.read_csv(gold_path / "city_wise_sales.csv")
status = pd.read_csv(gold_path / "order_status_summary.csv")

print("========== GOLD DATA VALIDATION ==========")

print("\n1. Daily Sales Records:", len(daily))
print("2. City Wise Sales Records:", len(city))
print("3. Order Status Records:", len(status))

print("\n4. Missing Values:")
print("Daily Sales:", daily.isnull().sum().sum())
print("City Sales:", city.isnull().sum().sum())
print("Status Summary:", status.isnull().sum().sum())

print("\n5. Total Orders in Gold:")
print("Daily:", daily["total_orders"].sum())
print("City:", city["total_orders"].sum())
print("Status:", status["total_orders"].sum())

print("\n6. Total Revenue:")
print("Daily:", round(daily["total_revenue"].sum(), 2))
print("City:", round(city["total_revenue"].sum(), 2))
print("Status:", round(status["total_revenue"].sum(), 2))

print("\nGOLD VALIDATION COMPLETED!")
