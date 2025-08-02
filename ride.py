import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Vehicle Ride Dashboard", layout="wide")
st.title("🚗 Vehicle Ride Telemetry Dashboard")

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("uber_iot_sample_rides_vKGnWZyZem.csv")  # Update filename if different
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])

    # Extract latitude and longitude from GPS_Location column
    df[["Latitude", "Longitude"]] = df["GPS_Location"].str.extract(
        r'([0-9.]+)° N,\s*([0-9.]+)° E'
    ).astype(float)

    return df

df = load_data()

# Sidebar filter
st.sidebar.header("⏱️ Filter by Time")
start_time = st.sidebar.time_input("Start Time", value=df["Timestamp"].min().time())
end_time = st.sidebar.time_input("End Time", value=df["Timestamp"].max().time())

# Apply time filter
df_filtered = df[
    (df["Timestamp"].dt.time >= start_time) &
    (df["Timestamp"].dt.time <= end_time)
]

# Preview
st.subheader("📄 Filtered Dataset")
st.dataframe(df_filtered)

# Summary statistics
st.subheader("📊 Summary Statistics")
st.dataframe(df_filtered.describe())

# Line plots
st.subheader("🚦 Speed Over Time")
fig1, ax1 = plt.subplots()
ax1.plot(df_filtered["Timestamp"], df_filtered["Speed_kmph"], marker='o')
ax1.set_xlabel("Time")
ax1.set_ylabel("Speed (kmph)")
ax1.set_title("Speed vs Time")
st.pyplot(fig1)

st.subheader("🔋 Fuel or Battery Level Over Time")
fig2, ax2 = plt.subplots()
ax2.plot(df_filtered["Timestamp"], df_filtered["Fuel_or_Battery_Level_%"], color='green', marker='x')
ax2.set_xlabel("Time")
ax2.set_ylabel("Level (%)")
ax2.set_title("Fuel/Battery Level vs Time")
st.pyplot(fig2)

# Fault & Safety Events
st.subheader("🚨 Safety Events and Brake Info")
st.write(df_filtered[["Timestamp", "Brake_Event", "Seatbelt_Status", "Door_Status", "Ambient_Noise_dB"]])

# 🌍 Location Map
st.subheader("📍 Ride Location Map")

# Rename columns to lowercase as required by st.map
map_data = df_filtered.rename(columns={"Latitude": "latitude", "Longitude": "longitude"})

if "latitude" in map_data and "longitude" in map_data:
    st.map(map_data[["latitude", "longitude"]])
else:
    st.warning("No location data available to plot on map.")

