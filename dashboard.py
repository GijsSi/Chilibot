from can_commands import turn_growlight_on, turn_growlight_off, turn_on_pump_and_valve
import schedulers.grow_light_scheduler as gl_scheduler
import schedulers.pump_valve_scheduler as pv_scheduler
import schedulers.sensor_scheduler as s_scheduler
from pages import grow_light_page, pump_valve_page


import streamlit as st
import schedule
import threading
import time
from datetime import datetime


# Function to run the scheduler in the background
def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

# Start the background scheduler thread
threading.Thread(target=run_schedule, daemon=True).start()

PAGES = {
    "Grow Light Scheduler 💡": grow_light_page,
    "Pump and Valve Scheduler 🚰": pump_valve_page
}

st.sidebar.title('Navigation')
selection = st.sidebar.selectbox("Go to", list(PAGES.keys()))

page = PAGES[selection]
page.app()

st.title("Sensor Dashboard")

if st.button("Turn Grow Light On", key="grow_light_on"):
    turn_growlight_on()
    st.write("Grow light turned on.")

if st.button("Turn Grow Light Off", key="grow_light_off"):
    turn_growlight_off()
    st.write("Grow light turned off.")

if st.button("Turn on water", key="water_on"):
    turn_on_pump_and_valve()



