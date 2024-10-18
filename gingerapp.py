#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import numpy as np
import pickle

# Load models
with open('crop_model.pkl', 'rb') as f:
    crop_model = pickle.load(f)
with open('fungal_model.pkl', 'rb') as f:
    fungal_model = pickle.load(f)

# Load crop mapping
with open('crop_mapping.pkl', 'rb') as f:
    crop_mapping = pickle.load(f)

# Streamlit app interface
st.set_page_config(page_title="Crop and Fungal Risk Recommendation", page_icon="🌱", layout="centered")

# Custom CSS for styling
st.markdown(
    """
    <style>
    body {
        background-color: #f0f2f6;
    }
    .main {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🌾 Crop Recommendation and Fungal Risk Detection 🌾")
st.write("Provide the parameters below to get crop and fungal risk recommendations.")

# User inputs for the features
N = st.number_input("Nitrogen (N)", min_value=0.0, step=0.1)
P = st.number_input("Phosphorus (P)", min_value=0.0, step=0.1)
K = st.number_input("Potassium (K)", min_value=0.0, step=0.1)
ph = st.number_input("pH level", min_value=0.0, max_value=14.0, step=0.1)
temperature = st.number_input("Temperature (°C)", min_value=-50.0, max_value=50.0, step=0.1)
humidity = st.number_input("Humidity (%)", min_value=0.0, max_value=100.0, step=0.1)
rainfall = st.number_input("Rainfall (mm)", min_value=0.0, step=0.1)

# Feature engineering
temp_humidity_interaction = temperature * humidity
rainfall_humidity_interaction = rainfall * humidity
cumulative_rainfall = rainfall

# Ensure features match the order used during training
input_data = np.array([[N, P, K, ph, temperature, humidity, rainfall,
                        temp_humidity_interaction, rainfall_humidity_interaction, cumulative_rainfall]])

# Make predictions upon button click
if st.button("Recommend Crop"):
    # Predict crop
    crop_prediction = crop_model.predict(input_data)[0]
    crop_name = crop_mapping[crop_prediction]
    
    # Predict fungal risk
    fungal_prediction = fungal_model.predict(input_data)[0]
    fungal_risk_label = {0: 'Low', 1: 'Medium', 2: 'High'}[fungal_prediction]
    
    # Display the results
    st.success(f"Recommended Crop: **{crop_name}**")
    st.info(f"Fungal Risk Level: **{fungal_risk_label}**")
else:
    st.write("Click on 'Recommend Crop' to get the prediction.")

# Footer
st.markdown("---")
st.write("🌍 Developed with ❤️ for sustainable farming 🌱")

