
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(
    "postgresql+psycopg2://postgres:root1@localhost:5432/food_delivery_dw"
)

query = "SELECT * FROM city_wise_sales"

df = pd.read_sql(query, engine)

print("========== CITY SALES ANALYSIS ==========")

print("\nCity Wise Data:")
print(df)

print("\nHighest Revenue City:")
print(df.loc[df["total_revenue"].idxmax()])

print("\nTotal Revenue:")
print(round(df["total_revenue"].sum(), 2))

print("\nTotal Orders:")
print(df["total_orders"].sum())

print("\nANALYSIS COMPLETED!")
