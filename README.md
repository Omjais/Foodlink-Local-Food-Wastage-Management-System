# 🍽️ FoodLink – Local Food Wastage Management System

## 📌 Project Overview
Food wastage is a critical issue — restaurants, hotels, and households often have surplus food, while NGOs, shelters, and individuals struggle with shortages.  

**FoodLink** is a database-driven application that connects **food providers** with **receivers**, enabling:
- Transparency in food donations  
- Reduced wastage  
- Direct coordination between providers and receivers  

The system is built with **Python, SQLite, Pandas, and Streamlit**, offering both **data analytics** and **management features**.

---

## 🚀 Features
- ✅ **SQLite Database** with 4 main tables:  
  - `providers`  
  - `receivers`  
  - `food_listings`  
  - `claims`  

- ✅ **15 Predefined SQL Queries** for insights such as:  
  - Provider/receiver distribution by city  
  - Top food contributors  
  - Claims by status  
  - Contact details of providers in a specific city  

- ✅ **Dynamic Filters**: by city, provider, food type, and meal type  
- ✅ **CRUD Operations**: Add, update, and delete records in all tables  
- ✅ **CSV Export**: Download query results for offline use  
- ✅ **Streamlit UI**: Easy-to-use web interface for managing the system  

---

## 🛠️ Tech Stack
- **Python** (3.8+)  
- **SQLite** – Lightweight relational database  
- **Pandas** – Data handling and CSV export  
- **Streamlit** – Interactive UI  

---

## 📂 Project Structure
```bash
foodlink/
│
├── data/                 # Database and CSVs
│   └── foodlink.db
│
├── notebooks/            # Jupyter/VS Code notebooks for queries
│   └── foodlink_queries.ipynb
│
├── src/                  # Scripts for data preparation and helpers
│   └── data_prep.py
│
├── app.py                # Streamlit application
├── requirements.txt      # Project dependencies
└── README.md             # Project documentation
