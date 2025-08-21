import streamlit as st
import sqlite3
import pandas as pd

DB_PATH = "../data/foodlink.db"

# Function to connect to DB
def get_connection():
    return sqlite3.connect(DB_PATH)

# All 15 queries in a dictionary
queries = {
    "1. Providers & Receivers count per city": """
        SELECT City,
               COUNT(DISTINCT Provider_ID) AS Total_Providers,
               COUNT(DISTINCT Receiver_ID) AS Total_Receivers
        FROM (
            SELECT City, Provider_ID, NULL AS Receiver_ID FROM providers
            UNION ALL
            SELECT City, NULL AS Provider_ID, Receiver_ID FROM receivers
        ) combined
        GROUP BY City
        ORDER BY City;
    """,
    "2. Provider type contributing most food": """
        SELECT Provider_Type,
               SUM(Quantity) AS Total_Quantity
        FROM food_listings
        GROUP BY Provider_Type
        ORDER BY Total_Quantity DESC;
    """,
    "3. Contact info of providers in a specific city": """
        SELECT Name, Type, Address, City, Contact
        FROM providers
        WHERE TRIM(LOWER(City)) = TRIM(LOWER(?))
        ORDER BY Name;
    """,
    "4. Receivers with most food claimed": """
        SELECT r.Name AS Receiver_Name,
               r.Type AS Receiver_Type,
               r.City,
               SUM(f.Quantity) AS Total_Quantity_Claimed
        FROM claims c
        JOIN receivers r ON c.Receiver_ID = r.Receiver_ID
        JOIN food_listings f ON c.Food_ID = f.Food_ID
        WHERE c.Status = 'Completed'
        GROUP BY r.Receiver_ID
        ORDER BY Total_Quantity_Claimed DESC;
    """,
    "5. What is the total quantity of food available from all providers?":"""
        SELECT SUM(Quantity) AS Total_Food_Quantity
        FROM food_listings; """,
    "6. Which city has the highest number of food listings?": """
        SELECT Location AS City,
        COUNT(Food_ID) AS Total_Listings
        FROM food_listings
        GROUP BY Location
        ORDER BY Total_Listings DESC;
        """,
    "7. What are the most commonly available food types?":"""
        SELECT Food_Type,
        COUNT(Food_ID) AS Total_Items
        FROM food_listings
        GROUP BY Food_Type
        ORDER BY Total_Items DESC;""",
    "8. How many food claims have been made for each food item ?"  :"""
        SELECT f.Food_Name,
        COUNT(c.Claim_ID) AS Total_Claims
        FROM claims c
        JOIN food_listings f ON c.Food_ID = f.Food_ID
        GROUP BY f.Food_Name
        ORDER BY Total_Claims DESC;""",
    "9. Which provider has had the highest number of successful food claims?" :"""
        SELECT p.Name AS Provider_Name,
        p.Type AS Provider_Type,
        COUNT(c.Claim_ID) AS Successful_Claims
        FROM claims c
        JOIN food_listings f ON c.Food_ID = f.Food_ID
        JOIN providers p ON f.Provider_ID = p.Provider_ID
        WHERE c.Status = 'Completed'
        GROUP BY p.Provider_ID
        ORDER BY Successful_Claims DESC;"""  ,
    "10. What percentage of food claims are completed vs. pending vs. canceled?": """
        SELECT Status,
        COUNT(*) AS Total_Claims,
        ROUND( (COUNT(*) * 100.0) / (SELECT COUNT(*) FROM claims), 2 ) AS Percentage
        FROM claims
        GROUP BY Status
        ORDER BY Percentage DESC;""",
    "11. What is the average quantity of food claimed per receiver?":"""
        SELECT r.Name AS Receiver_Name,
        r.Type AS Receiver_Type,
        r.City,
        ROUND(AVG(f.Quantity), 2) AS Avg_Quantity_Claimed
        FROM claims c
        JOIN receivers r ON c.Receiver_ID = r.Receiver_ID
        JOIN food_listings f ON c.Food_ID = f.Food_ID
        WHERE c.Status = 'Completed'
        GROUP BY r.Receiver_ID
        ORDER BY Avg_Quantity_Claimed DESC;""" , 
    "12. Which meal type (breakfast, lunch, dinner, snacks) is claimed the most?": """
        SELECT f.Meal_Type,
        SUM(f.Quantity) AS Total_Quantity_Claimed
        FROM claims c
        JOIN food_listings f ON c.Food_ID = f.Food_ID
        WHERE c.Status = 'Completed'
        GROUP BY f.Meal_Type
        ORDER BY Total_Quantity_Claimed DESC;
        """,
    "13. What is the total quantity of food donated by each provider?" :"""
        SELECT p.Name AS Provider_Name,
        p.Type AS Provider_Type,
        p.City,
        SUM(f.Quantity) AS Total_Quantity_Donated
        FROM food_listings f
        JOIN providers p ON f.Provider_ID = p.Provider_ID
        GROUP BY p.Provider_ID
        ORDER BY Total_Quantity_Donated DESC;""",
    "14. Find the provider(s) whose food is claimed the fastest (based on claim timestamp vs. food listing availability).":"""
        SELECT p.Name AS Provider_Name,
        ROUND( CAST(COUNT(c.Claim_ID) AS FLOAT) / COUNT(DISTINCT f.Food_ID), 2 ) AS Avg_Claims_Per_Listing
        FROM claims c
        JOIN food_listings f ON c.Food_ID = f.Food_ID
        JOIN providers p ON f.Provider_ID = p.Provider_ID
        GROUP BY p.Provider_ID
        ORDER BY Avg_Claims_Per_Listing DESC;""",
    "15. List top 5 most popular food items based on total claims quantity.":"""
        SELECT f.Food_Name,
        SUM(f.Quantity) AS Total_Quantity_Claimed
        FROM claims c
        JOIN food_listings f ON c.Food_ID = f.Food_ID
        WHERE c.Status = 'Completed'
        GROUP BY f.Food_Name
        ORDER BY Total_Quantity_Claimed DESC
        LIMIT 5;"""        
}

# Page setup
st.set_page_config(page_title="FoodLink", layout="wide")
st.title("🍽️ FoodLink - Local Food Wastage Management System")

# Sidebar navigation
menu = ["Home", "View Data", "Run SQL Queries", "CRUD Operations"]
choice = st.sidebar.selectbox("Select Page", menu)

# -----------------------
# HOME PAGE
# -----------------------
if choice == "Home":
    st.subheader("Welcome to FoodLink")
    st.write("""
        FoodLink connects surplus food providers with receivers in need, 
        reducing food wastage and helping the community.
    """)

# -----------------------
# VIEW DATA
# -----------------------
elif choice == "View Data":
    st.subheader("📋 View Tables from Database")
    tables = ["providers", "receivers", "food_listings", "claims"]
    selected_table = st.selectbox("Select Table", tables)

    conn = get_connection()
    df = pd.read_sql(f"SELECT * FROM {selected_table}", conn)
    st.dataframe(df)
    conn.close()

# -----------------------
# RUN SQL QUERIES
# -----------------------
elif choice == "Run SQL Queries":
    st.subheader("📊 Run Predefined SQL Queries")

    conn = get_connection()

    # Filters
    cities = ["All"] + pd.read_sql("SELECT DISTINCT City FROM providers", conn)["City"].tolist()
    providers_list = ["All"] + pd.read_sql("SELECT DISTINCT Name FROM providers", conn)["Name"].tolist()
    food_types = ["All"] + pd.read_sql("SELECT DISTINCT Food_Type FROM food_listings", conn)["Food_Type"].tolist()
    meal_types = ["All"] + pd.read_sql("SELECT DISTINCT Meal_Type FROM food_listings", conn)["Meal_Type"].tolist()

    col1, col2, col3, col4 = st.columns(4)
    selected_city = col1.selectbox("City", cities)
    selected_provider = col2.selectbox("Provider", providers_list)
    selected_food_type = col3.selectbox("Food Type", food_types)
    selected_meal_type = col4.selectbox("Meal Type", meal_types)

    # Choose query
    selected_query_name = st.selectbox("Choose a query", list(queries.keys()))

    # --------------------
    # Special handling for Query #3
    # --------------------
    if selected_query_name == "3. Contact info of providers in a specific city":
        if selected_city == "All":
            st.warning("Please select a city to view providers' contact details.")
            df = pd.DataFrame()
        else:
            df = pd.read_sql(queries[selected_query_name], conn, params=(selected_city,))
    else:
        # Apply filters dynamically for all other queries
        query_to_run = queries[selected_query_name]
        filter_conditions = []
        params = []

        if selected_city != "All":
            filter_conditions.append("City = ?")
            params.append(selected_city)
        if selected_provider != "All":
            filter_conditions.append("Name = ?")
            params.append(selected_provider)
        if selected_food_type != "All":
            filter_conditions.append("Food_Type = ?")
            params.append(selected_food_type)
        if selected_meal_type != "All":
            filter_conditions.append("Meal_Type = ?")
            params.append(selected_meal_type)

        if filter_conditions:
            if "WHERE" in query_to_run.upper():
                query_to_run += " AND " + " AND ".join(filter_conditions)
            else:
                query_to_run += " WHERE " + " AND ".join(filter_conditions)

        df = pd.read_sql(query_to_run, conn, params=params)

    conn.close()

    # Show results
    if not df.empty:
        st.write(f"**{len(df)} rows returned**")
        st.dataframe(df)

        # Download as CSV
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name=f"{selected_query_name}.csv",
            mime="text/csv"
        )
    else:
        st.warning("No results found for the selected filters.")


# -----------------------
# CRUD OPERATIONS
# -----------------------
elif choice == "CRUD Operations":
    st.subheader("✏️ Manage Database Records")

    crud_menu = ["Providers", "Receivers", "Food Listings", "Claims"]
    crud_choice = st.selectbox("Select Table to Manage", crud_menu)

    conn = get_connection()
    cursor = conn.cursor()

    # ---------------------------
    # PROVIDERS CRUD
    # ---------------------------
    if crud_choice == "Providers":
        st.markdown("### 📌 Manage Providers")

        # Show current providers
        df_providers = pd.read_sql("SELECT * FROM providers", conn)
        st.dataframe(df_providers)

        st.markdown("#### ➕ Add Provider")
        with st.form("add_provider_form"):
            provider_id = st.number_input("Provider ID", step=1)
            name = st.text_input("Name")
            type_ = st.text_input("Type")
            address = st.text_input("Address")
            city = st.text_input("City")
            contact = st.text_input("Contact")
            submitted = st.form_submit_button("Add Provider")
            if submitted:
                cursor.execute("""
                    INSERT INTO providers (Provider_ID, Name, Type, Address, City, Contact)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (provider_id, name, type_, address, city, contact))
                conn.commit()
                st.success("Provider added successfully!")

        st.markdown("#### 📝 Update Provider Contact")
        with st.form("update_provider_form"):
            provider_id_update = st.number_input("Provider ID to update", step=1)
            new_contact = st.text_input("New Contact")
            submitted_update = st.form_submit_button("Update Contact")
            if submitted_update:
                cursor.execute("""
                    UPDATE providers
                    SET Contact = ?
                    WHERE Provider_ID = ?
                """, (new_contact, provider_id_update))
                conn.commit()
                st.success("Provider contact updated successfully!")

        st.markdown("#### ❌ Delete Provider")
        with st.form("delete_provider_form"):
            provider_id_delete = st.number_input("Provider ID to delete", step=1)
            submitted_delete = st.form_submit_button("Delete Provider")
            if submitted_delete:
                cursor.execute("DELETE FROM providers WHERE Provider_ID = ?", (provider_id_delete,))
                conn.commit()
                st.success("Provider deleted successfully!")
    
    # ---------------------------
    # RECEIVERS CRUD
    # ---------------------------
    if crud_choice == "Receivers":
        st.markdown("### 📌 Manage Receivers")

        # Show current receivers
        df_receivers = pd.read_sql("SELECT * FROM receivers", conn)
        st.dataframe(df_receivers)

        st.markdown("#### ➕ Add Receiver")
        with st.form("add_receiver_form"):
            receiver_id = st.number_input("Receiver ID", step=1)
            name = st.text_input("Name")
            type_ = st.text_input("Type")
            address = st.text_input("Address")
            city = st.text_input("City")
            contact = st.text_input("Contact")
            submitted = st.form_submit_button("Add Receiver")
            if submitted:
                cursor.execute("""
                    INSERT INTO receivers (Receiver_ID, Name, Type, Address, City, Contact)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (receiver_id, name, type_, address, city, contact))
                conn.commit()
                st.success("Receiver added successfully!")

        st.markdown("#### 📝 Update Receiver Contact")
        with st.form("update_receiver_form"):
            receiver_id_update = st.number_input("Receiver ID to update", step=1)
            new_contact = st.text_input("New Contact")
            submitted_update = st.form_submit_button("Update Contact")
            if submitted_update:
                cursor.execute("""
                    UPDATE receivers
                    SET Contact = ?
                    WHERE Receiver_ID = ?
                """, (new_contact, receiver_id_update))
                conn.commit()
                st.success("Receiver contact updated successfully!")

        st.markdown("#### ❌ Delete Receiver")
        with st.form("delete_receiver_form"):
            receiver_id_delete = st.number_input("Receiver ID to delete", step=1)
            submitted_delete = st.form_submit_button("Delete Receiver")
            if submitted_delete:
                cursor.execute("DELETE FROM receivers WHERE Receiver_ID = ?", (receiver_id_delete,))
                conn.commit()
                st.success("Receiver deleted successfully!")
    
    # ---------------------------
    # FOOD LISTINGS CRUD
    # ---------------------------
    if crud_choice == "Food Listings":
        st.markdown("### 📌 Manage Food Listings")

        # Show current food listings
        df_food = pd.read_sql("SELECT * FROM food_listings", conn)
        st.dataframe(df_food)

        # Get provider IDs for dropdown
        provider_ids = pd.read_sql("SELECT Provider_ID FROM providers", conn)["Provider_ID"].tolist()

        st.markdown("#### ➕ Add Food Listing")
        with st.form("add_food_form"):
            food_id = st.number_input("Food ID", step=1)
            provider_id = st.selectbox("Provider ID", provider_ids)
            food_name = st.text_input("Food Name")
            food_type = st.text_input("Food Type (e.g., Vegetarian, Non-Vegetarian, Vegan)")
            meal_type = st.text_input("Meal Type (e.g., Breakfast, Lunch, Dinner, Snacks)")
            quantity = st.number_input("Quantity", step=1)
            location = st.text_input("Location (City)")
            submitted = st.form_submit_button("Add Food Listing")
            if submitted:
                cursor.execute("""
                    INSERT INTO food_listings (Food_ID, Provider_ID, Food_Name, Food_Type, Meal_Type, Quantity, Location)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (food_id, provider_id, food_name, food_type, meal_type, quantity, location))
                conn.commit()
                st.success("Food listing added successfully!")

        st.markdown("#### 📝 Update Food Quantity")
        with st.form("update_food_form"):
            food_id_update = st.number_input("Food ID to update", step=1)
            new_quantity = st.number_input("New Quantity", step=1)
            submitted_update = st.form_submit_button("Update Quantity")
            if submitted_update:
                cursor.execute("""
                    UPDATE food_listings
                    SET Quantity = ?
                    WHERE Food_ID = ?
                """, (new_quantity, food_id_update))
                conn.commit()
                st.success("Food quantity updated successfully!")

        st.markdown("#### ❌ Delete Food Listing")
        with st.form("delete_food_form"):
            food_id_delete = st.number_input("Food ID to delete", step=1)
            submitted_delete = st.form_submit_button("Delete Food Listing")
            if submitted_delete:
                cursor.execute("DELETE FROM food_listings WHERE Food_ID = ?", (food_id_delete,))
                conn.commit()
                st.success("Food listing deleted successfully!")
    
    # ---------------------------
    # CLAIMS CRUD
    # ---------------------------
    if crud_choice == "Claims":
        st.markdown("### 📌 Manage Claims")

        # Show current claims
        df_claims = pd.read_sql("SELECT * FROM claims", conn)
        st.dataframe(df_claims)

        # Get food IDs and receiver IDs for dropdowns
        food_ids = pd.read_sql("SELECT Food_ID FROM food_listings", conn)["Food_ID"].tolist()
        receiver_ids = pd.read_sql("SELECT Receiver_ID FROM receivers", conn)["Receiver_ID"].tolist()

        st.markdown("#### ➕ Add Claim")
        with st.form("add_claim_form"):
            claim_id = st.number_input("Claim ID", step=1)
            food_id = st.selectbox("Food ID", food_ids)
            receiver_id = st.selectbox("Receiver ID", receiver_ids)
            status = st.selectbox("Status", ["Pending", "Completed", "Cancelled"])
            submitted = st.form_submit_button("Add Claim")
            if submitted:
                cursor.execute("""
                    INSERT INTO claims (Claim_ID, Food_ID, Receiver_ID, Status)
                    VALUES (?, ?, ?, ?)
                """, (claim_id, food_id, receiver_id, status))
                conn.commit()
                st.success("Claim added successfully!")

        st.markdown("#### 📝 Update Claim Status")
        with st.form("update_claim_form"):
            claim_id_update = st.number_input("Claim ID to update", step=1)
            new_status = st.selectbox("New Status", ["Pending", "Completed", "Cancelled"])
            submitted_update = st.form_submit_button("Update Status")
            if submitted_update:
                cursor.execute("""
                    UPDATE claims
                    SET Status = ?
                    WHERE Claim_ID = ?
                """, (new_status, claim_id_update))
                conn.commit()
                st.success("Claim status updated successfully!")

        st.markdown("#### ❌ Delete Claim")
        with st.form("delete_claim_form"):
            claim_id_delete = st.number_input("Claim ID to delete", step=1)
            submitted_delete = st.form_submit_button("Delete Claim")
            if submitted_delete:
                cursor.execute("DELETE FROM claims WHERE Claim_ID = ?", (claim_id_delete,))
                conn.commit()
                st.success("Claim deleted successfully!")

    conn.close()
