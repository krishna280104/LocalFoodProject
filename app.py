import streamlit as st


page = st.sidebar.selectbox("Go to page", ["Main", "Receivers", "Food Listings"])
if page == "Main":
    st.header("Food Providers")
    # Paste your existing Providers + filter code here
    

elif page == "Receivers":
    st.header("Receivers Management")
    # Paste your full Receivers CRUD + contact code here
import streamlit as st
import sqlite3

# Connect to database
conn = sqlite3.connect("food_waste.db")
c = conn.cursor()

# Create Receivers table (if not exists)
c.execute('''
CREATE TABLE IF NOT EXISTS Receivers (
    receiver_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    contact_info TEXT,
    location TEXT
)
''')
conn.commit()

# Streamlit page for Receivers
st.header("Receivers Management")

# --- Add Receiver ---
with st.form("Add Receiver"):
    name = st.text_input("Name")
    contact = st.text_input("Contact Info (email/phone)")
    location = st.text_input("Location")
    submitted = st.form_submit_button("Add Receiver")
    if submitted:
        c.execute("INSERT INTO Receivers (name, contact_info, location) VALUES (?, ?, ?)",
                  (name, contact, location))
        conn.commit()
        st.success(f"Receiver '{name}' added!")

# --- Display all Receivers ---
st.subheader("All Receivers")
c.execute("SELECT * FROM Receivers")
receivers = c.fetchall()
st.dataframe(receivers)

# --- Update Receiver ---
st.subheader("Update Receiver")
receiver_ids = [r[0] for r in receivers]
selected_id = st.selectbox("Select Receiver ID to Update", receiver_ids)
if selected_id:
    new_name = st.text_input("New Name")
    new_contact = st.text_input("New Contact Info")
    new_location = st.text_input("New Location")
    if st.button("Update Receiver"):
        c.execute('''
        UPDATE Receivers
        SET name=?, contact_info=?, location=?
        WHERE receiver_id=?
        ''', (new_name, new_contact, new_location, selected_id))
        conn.commit()
        st.success("Receiver updated!")

# --- Delete Receiver ---
st.subheader("Delete Receiver")
selected_del = st.selectbox("Select Receiver ID to Delete", receiver_ids)
if st.button("Delete Receiver"):
    c.execute("DELETE FROM Receivers WHERE receiver_id=?", (selected_del,))
    conn.commit()
    st.success("Receiver deleted!")

# --- Contact Receiver ---
st.subheader("Contact Receiver")
for r in receivers:
    st.markdown(f"{r[1]} — [Contact]({r[2]})")  # r[1]=name, r[2]=contact_info


elif page == "Food Listings":
    st.header("Food Listings Management")
    # Paste your full Food Listings CRUD + contact code here
import streamlit as st
import sqlite3

# Connect to database
conn = sqlite3.connect("food_waste.db")
c = conn.cursor()

# Create Food Listings table (if not exists)
c.execute('''
CREATE TABLE IF NOT EXISTS Food_Listings (
    listing_id INTEGER PRIMARY KEY AUTOINCREMENT,
    provider_id INTEGER,
    food_type TEXT,
    quantity_available INTEGER,
    date_posted TEXT,
    FOREIGN KEY(provider_id) REFERENCES Providers(provider_id)
)
''')
conn.commit()

st.header("Food Listings Management")

# --- Add Food Listing ---
with st.form("Add Listing"):
    provider_id = st.number_input("Provider ID", min_value=1, step=1)
    food_type = st.text_input("Food Type")
    quantity = st.number_input("Quantity Available", min_value=0, step=1)
    date_posted = st.date_input("Date Posted")
    submitted = st.form_submit_button("Add Listing")
    if submitted:
        c.execute('''
        INSERT INTO Food_Listings (provider_id, food_type, quantity_available, date_posted)
        VALUES (?, ?, ?, ?)
        ''', (provider_id, food_type, quantity, date_posted))
        conn.commit()
        st.success(f"Listing '{food_type}' added!")

# --- Display all listings ---
st.subheader("All Food Listings")
c.execute("SELECT * FROM Food_Listings")
listings = c.fetchall()
st.dataframe(listings)

# --- Update Listing ---
st.subheader("Update Listing")
listing_ids = [l[0] for l in listings]
selected_id = st.selectbox("Select Listing ID to Update", listing_ids)
if selected_id:
    new_food_type = st.text_input("New Food Type")
    new_quantity = st.number_input("New Quantity", min_value=0, step=1)
    if st.button("Update Listing"):
        c.execute('''
        UPDATE Food_Listings
        SET food_type=?, quantity_available=?
        WHERE listing_id=?
        ''', (new_food_type, new_quantity, selected_id))
        conn.commit()
        st.success("Listing updated!")

# --- Delete Listing ---
st.subheader("Delete Listing")
selected_del = st.selectbox("Select Listing ID to Delete", listing_ids)
if st.button("Delete Listing"):
    c.execute("DELETE FROM Food_Listings WHERE listing_id=?", (selected_del,))
    conn.commit()
    st.success("Listing deleted!")

# --- Contact Provider ---
st.subheader("Contact Provider")
for l in listings:
    provider_id = l[1]  # provider_id
    # Fetch provider contact info
    c.execute("SELECT name, contact_info FROM Providers WHERE provider_id=?", (provider_id,))
    provider = c.fetchone()
    if provider:
        st.markdown(f"Listing '{l[2]}' by {provider[0]} — [Contact]({provider[1]})")



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

