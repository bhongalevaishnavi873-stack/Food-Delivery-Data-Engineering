
import pandas as pd
import numpy as np
import random
from pathlib import Path

# Random data reproducible ठेवण्यासाठी
random.seed(42)
np.random.seed(42)

# Project folder path
project_path = Path(__file__).resolve().parents[1]
raw_path = project_path / "data" / "raw"
raw_path.mkdir(parents=True, exist_ok=True)

# 1. CUSTOMERS DATA
customers = pd.DataFrame({
    "customer_id": range(1, 301),
    "customer_name": [
        f"Customer_{i}" for i in range(1, 301)
    ],
    "city": np.random.choice(
        ["Pune", "Mumbai", "Nashik", "Indore", "Nagpur"],
        300
    ),
    "email": [
        f"customer{i}@gmail.com" for i in range(1, 301)
    ]
})

# 2. RESTAURANTS DATA
restaurants = pd.DataFrame({
    "restaurant_id": range(1, 51),
    "restaurant_name": [
        f"Restaurant_{i}" for i in range(1, 51)
    ],
    "city": np.random.choice(
        ["Pune", "Mumbai", "Nashik", "Indore", "Nagpur"],
        50
    ),
    "cuisine": np.random.choice(
        ["Indian", "Chinese", "Italian", "Fast Food"],
        50
    )
})

# 3. DELIVERY PARTNERS DATA
partners = pd.DataFrame({
    "partner_id": range(1, 101),
    "partner_name": [
        f"Partner_{i}" for i in range(1, 101)
    ],
    "rating": np.round(
        np.random.uniform(2.5, 5.0, 100), 1
    )
})

# 4. ORDERS DATA
n = 1500

orders = pd.DataFrame({
    "order_id": range(1001, 1001 + n),
    "customer_id": np.random.randint(1, 301, n),
    "restaurant_id": np.random.randint(1, 51, n),
    "partner_id": np.random.randint(1, 101, n),
    "order_amount": np.round(
        np.random.uniform(100, 2000, n), 2
    ),
    "order_status": np.random.choice(
        ["Delivered", "Cancelled", "Pending"],
        n,
        p=[0.75, 0.15, 0.10]
    ),
    "order_date": (
        pd.Timestamp("2026-01-01")
        + pd.to_timedelta(
            np.random.randint(0, 300, n), unit="D"
        )
    )
})

# 5. PAYMENTS DATA
payments = pd.DataFrame({
    "payment_id": range(5001, 5001 + n),
    "order_id": orders["order_id"],
    "payment_mode": np.random.choice(
        ["UPI", "Credit Card", "Debit Card", "Cash"],
        n
    ),
    "payment_amount": orders["order_amount"],
    "payment_status": np.random.choice(
        ["Success", "Failed"],
        n,
        p=[0.95, 0.05]
    )
})

# Introduce some realistic data quality issues
# Duplicate order records
orders = pd.concat(
    [orders, orders.sample(5, random_state=42)],
    ignore_index=True
)

# Negative order amounts
orders.loc[0:2, "order_amount"] = -100

# Missing delivery partner IDs
orders.loc[10:19, "partner_id"] = np.nan

# Inconsistent status values
orders.loc[20:24, "order_status"] = "delivered"

# Save all datasets as CSV files
customers.to_csv(raw_path / "customers.csv", index=False)
restaurants.to_csv(raw_path / "restaurants.csv", index=False)
partners.to_csv(raw_path / "delivery_partners.csv", index=False)
orders.to_csv(raw_path / "orders.csv", index=False)
payments.to_csv(raw_path / "payments.csv", index=False)

print("All datasets generated successfully!")

print("\nDataset Summary:")
print("Customers:", customers.shape)
print("Restaurants:", restaurants.shape)
print("Delivery Partners:", partners.shape)
print("Orders:", orders.shape)
print("Payments:", payments.shape)

print("\nFiles saved at:", raw_path)
