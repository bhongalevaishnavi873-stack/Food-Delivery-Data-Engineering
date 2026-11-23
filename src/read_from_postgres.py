
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(
    "postgresql+psycopg2://postgres:root1@localhost:5432/food_delivery_dw"
)

query = """
SELECT
    city,
    total_orders,
    total_revenue
FROM city_wise_sales
ORDER BY total_revenue DESC;
"""

df = pd.read_sql(query, engine)

print("========== POSTGRESQL DATA ==========")
print(df)

print("\nTotal Cities:", len(df))
print("\nData Successfully Retrieved!")
