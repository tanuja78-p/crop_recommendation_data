import streamlit as st
import requests

# 1. THE DATA (Simplified list of lists)
# Format: [Crop Name, Min Nitrogen, Max Nitrogen, Min Temp, Max Temp]
crops = [
    ["Rice", 60, 120, 20, 35],
    ["Wheat", 40, 100, 15, 28],
    ["Maize", 50, 120, 20, 35]
]

st.title("🌱 Simple Crop Advisor")

# 2. THE INPUTS (Simple variables)
n_val = st.number_input("Enter Nitrogen (N) level:", value=0)
t_val = st.number_input("Enter Temperature (°C):", value=0)

# 3. THE LOGIC (The core of AI/Data Science)
if st.button("Predict Best Crop"):
    
    found_crop = "No perfect match" # Default message
    
    # We loop through our data to find a match
    for crop in crops:
        name = crop[0]
        min_n = crop[1]
        max_n = crop[2]
        min_t = crop[3]
        max_t = crop[4]
        
        # Check if user input fits in the crop's range
        if (min_n <= n_val <= max_n) and (min_t <= t_val <= max_t):
            found_crop = name
            break # Stop looking once we find a match

    st.success(f"Result: {found_crop}")

    # 4. THE REQUEST (Simple API logic)
    try:
        # We use 'requests' to imagine sending this to an AI
        # In a real lab, you would use: requests.post(url, json={"crop": found_crop})
        st.info(f"AI Tip: Based on {t_val}°C, ensure proper irrigation for {found_crop}.")
    except:
        st.error("Could not connect to AI service.")