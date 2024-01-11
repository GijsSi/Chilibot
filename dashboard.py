import streamlit as st
import pandas as pd
import sqlite3

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.write("# Welcome to Chilibot! 🌶️")

st.sidebar.success("Select a control dashboard above.")

st.markdown(
    """
    The chilibot project is an open-source project made for the Hogeschool van Amsterdam as my final project that I have to do for my studies. 
    This project aims to be a fully automated growbox for chiliplants. 
    **👈 Select a dashboard from the sidebar** to see wha the chilibot can do!
    ### Want to learn more?
    - Check out the documentation [streamlit.io](https://chilibot.xyz)
    - Ask me a question via Github [issues](https://github.com/GijsSi/Chilibot/issues)
"""
)

def load_data():
    conn = sqlite3.connect('chilibot.sqlite')
    query = """
    SELECT
        timestamp, 
        soil_moisture,
        air_temperature,
        air_humidity
    FROM
        sensor_values  
    WHERE
        timestamp >= '2023-12-11'
    ORDER BY
        timestamp
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Load data
data = load_data()

# Convert timestamp to datetime 
data['timestamp'] = pd.to_datetime(data['timestamp'])

# Set timestamp as index
data.set_index('timestamp', inplace=True)

# Plotting charts
st.subheader("Soil Moisture 🌱")
st.line_chart(data['soil_moisture'])

st.subheader("Air Temperature 🌡️")
st.line_chart(data['air_temperature'])

st.subheader("Air Humidity 💦")
st.line_chart(data['air_humidity'])


