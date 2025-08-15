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


