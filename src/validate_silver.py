
import pandas as pd
from pathlib import Path

project_path = Path(__file__).resolve().parents[1]

silver_path = project_path / "data" / "silver"
quarantine_path = project_path / "data" / "quarantine"

# Load Silver and Quarantine data
silver_df = pd.read_csv(silver_path / "orders_clean.csv")
quarantine_df = pd.read_csv(quarantine_path / "orders_rejected.csv")

print("========== SILVER LAYER VALIDATION ==========")

print("\n1. Silver Dataset Shape:")
print(silver_df.shape)

print("\n2. Duplicate Order IDs:")
print(silver_df["order_id"].duplicated().sum())

print("\n3. Negative Order Amounts:")
print((silver_df["order_amount"] < 0).sum())

print("\n4. Invalid Order Status:")
valid_status = ["Delivered", "Cancelled", "Pending"]
print((~silver_df["order_status"].isin(valid_status)).sum())

print("\n5. Missing Partner IDs:")
print(silver_df["partner_id"].isna().sum())

print("\n6. Quarantine Records:")
print(len(quarantine_df))

print("\nSILVER VALIDATION COMPLETED!")
