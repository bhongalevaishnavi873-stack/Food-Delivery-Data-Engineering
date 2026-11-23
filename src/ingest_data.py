
import pandas as pd
import logging
from pathlib import Path
from datetime import datetime, timezone

# 1. Project paths
project_path = Path(__file__).resolve().parents[1]

raw_path = project_path / "data" / "raw"
bronze_path = project_path / "data" / "bronze"
logs_path = project_path / "logs"

# Create folders if they don't exist
bronze_path.mkdir(parents=True, exist_ok=True)
logs_path.mkdir(parents=True, exist_ok=True)

# 2. Configure logging
logging.basicConfig(
    filename=logs_path / "ingestion.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# 3. List of source files
source_files = [
    "customers.csv",
    "restaurants.csv",
    "delivery_partners.csv",
    "orders.csv",
    "payments.csv"
]

# 4. Data ingestion function
def ingest_data(file_name):

    source_file = raw_path / file_name
    destination_file = bronze_path / file_name

    try:
        # Check source file
        if not source_file.exists():
            raise FileNotFoundError(
                f"Source file not found: {source_file}"
            )

        # Read raw data
        df = pd.read_csv(source_file)

        # Add ingestion timestamp
        df["ingestion_timestamp"] = datetime.now(
            timezone.utc
        ).isoformat()

        # Save data in Bronze layer
        df.to_csv(destination_file, index=False)

        # Log success
        logging.info(
            f"Successfully ingested {file_name}, "
            f"Rows: {len(df)}"
        )

        print(
            f"SUCCESS: {file_name} | Rows: {len(df)}"
        )

        return len(df)

    except Exception as error:

        logging.error(
            f"Failed to ingest {file_name}: {error}"
        )

        print(f"FAILED: {file_name} | Error: {error}")

        return None


# 5. Execute pipeline
print("Starting Food Delivery Data Ingestion Pipeline\n")

total_rows = 0

for file_name in source_files:

    rows = ingest_data(file_name)

    if rows is not None:
        total_rows += rows

print("\n--------------------------------")
print("INGESTION PIPELINE COMPLETED")
print("Total Records Ingested:", total_rows)
print("--------------------------------")
