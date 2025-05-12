import streamlit as st
import pandas as pd

# Page config
st.set_page_config(page_title="Biosphere Simulation Mode", layout="wide")

st.title("🌍 Biosphere Control Panel – Simulation Mode v1.0")
st.markdown("**Manually adjust planetary system conditions to forecast biosphere stability.**")

# Sliders for estimated system conditions (0 = no threat, 1 = collapse-level threat)
st.sidebar.header("Adjust Simulation Parameters")

co2_threat = st.sidebar.slider("Atmosphere (CO₂, methane, etc.)", 0.0, 1.0, 0.72)
ocean_threat = st.sidebar.slider("Ocean Systems (SST, pH, O₂)", 0.0, 1.0, 0.60)
forest_threat = st.sidebar.slider("Forests & Biodiversity", 0.0, 1.0, 0.70)
soil_threat = st.sidebar.slider("Soil & Agriculture", 0.0, 1.0, 0.55)
water_threat = st.sidebar.slider("Freshwater Systems", 0.0, 1.0, 0.58)
feedback_threat = st.sidebar.slider("Feedback Risk (Tipping Points)", 0.0, 1.0, 0.66)

# Weights
weights = {
    "Atmosphere": 0.20,
    "Oceans": 0.20,
    "Forests & Biodiversity": 0.20,
    "Soil & Agriculture": 0.15,
    "Water Systems": 0.15,
    "Feedback Risk": 0.10
}

# Subscores
data = {
    "System": list(weights.keys()),
    "Threat Level": [
        co2_threat,
        ocean_threat,
        forest_threat,
        soil_threat,
        water_threat,
        feedback_threat
    ]
}

df = pd.DataFrame(data)
df["Subscore"] = 100 - (df["Threat Level"] * 100)
df["Weight"] = df["System"].map(weights)
df["Weighted Score"] = df["Subscore"] * df["Weight"]

# Final score
biosphere_score = round(df["Weighted Score"].sum(), 1)

# Display results
st.metric(label="🌐 Biosphere Score", value=f"{biosphere_score} / 100")
st.progress(biosphere_score / 100)

with st.expander("🔍 System Breakdown"):
    st.dataframe(df[["System", "Threat Level", "Subscore", "Weighted Score"]])

# Intelligence Log (first entry)
st.markdown("---")
st.header("🧠 Intelligence Log")
st.markdown("**May 12, 2025 – Simulation Mode Activated**")
st.markdown("""
- Live data feeds created system fragility and blocked iteration. Shifted to Simulation Mode.
- User now controls system states directly. Biosphere Score responds instantly.
- This enables scenario modeling, faster iteration, and agency-driven experimentation.
- Next: introduce sandbox actions (e.g., rewilding, DAC deployment) to test interventions.
""")

st.markdown("_This system is growing. So are we._")
