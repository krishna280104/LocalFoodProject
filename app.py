import streamlit as st
import pandas as pd
import sqlite3

# --- Database connection ---
conn = sqlite3.connect("food_wastage.db")

# --- Sidebar for navigation ---
st.sidebar.title("📌 Navigation")
page = st.sidebar.radio("Go to:", 
                        ["🏠 Home", 
                         "📦 Food Listings", 
                         "👨‍🍳 Providers", 
                         "🙋 Receivers", 
                         "📑 Claims", 
                         "📊 Analysis (15 Queries)", 
                         "✏️ CRUD Operations"])

# --- Home Page ---
if page == "🏠 Home":
    st.title("🍽️ Local Food Wastage Management System")
    st.write("""
    This system connects **food providers** (restaurants, stores) with **receivers** (NGOs, individuals).  
    ✅ Filter food donations by location, provider, type  
    ✅ View provider & receiver contact info  
    ✅ Perform CRUD operations  
    ✅ Run 15 SQL queries for analysis  
    """)

# --- Food Listings ---
elif page == "📦 Food Listings":
    st.title("📦 Food Listings with Filters")
    food_df = pd.read_sql("SELECT * FROM food_listings", conn)

    # Sidebar filters
    st.sidebar.subheader("Filters")
    city_filter = st.sidebar.selectbox("Location:", ["All"] + list(food_df["Location"].unique()))
    provider_filter = st.sidebar.selectbox("Provider Type:", ["All"] + list(food_df["Provider_Type"].unique()))
    food_type_filter = st.sidebar.selectbox("Food Type:", ["All"] + list(food_df["Food_Type"].unique()))

    # Apply filters
    filtered = food_df.copy()
    if city_filter != "All":
        filtered = filtered[filtered["Location"] == city_filter]
    if provider_filter != "All":
        filtered = filtered[filtered["Provider_Type"] == provider_filter]
    if food_type_filter != "All":
        filtered = filtered[filtered["Food_Type"] == food_type_filter]

    st.dataframe(filtered)
    st.write(f"Showing {len(filtered)} records.")

# --- Providers ---
elif page == "👨‍🍳 Providers":
    st.title("👨‍🍳 Food Providers")
    providers_df = pd.read_sql("SELECT Name, City, Contact FROM providers", conn)
    st.dataframe(providers_df)

# --- Receivers ---
elif page == "🙋 Receivers":
    st.title("🙋 Food Receivers")
    receivers_df = pd.read_sql("SELECT Name, City, Contact FROM receivers", conn)
    st.dataframe(receivers_df)

# --- Claims ---
elif page == "📑 Claims":
    st.title("📑 Claims")
    claims_df = pd.read_sql("SELECT * FROM claims", conn)
    st.dataframe(claims_df)

# --- Analysis (15 Queries) ---
elif page == "📊 Analysis (15 Queries)":
    st.title("📊 SQL Analysis - 15 Queries")

    st.subheader("1. Providers per City")
    q1 = "SELECT City, COUNT(*) AS provider_count FROM providers GROUP BY City"
    st.dataframe(pd.read_sql(q1, conn))

    st.subheader("2. Receivers per City")
    q2 = "SELECT City, COUNT(*) AS receiver_count FROM receivers GROUP BY City"
    st.dataframe(pd.read_sql(q2, conn))

   

    # Query 3
    st.subheader("3. Contact Info of Food Providers in Kochi")
    q3 = "SELECT Name, Contact FROM providers WHERE City = 'Kochi'"
    st.dataframe(pd.read_sql(q3, conn))

    # Query 4
    st.subheader("4. Food Contribution by Provider Type")
    q4 = """
    SELECT Provider_Type, SUM(Quantity) AS total_quantity
    FROM food_listings
    GROUP BY Provider_Type
    ORDER BY total_quantity DESC
    """
    st.dataframe(pd.read_sql(q4, conn))

    # Query 5
    st.subheader("5. Most Frequently Claimed Food Items")
    q5 = """
    SELECT f.Food_Name, COUNT(c.Claim_ID) AS times_claimed
    FROM food_listings f
    JOIN claims c ON f.Food_ID = c.Food_ID
    GROUP BY f.Food_Name
    ORDER BY times_claimed DESC
    LIMIT 10
    """
    st.dataframe(pd.read_sql(q5, conn))

    # Query 6
    st.subheader("6. Food Listings Expiring Within 2 Days")
    q6 = "SELECT * FROM food_listings WHERE julianday(Expiry_Date) - julianday('now') <= 2"
    st.dataframe(pd.read_sql(q6, conn))

    # Query 7
    st.subheader("7. Top 5 Cities by Food Providers")
    q7 = "SELECT City, COUNT(*) AS provider_count FROM providers GROUP BY City ORDER BY provider_count DESC LIMIT 5"
    st.dataframe(pd.read_sql(q7, conn))

    # Query 8
    st.subheader("8. Claims by Receivers")
    q8 = """
    SELECT r.Name, COUNT(c.Claim_ID) AS total_claims
    FROM receivers r
    JOIN claims c ON r.Receiver_ID = c.Receiver_ID
    GROUP BY r.Name
    ORDER BY total_claims DESC
    """
    st.dataframe(pd.read_sql(q8, conn))

    # Query 9
    st.subheader("9. Pending Claims")
    q9 = "SELECT * FROM claims WHERE Status = 'Pending'"
    st.dataframe(pd.read_sql(q9, conn))

    # Query 10
    st.subheader("10. Average Quantity of Food by Type")
    q10 = "SELECT Food_Type, AVG(Quantity) AS avg_quantity FROM food_listings GROUP BY Food_Type"
    st.dataframe(pd.read_sql(q10, conn))

    # Query 11
    st.subheader("11. Providers with More than 5 Donations")
    q11 = """
    SELECT p.Name, COUNT(f.Food_ID) AS donations
    FROM providers p
    JOIN food_listings f ON p.Provider_ID = f.Provider_ID
    GROUP BY p.Name
    HAVING donations > 5
    """
    st.dataframe(pd.read_sql(q11, conn))

    # Query 12
    st.subheader("12. Food Listings Grouped by Meal Type")
    q12 = "SELECT Meal_Type, COUNT(*) AS total_listings FROM food_listings GROUP BY Meal_Type"
    st.dataframe(pd.read_sql(q12, conn))

    # Query 13
    st.subheader("13. Completed Claims with Receiver Info")
    q13 = """
    SELECT c.Claim_ID, r.Name AS Receiver_Name, f.Food_Name, c.Status
    FROM claims c
    JOIN receivers r ON c.Receiver_ID = r.Receiver_ID
    JOIN food_listings f ON c.Food_ID = f.Food_ID
    WHERE c.Status = 'Completed'
    """
    st.dataframe(pd.read_sql(q13, conn))

    # Query 14
    st.subheader("14. Top 5 Most Donated Food Items")
    q14 = """
    SELECT Food_Name, COUNT(*) AS donation_count
    FROM food_listings
    GROUP BY Food_Name
    ORDER BY donation_count DESC
    LIMIT 5
    """
    st.dataframe(pd.read_sql(q14, conn))

    # Query 15
    st.subheader("15. Claims Distribution by Status")
    q15 = "SELECT Status, COUNT(*) AS total FROM claims GROUP BY Status"
    st.dataframe(pd.read_sql(q15, conn))


# --- CRUD Operations ---
elif page == "✏️ CRUD Operations":
    st.title("✏️ CRUD Operations - Add New Food Listing")

    with st.form("add_food"):
        food_name = st.text_input("Food Name")
        quantity = st.number_input("Quantity", min_value=1)
        expiry = st.date_input("Expiry Date")
        provider_id = st.number_input("Provider ID", min_value=1)
        food_type = st.selectbox("Food Type", ["Vegetarian", "Non-Vegetarian", "Vegan"])
        meal_type = st.selectbox("Meal Type", ["Breakfast", "Lunch", "Dinner", "Snacks"])
        submitted = st.form_submit_button("Add Food")

        if submitted:
            conn.execute(
                "INSERT INTO food_listings (Food_Name, Quantity, Expiry_Date, Provider_ID, Provider_Type, Location, Food_Type, Meal_Type) VALUES (?, ?, ?, ?, '', '', ?, ?)",
                (food_name, quantity, str(expiry), provider_id, food_type, meal_type)
            )
            conn.commit()
            st.success("✅ New food listing added!")
