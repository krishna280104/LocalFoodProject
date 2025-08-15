import streamlit as st
import pandas as pd
import sqlite3

# Page title
st.title("🍽️ Local Food Wastage Management System")
st.write("Connect surplus food providers with receivers to reduce waste.")

# Connect to database
conn = sqlite3.connect("food_wastage.db")

# --- Load providers data ---
providers_df = pd.read_sql("SELECT * FROM providers", conn)

# --- City filter ---
cities = providers_df['City'].dropna().unique()
selected_city = st.selectbox("Select a city to view providers:", ["All"] + sorted(cities))

if selected_city != "All":
    filtered_df = providers_df[providers_df['City'] == selected_city]
else:
    filtered_df = providers_df

# --- Show providers table ---
st.subheader("Food Providers")
st.dataframe(filtered_df)

# --- Record count ---
st.write(f"Showing {len(filtered_df)} providers.")

# Close connection
conn.close()

