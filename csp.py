
import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

st.title("🩸 Blood Donor Registry")

menu = st.sidebar.selectbox("Menu", ["Register as Donor", "Search Donors"])

# Donor Registration
if menu == "Register as Donor":
    st.subheader("Register as a Donor")

    name = st.text_input("Full Name")
    age = st.number_input("Age", min_value=18, max_value=65)
    blood_group = st.selectbox("Blood Group", ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
    city = st.text_input("City")
    contact = st.text_input("Contact Number")

    if st.button("Register"):
        if name and city and contact:
            db.collection("donors").add({
                "name": name,
                "age": age,
                "blood_group": blood_group,
                "city": city.lower(),
                "contact": contact
            })
            st.success("✅ Donor registered successfully!")
        else:
            st.error("❗ Please fill in all required fields.")

# Search Donors
elif menu == "Search Donors":
    st.subheader("Search for Donors")

    search_blood = st.selectbox("Blood Group", ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
    search_city = st.text_input("City").lower()

    if st.button("Search"):
        donors = db.collection("donors") \
                   .where("blood_group", "==", search_blood) \
                   .where("city", "==", search_city) \
                   .stream()

        found = False
        for donor in donors:
            data = donor.to_dict()
            st.write(f"**Name:** {data['name']}")
            st.write(f"**Age:** {data['age']}")
            st.write(f"**Contact:** {data['contact']}")
            st.markdown("---")
            found = True

        if not found:
            st.warning("No donors found for that city and blood group.")
