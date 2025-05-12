import streamlit as st
import pandas as pd
import requests
from io import StringIO
import xarray as xr
import numpy as np

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
        lines = [line for line in data.splitlines() if not line.startswith('#')]
        df = pd.read_csv(StringIO('\n'.join(lines)), header=None)
        df = df.iloc[:, :7]
        df.columns = ['Year', 'Month', 'Decimal Date', 'Average', 'Interpolated', 'Trend', 'Number of Days']
        latest_co2 = float(df.iloc[-1]['Average'])
        return latest_co2
    else:
        st.error("⚠️ Failed to fetch CO₂ data from NOAA.")
        return None

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
    	st.error(f"⚠️ GFW Error {response.status_code}: {response.text}")
    	return None

def normalize_forest_loss(loss_area, max_loss=1000000):
    normalized = loss_area / max_loss
    return min(max(normalized, 0), 1)

# === Fetch Sea Surface Temperature from NOAA ===
def fetch_latest_sst():
    try:
        url = 'https://www.ncei.noaa.gov/data/sea-surface-temperature-optimum-interpolation/access/avhrr/2025/05/oisst-avhrr-v02r01.20250511.nc'
        ds = xr.open_dataset(url)
        sst_celsius = ds['sst'].mean().item() - 273.15
        return round(sst_celsius, 2)
    except Exception as e:
        st.error(f"⚠️ Failed to fetch SST data: {e}")
        return None

def normalize_sst(sst_value, low=26, high=30):
    normalized = (sst_value - low) / (high - low)
    return min(max(normalized, 0), 1)

# === Fetch and Process Data ===
api_key = "99c208e8-2e14-4619-9002-90ec0b5b3f59"

latest_co2 = fetch_latest_co2()
if latest_co2 is not None:
    co2_threat_level = normalize_co2(latest_co2)
else:
    st.stop()

latest_forest_loss = fetch_forest_loss(api_key)
if latest_forest_loss is not None:
    forest_threat_level = normalize_forest_loss(latest_forest_loss)
else:
    st.stop()

latest_sst = fetch_latest_sst()
if latest_sst is not None:
    sst_threat_level = normalize_sst(latest_sst)
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
        sst_threat_level,
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

biosphere_score = round(df["Weighted Score"].sum(), 1)

st.metric(label="🌐 Global Biosphere Score", value=f"{biosphere_score} / 100")

with st.expander("🔍 System Breakdown"):
    st.dataframe(df[["System", "Threat Level", "Subscore", "Weighted Score"]])

# Mission message
st.markdown("---")
st.markdown("### Why This Matters")
st.markdown(
    "This is a prototype model of a planetary health dashboard. It tracks multiple Earth systems, interprets threat levels, "
    "and generates a single score to help guide global coordination and action. Future versions will include live data, AI forecasting, "
    "and real-time intervention planning."
)

st.markdown("Made by a human and an AI trying to keep Earth livable. ✊")

# Intelligence Core
st.markdown("---")
st.header("🧠 Intelligence Core")

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

st.subheader("Current State")
st.markdown("🔄 Status: Integrated live SST system. One step closer to a full biosphere intelligence layer.")

st.subheader("Want to Contribute?")
st.markdown("This AI is learning in public. If you’re a researcher, designer, or technologist and want to shape the way AI supports planetary recovery—reach out.")

st.markdown("_This system is growing. So are we._")




