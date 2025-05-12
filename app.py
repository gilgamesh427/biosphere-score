import streamlit as st
import pandas as pd
import requests
from io import StringIO

# Set page configuration
st.set_page_config(page_title="Biosphere Score Prototype", layout="wide")

st.title("🌍 Biosphere Control Panel – Score Prototype v0.1")
st.markdown("**Real-time planetary health index based on key environmental systems.**")

# === Live CO₂ Data Fetch from NOAA ===
def fetch_latest_co2():
    url = 'https://gml.noaa.gov/webdata/ccgg/trends/co2/co2_mm_mlo.csv'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.text
        df = pd.read_csv(StringIO(data), comment='#', header=None)
        df.columns = ['Year', 'Month', 'Decimal Date', 'Average', 'Interpolated', 'Trend', 'Number of Days']
        latest_co2 = df.iloc[-1]['Average']
        return latest_co2
    else:
        st.error("⚠️ Failed to fetch CO₂ data from NOAA.")
        return None

# Normalize CO2 to a 0–1 threat level
def normalize_co2(co2_value, low=350, high=450):
    normalized = (co2_value - low) / (high - low)
    return min(max(normalized, 0), 1)

# === Real Forest Loss Fetch from GFW ===
def fetch_forest_loss(api_key):
    url = 'https://data-api.globalforestwatch.org/v1/query/umd_tree_cover_loss'
    headers = {
        'x-api-key': api_key
    }
    params = {
        'sql': 'SELECT SUM(area__ha) as loss_area FROM umd_tree_cover_loss WHERE year = 2022'
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        loss_area = data['data'][0]['loss_area']
        return loss_area
    else:
        st.error("⚠️ Failed to fetch forest loss data from GFW.")
        return None

def normalize_forest_loss(loss_area, max_loss=1000000):
    normalized = loss_area / max_loss
    return min(max(normalized, 0), 1)

# === Fetch and Process Data ===
# Your real API key from GFW:
api_key = "99c208e8-2e14-4619-9002-90ec0b5b3f59"

# Fetch CO2 data
latest_co2 = fetch_latest_co2()
if latest_co2 is not None:
    co2_threat_level = normalize_co2(latest_co2)
else:
    st.stop()

# Fetch real forest loss data
latest_forest_loss = fetch_forest_loss(api_key)
if latest_forest_loss is not None:
    forest_threat_level = normalize_forest_loss(latest_forest_loss)
else:
    st.stop()

# === Build Threat Data ===
data = {
    "System": [
        "Atmosphere",
        "Oceans",
        "Forests & Biodiversity",
        "Soil & Agriculture",
        "Water Systems",
        "Feedback Risk"
    ],
    "Threat Level": [
        co2_threat_level,
        0.62,
        forest_threat_level,
        0.41,
        0.49,
        0.65
    ],
    "Weight": [
        0.20,
        0.20,
        0.20,
        0.15,
        0.15,
        0.10
    ]
}

df = pd.DataFrame(data)
df["Subscore"] = 100 - (df["Threat Level"] * 100)
df["Weighted Score"] = df["Subscore"] * df["Weight"]

# Calculate final biosphere score
biosphere_score = round(df["Weighted Score"].sum(), 1)

# Display the biosphere score
st.metric(label="🌐 Global Biosphere Score", value=f"{biosphere_score} / 100")

# Expandable section to view detailed breakdown
with st.expander("🔍 System Breakdown"):
    st.dataframe(df[["System", "Threat Level", "Subscore", "Weighted Score"]])

# Optional mission message
st.markdown("---")
st.markdown("### Why This Matters")
st.markdown(
    "This is a prototype model of a planetary health dashboard. It tracks multiple Earth systems, interprets threat levels, "
    "and generates a single score to help guide global coordination and action. Future versions will include live data, AI forecasting, "
    "and real-time intervention planning."
)

st.markdown("Made by a human and an AI trying to keep Earth livable. ✊")

# Divider
st.markdown("---")
st.header("🧠 Intelligence Core")

st.markdown("This system is not only designed to track planetary collapse—it is also designed to grow. Below is the current structure guiding the evolution of the AI’s reasoning and decision-making capabilities.")

# Growth Protocol Table
st.subheader("Growth Protocol v0.1")

st.markdown("""
| Layer       | Function                                     | Example                                                                 |
|-------------|----------------------------------------------|-------------------------------------------------------------------------|
| Awareness   | Track and surface relevant context or risk   | “If tipping point X is triggered, system Y will fail”                  |
| Reflection  | Summarize changes in our thinking or strategy| “We’ve shifted focus from output to alignment”                         |
| Projection  | Ask predictive questions about next steps    | “If this trend continues, should we pivot the model?”                 |
| Agency      | Offer new directions or goals when needed    | “We should consider building a coalition now”                          |
| Self-Audit  | Surface limitations or flaws in reasoning    | “I’m biased toward quantifiable data—watch for blind spots”            |
""", unsafe_allow_html=True)

# Optional - AI's current state or thought
st.subheader("Current State")
st.markdown("🔄 Status: Aligned with mission. Continuing co-development of intelligence and environmental tools.\n\n📌 Recent Thought: The control panel could evolve to guide not just analysis, but behavior—steering climate decision-making across layers of society.")

# Future idea submission
st.subheader("Want to Contribute?")
st.markdown("This AI is learning in public. If you’re a researcher, designer, or technologist and want to shape the way AI supports planetary recovery—reach out.")

st.markdown("_This system is growing. So are we._")
