
import pandas as pd
from pathlib import Path

# Project paths
project_path = Path(__file__).resolve().parents[1]
bronze_path = project_path / "data" / "bronze"

# Read orders data
df = pd.read_csv(bronze_path / "orders.csv")

print("========== DATA QUALITY REPORT ==========")

# 1. Dataset information
print("\n1. Dataset Shape:")
print(df.shape)

# 2. Missing values
print("\n2. Missing Values:")
print(df.isnull().sum())

# 3. Duplicate records
print("\n3. Duplicate Records:")
print(df.duplicated().sum())

# 4. Duplicate Order IDs
print("\n4. Duplicate Order IDs:")
print(df["order_id"].duplicated().sum())

# 5. Negative order amounts
print("\n5. Negative Order Amounts:")
print((df["order_amount"] < 0).sum())

# 6. Invalid order statuses
valid_status = ["Delivered", "Cancelled", "Pending"]

print("\n6. Invalid Order Status:")
print((~df["order_status"].isin(valid_status)).sum())

# 7. Data types
print("\n7. Data Types:")
print(df.dtypes)

print("\n========== VALIDATION COMPLETED ==========")
