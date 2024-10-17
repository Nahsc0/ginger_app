#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import streamlit as st
import pickle
import pandas as pd

# Load the trained model
with open('fungal_risk_model.pkl', 'rb') as f:
    model = pickle.load(f)

# Define categorical mappings
crop_rotation_mapping = {'no': 0, 'yes': 1}
irrigation_mapping = {'low': 0, 'medium': 1, 'high': 2}
previous_infection_mapping = {'no': 0, 'yes': 1}
fungal_species_mapping = {'None': 0, 'Fusarium': 1, 'Rhizoctonia': 2}

# Apply custom CSS for styling
st.markdown(
    """
    <style>
    .main {
        background-color: #f5f5f5;
    }
    .footer {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: #f5f5f5;
        text-align: center;
        padding: 10px;
        font-size: small;
        color: #666;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Streamlit app layout
st.title("🌿Ginger Fungal Risk Prediction")
st.write("Predict the risk of fungal infection for ginger crops based on environmental and cultivation factors.")

# Input fields for numeric features using sliders
temperature = st.slider("Temperature (°C)", min_value=10.0, max_value=40.0, value=28.5)
humidity = st.slider("Humidity (%)", min_value=10, max_value=100, value=75)
rainfall = st.slider("Rainfall (mm)", min_value=0, max_value=500, value=150)
soil_moisture = st.slider("Soil Moisture (%)", min_value=0, max_value=100, value=40)
ph = st.slider("Soil pH", min_value=3.0, max_value=9.0, value=6.5)

# Input fields for categorical features
crop_rotation = st.selectbox("Crop Rotation", options=['no', 'yes'])
irrigation = st.selectbox("Irrigation Level", options=['low', 'medium', 'high'])
previous_infection = st.radio("Previous Fungal Infection", options=['no', 'yes'])
fungal_species = st.selectbox("Fungal Species", options=['None', 'Fusarium', 'Rhizoctonia'])

# Encode the categorical features
crop_rotation_encoded = crop_rotation_mapping[crop_rotation]
irrigation_encoded = irrigation_mapping[irrigation]
previous_infection_encoded = previous_infection_mapping[previous_infection]
fungal_species_encoded = fungal_species_mapping[fungal_species]

# Prepare input data for prediction
input_data = pd.DataFrame([[temperature, humidity, rainfall, soil_moisture, ph, 
                            crop_rotation_encoded, irrigation_encoded, 
                            previous_infection_encoded, fungal_species_encoded]], 
                          columns=['temperature', 'humidity', 'rainfall', 'soil_moisture', 
                                   'ph', 'crop_rotation', 'irrigation', 
                                   'previous_fungal_infection', 'fungal_species'])

# Prediction
if st.button("Predict Fungal Risk"):
    prediction = model.predict(input_data)[0]
    risk_levels = {0: 'Low', 1: 'Medium', 2: 'High'}
    st.success(f"The predicted fungal risk is: {risk_levels[prediction]}")

# Footer
st.write("---")
st.markdown("### About the App")
st.markdown(
    """
    Developed to assist ginger farmers in identifying potential fungal disease risks.  
    Please ensure to take necessary agricultural measures if the risk level is **'High'**.
    """
)