# from can_commands import turn_growlight_on, turn_growlight_off, turn_on_pump_and_valve
# import schedulers.grow_light_scheduler as gl_scheduler
# import schedulers.pump_valve_scheduler as pv_scheduler
# import schedulers.sensor_scheduler as s_scheduler
# from pages import grow_light_page, pump_valve_page


# import streamlit as st
# import schedule
# import threading
# import time
# from datetime import datetime



# # Function to run the scheduler in the background
# def run_schedule():
#     while True:
#         schedule.run_pending()
#         time.sleep(1)

# # Start the background scheduler thread
# threading.Thread(target=run_schedule, daemon=True).start()

# # Define your page functions
# def home_page():
#     st.title("Welcome to the Sensor Dashboard")
#     # ...

# # Pages dictionary (optional if you have a lot of pages)
# PAGES = {
#     "home": home_page,
#     "grow_light": grow_light_page,
#     "pump_valve": pump_valve_page
# }

# # Function to create a clickable link in the sidebar
# def create_sidebar_link(page, text):
#     # Creating the hyperlink and setting the URL's query parameter
#     query_params = st.experimental_get_query_params()
#     current_page = query_params["page"][0] if "page" in query_params else ""
#     if current_page == page:
#         # Highlight the current page
#         st.sidebar.markdown(f"* **{text}**")
#     else:
#         st.sidebar.markdown(f"[{text}](/?page={page})")

# # Add links to the sidebar
# create_sidebar_link("home", "Home")
# create_sidebar_link("grow_light", "Grow Light Scheduler 💡")
# create_sidebar_link("pump_valve", "Pump and Valve Scheduler 🚰")

# # Determine which page to display based on the URL's query parameter
# query_params = st.experimental_get_query_params()
# page = query_params["page"][0] if "page" in query_params else "home"
# if page == "grow_light":
#     grow_light_page.app()  # Calling the app function from grow_light_page
# elif page == "pump_valve":
#     pump_valve_page.app()  # Calling the app function from pump_valve_page
# else:
#     home_page()  # Display the main dashboard page

# st.title("🌶️ Chilibot dashboard ")

# if st.button("Turn Grow Light On", key="grow_light_on"):
#     turn_growlight_on()
#     st.write("Grow light turned on.")

# if st.button("Turn Grow Light Off", key="grow_light_off"):
#     turn_growlight_off()
#     st.write("Grow light turned off.")

# if st.button("Turn on water", key="water_on"):
#     turn_on_pump_and_valve()



# import streamlit as st
# from pages import grow_light_page, pump_valve_page

# # Define your page functions
# def home_page():
#     st.title("Welcome to the Sensor Dashboard")

# # Page routes
# PAGES = {
#     "grow_light": grow_light_page.app,
#     "pump_valve": pump_valve_page.app,
#     "home": home_page
# }

# # Page selection based on URL
# query_params = st.experimental_get_query_params()
# page = query_params.get("page", ["home"])[0]  # Default to home page

# if page in PAGES:
#     PAGES[page]()  # Call the appropriate page function
# else:
#     st.error("Page not found")

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
    - Check out the documentation [streamlit.io](https://streamlit.io)
    - Jump into our [documentation](https://docs.streamlit.io)
    - Ask me a question via Github [community
        forums](https://discuss.streamlit.io)
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

# Convert timestamp to datetime if it's not already
data['timestamp'] = pd.to_datetime(data['timestamp'])

# Set timestamp as index (optional, for better plotting)
data.set_index('timestamp', inplace=True)

# Plotting separate charts
st.subheader("Soil Moisture 🌱")
st.line_chart(data['soil_moisture'])

st.subheader("Air Temperature 🌡️")
st.line_chart(data['air_temperature'])

st.subheader("Air Humidity 💦")
st.line_chart(data['air_humidity'])


