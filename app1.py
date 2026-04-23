import streamlit as st
import requests
import json

# --- PAGE CONFIG ---
st.set_page_config(page_title="AgriSense Dashboard", layout="wide")

# --- CUSTOM STYLING (Matching your HTML) ---
st.markdown("""
    <style>
    .main { background-color: #f0fae9; }
    div[data-testid="stMetricValue"] { color: #2e7d20; font-family: 'Outfit', sans-serif; }
    .stButton>button {
        background-color: #236118;
        color: white;
        border-radius: 8px;
        width: 100%;
        height: 3em;
    }
    .ai-response-box {
        background-color: #ffffff;
        border-left: 5px solid #3a9c28;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# --- MOCK DATA & LOGIC ---
CROP_DATA = [
    {"name": "Rice", "minN": 60, "maxN": 120, "minP": 30, "maxP": 80, "minK": 30, "maxK": 80, "minTemp": 20, "maxTemp": 35, "minHum": 70, "maxHum": 95, "minPh": 5.5, "maxPh": 7.0, "minRain": 150, "maxRain": 300},
    {"name": "Maize", "minN": 50, "maxN": 120, "minP": 35, "maxP": 75, "minK": 30, "maxK": 80, "minTemp": 20, "maxTemp": 35, "minHum": 50, "maxHum": 80, "minPh": 5.8, "maxPh": 7.2, "minRain": 80, "maxRain": 200},
    {"name": "Wheat", "minN": 40, "maxN": 100, "minP": 30, "maxP": 70, "minK": 25, "maxK": 70, "minTemp": 15, "maxTemp": 28, "minHum": 45, "maxHum": 75, "minPh": 6.0, "maxPh": 7.5, "minRain": 50, "maxRain": 150}
]

def calculate_match(crop, inputs):
    score = 0
    params = [
        (inputs['N'], crop['minN'], crop['maxN']),
        (inputs['P'], crop['minP'], crop['maxP']),
        (inputs['K'], crop['minK'], crop['maxK']),
        (inputs['temp'], crop['minTemp'], crop['maxTemp']),
        (inputs['ph'], crop['minPh'], crop['maxPh'])
    ]
    for val, c_min, c_max in params:
        if c_min <= val <= c_max: score += 1
        else:
            diff = min(abs(val - c_min), abs(val - c_max))
            score += max(0, 1 - (diff / 20)) 
    return (score / len(params)) * 100

# --- HEADER ---
st.title("🌿 AgriSense")
st.markdown("*Smart Climate Crop Monitoring Platform*")

# --- DASHBOARD STATS ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("Avg Temp", "27.8°C", "1.2°")
col2.metric("Humidity", "68%", "Stable")
col3.metric("Rainfall", "186mm", "14mm")
col4.metric("Soil pH", "6.4", "-0.1")

st.divider()

# --- INPUT SECTION ---
st.subheader("Field Parameters")
c1, c2, c3, c4 = st.columns(4)
n_val = c1.number_input("Nitrogen (N)", 0, 200, 90)
p_val = c2.number_input("Phosphorus (P)", 0, 200, 42)
k_val = c3.number_input("Potassium (K)", 0, 200, 43)
ph_val = c4.number_input("pH level", 0.0, 14.0, 6.5)

temp_val = c1.slider("Temperature (°C)", 10, 50, 28)
hum_val = c2.slider("Humidity (%)", 0, 100, 70)
rain_val = c3.slider("Rainfall (mm)", 0, 500, 150)
soil_type = c4.selectbox("Soil Type", ["Loamy", "Sandy", "Clay", "Black"])

# --- API ANALYSIS ---
if st.button("Generate AI Insights"):
    current_inputs = {'N': n_val, 'P': p_val, 'K': k_val, 'temp': temp_val, 'ph': ph_val}
    
    # Calculate recommendations
    results = []
    for crop in CROP_DATA:
        match_perc = calculate_match(crop, current_inputs)
        results.append({"name": crop['name'], "score": match_perc})
    
    results = sorted(results, key=lambda x: x['score'], reverse=True)
    top_crop = results[0]['name']

    # Streamlit "Requests" to Claude API (or your proxy)
    # Note: Replace with your actual API key and endpoint
    API_URL = "https://api.anthropic.com/v1/messages"
    HEADERS = {
        "x-api-key": "YOUR_API_KEY",
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }
    
    prompt = f"The top crop is {top_crop} with parameters N:{n_val}, P:{p_val}, K:{k_val}, pH:{ph_val}. Provide 3 short agronomic tips."
    
    payload = {
        "model": "claude-3-haiku-20240307",
        "max_tokens": 200,
        "messages": [{"role": "user", "content": prompt}]
    }

    with st.spinner("Analyzing soil data..."):
        try:
            # Using requests to fetch the AI response
            # response = requests.post(API_URL, headers=HEADERS, json=payload)
            # data = response.json()
            # ai_text = data['content'][0]['text']
            
            # Fallback for demonstration
            ai_text = f"Based on your NPK levels and pH of {ph_val}, {top_crop} is your best choice. Ensure consistent irrigation during the flowering stage to maximize yield in {soil_type} soil."
            
            st.success(f"Top Match: {top_crop} ({results[0]['score']:.1f}%)")
            st.markdown(f"""<div class="ai-response-box"><b>AI Insight:</b><br>{ai_text}</div>""", unsafe_allow_html=True)
            
            # Simple Chart using Streamlit's native charting
            st.bar_chart({res['name']: res['score'] for res in results})
            
        except Exception as e:
            st.error(f"Error connecting to AI service: {e}")

# --- FOOTER ---
st.caption("AgriSense Engine v3.1 | Data refreshed every 5 minutes")