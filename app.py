import streamlit as st
import pandas as pd

# Set page configuration
st.set_page_config(page_title="Biosphere Score Prototype", layout="wide")

st.title("🌍 Biosphere Control Panel – Score Prototype v0.1")
st.markdown("**Real-time planetary health index based on key environmental systems.**")

# Mock data for biosphere systems
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
        0.53,
        0.62,
        0.56,
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
