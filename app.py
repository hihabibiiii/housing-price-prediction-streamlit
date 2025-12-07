import streamlit as st
import joblib
import pandas as pd

# Load Model & Columns
model = joblib.load("house_price_model.pkl")
model_columns = joblib.load("model_columns.pkl")

st.title("🏠 California Housing Price Prediction App")

st.markdown("Enter the housing details below to predict price:")

# Input fields UI
longitude = st.number_input("Longitude", step=0.01)
latitude = st.number_input("Latitude", step=0.01)
housing_median_age = st.number_input("Median Housing Age", step=1.0)
total_rooms = st.number_input("Total Rooms", step=1.0)
total_bedrooms = st.number_input("Total Bedrooms", step=1.0)
population = st.number_input("Population", step=1.0)
households = st.number_input("Households", step=1.0)
median_income = st.number_input("Median Income", step=0.01)

st.write("Select Ocean Proximity Category:")
ocean = st.selectbox("Ocean Proximity", 
                     ["INLAND","ISLAND","NEAR BAY","NEAR OCEAN","<base_category>"])

# Convert ocean proximity to dummy encoding
ocean_data = {
    "ocean_proximity_INLAND": 0,
    "ocean_proximity_ISLAND": 0,
    "ocean_proximity_NEAR BAY": 0,
    "ocean_proximity_NEAR OCEAN": 0,
}

# If selected category exists then set 1
key = f"ocean_proximity_{ocean}"
if key in ocean_data:
    ocean_data[key] = 1

# Prepare final input
input_data = {
    "longitude": longitude,
    "latitude": latitude,
    "housing_median_age": housing_median_age,
    "total_rooms": total_rooms,
    "total_bedrooms": total_bedrooms,
    "population": population,
    "households": households,
    "median_income": median_income,
    **ocean_data
}

# Convert to df & align with training columns
df = pd.DataFrame([input_data]).reindex(columns=model_columns, fill_value=0)

# Predict button
if st.button("Predict Price"):
    pred = model.predict(df)[0]
    st.success(f"💰 Predicted House Price: **${int(pred)}**")
