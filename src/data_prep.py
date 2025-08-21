"""
data_prep.py
Step 2: Load CSV files, clean data, and create SQLite database.
"""

import os
import pandas as pd
import sqlite3

# 1. Paths to your CSV files
DATA_DIR = "data/"
PROVIDERS_CSV = os.path.join(DATA_DIR, "providers_data.csv")
RECEIVERS_CSV = os.path.join(DATA_DIR, "receivers_data.csv")
FOOD_LISTINGS_CSV = os.path.join(DATA_DIR, "food_listings_data.csv")
CLAIMS_CSV = os.path.join(DATA_DIR, "claims_data.csv")

# 2. Path to SQLite database
DB_PATH = os.path.join(DATA_DIR, "foodlink.db")

# 3. Function to load CSV
def load_csv(file_path):
    """Load a CSV file into a pandas DataFrame."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    df = pd.read_csv(file_path)
    print(f"Loaded {file_path} with {len(df)} rows")
    return df

# 4. Load data
providers_df = load_csv(PROVIDERS_CSV)
receivers_df = load_csv(RECEIVERS_CSV)
food_listings_df = load_csv(FOOD_LISTINGS_CSV)
claims_df = load_csv(CLAIMS_CSV)

# 5. Basic cleaning examples
providers_df.drop_duplicates(subset=["Provider_ID"], inplace=True)
receivers_df.drop_duplicates(subset=["Receiver_ID"], inplace=True)
food_listings_df.drop_duplicates(subset=["Food_ID"], inplace=True)
claims_df.drop_duplicates(subset=["Claim_ID"], inplace=True)

# Optional: Convert date columns
food_listings_df["Expiry_Date"] = pd.to_datetime(food_listings_df["Expiry_Date"], errors="coerce")
claims_df["Timestamp"] = pd.to_datetime(claims_df["Timestamp"], errors="coerce")

# 6. Create SQLite database and tables
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS providers (
    Provider_ID INTEGER PRIMARY KEY,
    Name TEXT,
    Type TEXT,
    Address TEXT,
    City TEXT,
    Contact TEXT
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS receivers (
    Receiver_ID INTEGER PRIMARY KEY,
    Name TEXT,
    Type TEXT,
    City TEXT,
    Contact TEXT
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS food_listings (
    Food_ID INTEGER PRIMARY KEY,
    Food_Name TEXT,
    Quantity INTEGER,
    Expiry_Date TEXT,
    Provider_ID INTEGER,
    Provider_Type TEXT,
    Location TEXT,
    Food_Type TEXT,
    Meal_Type TEXT,
    FOREIGN KEY (Provider_ID) REFERENCES providers (Provider_ID)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS claims (
    Claim_ID INTEGER PRIMARY KEY,
    Food_ID INTEGER,
    Receiver_ID INTEGER,
    Status TEXT,
    Timestamp TEXT,
    FOREIGN KEY (Food_ID) REFERENCES food_listings (Food_ID),
    FOREIGN KEY (Receiver_ID) REFERENCES receivers (Receiver_ID)
);
""")

# 7. Insert data into tables
providers_df.to_sql("providers", conn, if_exists="replace", index=False)
receivers_df.to_sql("receivers", conn, if_exists="replace", index=False)
food_listings_df.to_sql("food_listings", conn, if_exists="replace", index=False)
claims_df.to_sql("claims", conn, if_exists="replace", index=False)

conn.commit()
conn.close()

print(f"Database created at {DB_PATH}")
