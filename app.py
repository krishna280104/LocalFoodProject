import streamlit as st


page = st.sidebar.selectbox("Go to page", ["Main", "Receivers", "Food Listings"])
if page == "Main":
    st.header("Food Providers")
    # Paste your existing Providers + filter code here
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


    

elif page == "Receivers":
    st.header("Receivers Management")
    # Paste your full Receivers CRUD + contact code here



elif page == "Food Listings":
    st.header("Food Listings Management")
    # Paste your full Food Listings CRUD + contact code here



