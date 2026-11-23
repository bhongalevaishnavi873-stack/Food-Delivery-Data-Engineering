
import pandas as pd
from pathlib import Path

# 1. Project paths
project_path = Path(__file__).resolve().parents[1]

bronze_path = project_path / "data" / "bronze"
silver_path = project_path / "data" / "silver"
quarantine_path = project_path / "data" / "quarantine"

# Create folders
silver_path.mkdir(parents=True, exist_ok=True)
quarantine_path.mkdir(parents=True, exist_ok=True)

# 2. Read Bronze data
df = pd.read_csv(bronze_path / "orders.csv")

print("Original Records:", len(df))

# 3. Remove duplicate Order IDs
before_duplicates = len(df)

df = df.drop_duplicates(
    subset=["order_id"],
    keep="first"
)

duplicates_removed = before_duplicates - len(df)

print("Duplicates Removed:", duplicates_removed)

# 4. Standardize Order Status
df["order_status"] = (
    df["order_status"]
    .str.strip()
    .str.title()
)

# 5. Convert data types
df["order_date"] = pd.to_datetime(
    df["order_date"],
    errors="coerce"
)

df["ingestion_timestamp"] = pd.to_datetime(
    df["ingestion_timestamp"],
    errors="coerce",
    utc=True
)

df["order_amount"] = pd.to_numeric(
    df["order_amount"],
    errors="coerce"
)

df["partner_id"] = pd.to_numeric(
    df["partner_id"],
    errors="coerce"
).astype("Int64")

# 6. Identify invalid records
valid_status = ["Delivered", "Cancelled", "Pending"]

negative_amount = df["order_amount"] < 0

invalid_amount = df["order_amount"].isna()

invalid_status = ~df["order_status"].isin(valid_status)

invalid_date = df["order_date"].isna()

# 7. Create rejection reasons
reasons = []

for index, row in df.iterrows():

    row_reasons = []

    if pd.isna(row["order_amount"]) or row["order_amount"] < 0:
        row_reasons.append("Invalid order amount")

    if row["order_status"] not in valid_status:
        row_reasons.append("Invalid order status")

    if pd.isna(row["order_date"]):
        row_reasons.append("Invalid order date")

    reasons.append(", ".join(row_reasons))

df["rejection_reason"] = reasons

# 8. Separate rejected records
reject_mask = (
    negative_amount |
    invalid_amount |
    invalid_status |
    invalid_date
)

rejected_df = df[reject_mask].copy()

clean_df = df[~reject_mask].copy()

# 9. Remove temporary rejection column
clean_df = clean_df.drop(columns=["rejection_reason"])

# 10. Save Silver data
clean_df.to_csv(
    silver_path / "orders_clean.csv",
    index=False
)

# 11. Save rejected data
rejected_df.to_csv(
    quarantine_path / "orders_rejected.csv",
    index=False
)

# 12. Final report
print("\n========== CLEANING REPORT ==========")

print("Original Records:", before_duplicates)
print("Duplicates Removed:", duplicates_removed)
print("Clean Records:", len(clean_df))
print("Rejected Records:", len(rejected_df))
print("Missing Partner IDs Retained:",
      clean_df["partner_id"].isna().sum())

print("\nFinal Files Created:")
print("Silver: orders_clean.csv")
print("Quarantine: orders_rejected.csv")

print("\nDATA CLEANING COMPLETED SUCCESSFULLY!")
