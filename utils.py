# utils.py
import pandas as pd

def load_data(path):
    df = pd.read_csv(path)
    return df

def compute_kpis(df):
    total_energy = int(df['Energy_Consumption_kWh'].sum())
    avg_renew = float(df['Renewable_Energy_Percent'].mean())
    total_co2 = float(df['CO2_Emissions_tCO2e'].sum())
    latest_intensity = float(df.iloc[-1]['Energy_Consumption_kWh'] / df.iloc[-1]['Units_Produced'])
    return {
        "total_energy": total_energy,
        "avg_renewable_pct": avg_renew,
        "total_co2": total_co2,
        "latest_intensity": latest_intensity
    }
