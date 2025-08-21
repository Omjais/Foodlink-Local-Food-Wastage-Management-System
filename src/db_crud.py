"""
db_crud.py
Contains CRUD operations for the FoodLink database (SQLite)
"""

import sqlite3
import pandas as pd

DB_PATH = """"
db_crud.py
Contains CRUD operations for the FoodLink database (SQLite)
"""

import sqlite3
import pandas as pd

DB_PATH = "C:/Users/omj48/OneDrive/Desktop/Labmentix projects/foodlink/data/foodlink.db"

# Utility function to connect to the database
def get_connection():
    return sqlite3.connect(DB_PATH)

# -------------------------
# PROVIDERS CRUD
# -------------------------
def add_provider(provider_id, name, type_, address, city, contact):
    conn = get_connection()
    conn.execute("""
        INSERT INTO providers (Provider_ID, Name, Type, Address, City, Contact)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (provider_id, name, type_, address, city, contact))
    conn.commit()
    conn.close()

def get_all_providers():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM providers", conn)
    conn.close()
    return df

def update_provider_contact(provider_id, new_contact):
    conn = get_connection()
    conn.execute("""
        UPDATE providers
        SET Contact = ?
        WHERE Provider_ID = ?
    """, (new_contact, provider_id))
    conn.commit()
    conn.close()

def delete_provider(provider_id):
    conn = get_connection()
    conn.execute("DELETE FROM providers WHERE Provider_ID = ?", (provider_id,))
    conn.commit()
    conn.close()

# -------------------------
# RECEIVERS CRUD
# -------------------------
def add_receiver(receiver_id, name, type_, city, contact):
    conn = get_connection()
    conn.execute("""
        INSERT INTO receivers (Receiver_ID, Name, Type, City, Contact)
        VALUES (?, ?, ?, ?, ?)
    """, (receiver_id, name, type_, city, contact))
    conn.commit()
    conn.close()

def get_all_receivers():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM receivers", conn)
    conn.close()
    return df

def update_receiver_contact(receiver_id, new_contact):
    conn = get_connection()
    conn.execute("""
        UPDATE receivers
        SET Contact = ?
        WHERE Receiver_ID = ?
    """, (new_contact, receiver_id))
    conn.commit()
    conn.close()

def delete_receiver(receiver_id):
    conn = get_connection()
    conn.execute("DELETE FROM receivers WHERE Receiver_ID = ?", (receiver_id,))
    conn.commit()
    conn.close()

# -------------------------
# FOOD LISTINGS CRUD
# -------------------------
def add_food(food_id, name, quantity, expiry_date, provider_id, provider_type, location, food_type, meal_type):
    conn = get_connection()
    conn.execute("""
        INSERT INTO food_listings 
        (Food_ID, Food_Name, Quantity, Expiry_Date, Provider_ID, Provider_Type, Location, Food_Type, Meal_Type)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (food_id, name, quantity, expiry_date, provider_id, provider_type, location, food_type, meal_type))
    conn.commit()
    conn.close()

def get_all_food():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM food_listings", conn)
    conn.close()
    return df

def update_food_quantity(food_id, new_quantity):
    conn = get_connection()
    conn.execute("""
        UPDATE food_listings
        SET Quantity = ?
        WHERE Food_ID = ?
    """, (new_quantity, food_id))
    conn.commit()
    conn.close()

def delete_food(food_id):
    conn = get_connection()
    conn.execute("DELETE FROM food_listings WHERE Food_ID = ?", (food_id,))
    conn.commit()
    conn.close()

# -------------------------
# CLAIMS CRUD
# -------------------------
def add_claim(claim_id, food_id, receiver_id, status, timestamp):
    conn = get_connection()
    conn.execute("""
        INSERT INTO claims (Claim_ID, Food_ID, Receiver_ID, Status, Timestamp)
        VALUES (?, ?, ?, ?, ?)
    """, (claim_id, food_id, receiver_id, status, timestamp))
    conn.commit()
    conn.close()

def get_all_claims():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM claims", conn)
    conn.close()
    return df

def update_claim_status(claim_id, new_status):
    conn = get_connection()
    conn.execute("""
        UPDATE claims
        SET Status = ?
        WHERE Claim_ID = ?
    """, (new_status, claim_id))
    conn.commit()
    conn.close()

def delete_claim(claim_id):
    conn = get_connection()
    conn.execute("DELETE FROM claims WHERE Claim_ID = ?", (claim_id,))
    conn.commit()
    conn.close()


# Utility function to connect to the database
def get_connection():
    return sqlite3.connect(DB_PATH)

# -------------------------
# PROVIDERS CRUD
# -------------------------
def add_provider(provider_id, name, type_, address, city, contact):
    conn = get_connection()
    conn.execute("""
        INSERT INTO providers (Provider_ID, Name, Type, Address, City, Contact)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (provider_id, name, type_, address, city, contact))
    conn.commit()
    conn.close()

def get_all_providers():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM providers", conn)
    conn.close()
    return df

def update_provider_contact(provider_id, new_contact):
    conn = get_connection()
    conn.execute("""
        UPDATE providers
        SET Contact = ?
        WHERE Provider_ID = ?
    """, (new_contact, provider_id))
    conn.commit()
    conn.close()

def delete_provider(provider_id):
    conn = get_connection()
    conn.execute("DELETE FROM providers WHERE Provider_ID = ?", (provider_id,))
    conn.commit()
    conn.close()

# -------------------------
# RECEIVERS CRUD
# -------------------------
def add_receiver(receiver_id, name, type_, city, contact):
    conn = get_connection()
    conn.execute("""
        INSERT INTO receivers (Receiver_ID, Name, Type, City, Contact)
        VALUES (?, ?, ?, ?, ?)
    """, (receiver_id, name, type_, city, contact))
    conn.commit()
    conn.close()

def get_all_receivers():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM receivers", conn)
    conn.close()
    return df

def update_receiver_contact(receiver_id, new_contact):
    conn = get_connection()
    conn.execute("""
        UPDATE receivers
        SET Contact = ?
        WHERE Receiver_ID = ?
    """, (new_contact, receiver_id))
    conn.commit()
    conn.close()

def delete_receiver(receiver_id):
    conn = get_connection()
    conn.execute("DELETE FROM receivers WHERE Receiver_ID = ?", (receiver_id,))
    conn.commit()
    conn.close()

# -------------------------
# FOOD LISTINGS CRUD
# -------------------------
def add_food(food_id, name, quantity, expiry_date, provider_id, provider_type, location, food_type, meal_type):
    conn = get_connection()
    conn.execute("""
        INSERT INTO food_listings 
        (Food_ID, Food_Name, Quantity, Expiry_Date, Provider_ID, Provider_Type, Location, Food_Type, Meal_Type)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (food_id, name, quantity, expiry_date, provider_id, provider_type, location, food_type, meal_type))
    conn.commit()
    conn.close()

def get_all_food():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM food_listings", conn)
    conn.close()
    return df

def update_food_quantity(food_id, new_quantity):
    conn = get_connection()
    conn.execute("""
        UPDATE food_listings
        SET Quantity = ?
        WHERE Food_ID = ?
    """, (new_quantity, food_id))
    conn.commit()
    conn.close()

def delete_food(food_id):
    conn = get_connection()
    conn.execute("DELETE FROM food_listings WHERE Food_ID = ?", (food_id,))
    conn.commit()
    conn.close()

# -------------------------
# CLAIMS CRUD
# -------------------------
def add_claim(claim_id, food_id, receiver_id, status, timestamp):
    conn = get_connection()
    conn.execute("""
        INSERT INTO claims (Claim_ID, Food_ID, Receiver_ID, Status, Timestamp)
        VALUES (?, ?, ?, ?, ?)
    """, (claim_id, food_id, receiver_id, status, timestamp))
    conn.commit()
    conn.close()

def get_all_claims():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM claims", conn)
    conn.close()
    return df

def update_claim_status(claim_id, new_status):
    conn = get_connection()
    conn.execute("""
        UPDATE claims
        SET Status = ?
        WHERE Claim_ID = ?
    """, (new_status, claim_id))
    conn.commit()
    conn.close()

def delete_claim(claim_id):
    conn = get_connection()
    conn.execute("DELETE FROM claims WHERE Claim_ID = ?", (claim_id,))
    conn.commit()
    conn.close()
