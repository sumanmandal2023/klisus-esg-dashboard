import streamlit as st
import pandas as pd
import os
from utils import load_data, compute_kpis
from verification import compute_hash, create_proof_record, store_proof_local

st.set_page_config(page_title="KliSus ESG-Energy Dashboard", layout="wide")
st.title("🌱 KliSus ESG-Energy Dashboard (MVP)")

# --- Sidebar ---
st.sidebar.header("Data Input")
upload = st.sidebar.file_uploader("Upload your energy CSV", type=["csv"])
use_sample = st.sidebar.checkbox("Use sample data", value=True)

# --- File Handling ---
df = None

if upload is not None:
    file_bytes = upload.getvalue()
    file_hash = compute_hash(file_bytes)
    st.sidebar.markdown(f"**File hash:** `{file_hash[:16]}...`")
    try:
        df = pd.read_csv(upload)
        record = create_proof_record(upload.name, file_hash)
        store_proof_local(record)
        st.sidebar.success("✅ File uploaded and verified")
    except Exception as e:
        st.error(f"Error reading uploaded CSV: {e}")
        st.stop()

elif use_sample:
    local_path = "data/energy_sample.csv"
    remote_url = "https://raw.githubusercontent.com/sumanmandal2023/klisus-esg-dashboard/refs/heads/main/energy_sample.csv"

    try:
        if os.path.exists(local_path):
            df = pd.read_csv(local_path)
        else:
            st.info("🔄 Loading sample data from GitHub...")
            df = pd.read_csv(remote_url)
            st.sidebar.success("✅ Sample data loaded from GitHub")
    except Exception as e:
        st.warning("⚠️ Sample data not found. Please upload a CSV file using the sidebar.")
        st.stop()
else:
    st.info("📂 Please upload your CSV or check 'Use sample data'.")
    st.stop()

# --- KPIs ---
kpis = compute_kpis(df)
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Energy (kWh)", f"{kpis['total_energy']:,}")
col2.metric("Avg Renewable (%)", f"{kpis['avg_renewable_pct']:.1f}%")
col3.metric("Total CO₂ (tCO₂e)", f"{kpis['total_co2']:,}")
col4.metric("Energy Intensity (kWh/unit)", f"{kpis['latest_intensity']:.2f}")

# --- Charts ---
st.subheader("📊 Trends Overview")
st.line_chart(df.set_index("Year")["Energy_Consumption_kWh"])
st.bar_chart(df.set_index("Year")["Renewable_Energy_Percent"])
st.line_chart(df.set_index("Year")["CO2_Emissions_tCO2e"])

# --- ESG Mapping ---
st.subheader("🌍 ESG Indicator Mapping")
mapping = {
    "BRSR": "Energy use, Renewable energy, Emission reduction",
    "GRI 302": "Energy efficiency initiatives",
    "GRI 305": "Emission reduction performance",
    "CSRD": "Verified renewable energy share"
}
st.table(pd.DataFrame(list(mapping.items()), columns=["Framework", "Relevant Metrics"]))

# --- Verification Records ---
st.subheader("🧾 Verification Ledger")
try:
    with open("ledger.json", "r") as f:
        import json
        ledger = json.load(f)
        st.dataframe(ledger)
except FileNotFoundError:
    st.info("No verification records yet — upload a CSV to create one.")


