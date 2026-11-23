
import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine

project_path = Path(__file__).resolve().parents[1]
gold_path = project_path / "data" / "gold"

# PostgreSQL connection
engine = create_engine(
    "postgresql+psycopg2://postgres:root1@localhost:5432/food_delivery_dw"
)

# Load CSV files
daily = pd.read_csv(gold_path / "daily_sales.csv")
city = pd.read_csv(gold_path / "city_wise_sales.csv")
status = pd.read_csv(gold_path / "order_status_summary.csv")

# Insert data into PostgreSQL
daily.to_sql("daily_sales", engine, if_exists="append", index=False)
city.to_sql("city_wise_sales", engine, if_exists="append", index=False)
status.to_sql("order_status_summary", engine, if_exists="append", index=False)

print("========== POSTGRESQL LOAD REPORT ==========")
print("Daily Sales Loaded:", len(daily))
print("City Wise Sales Loaded:", len(city))
print("Order Status Loaded:", len(status))
print("DATA SUCCESSFULLY LOADED INTO POSTGRESQL!")
