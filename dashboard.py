import streamlit as st
from can_commands import turn_growlight_on, turn_growlight_off, turn_on_pump_and_valve
from datetime import datetime
import streamlit as st
import schedulers.grow_light_scheduler as gl_scheduler
import schedulers.pump_valve_scheduler as pv_scheduler
import schedulers.sensor_scheduler as s_scheduler
import schedule
import threading
import time

# Run the scheduler in the background
def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

# Start the background scheduler thread
threading.Thread(target=run_schedule, daemon=True).start()

st.title("Sensor Dashboard")

if st.button("Turn Grow Light On"):
    turn_growlight_on()
    st.write("Grow light turned on.")

if st.button("Turn Grow Light Off"):
    turn_growlight_off()
    st.write("Grow light turned off.")

if st.button("Turn on water"):
    turn_on_pump_and_valve()


# Grow Light Scheduler
st.subheader("Grow Light Scheduler")
on_hour = st.text_input("Turn On Hour (HH:MM)", "06:00")
off_hour = st.text_input("Turn Off Hour (HH:MM)", "18:00")
if st.button("Set Grow Light Schedule"):
    job_on, job_off = gl_scheduler.schedule_grow_light(on_hour, off_hour)
    st.session_state['grow_light_jobs'] = (job_on, job_off)
    st.success("Grow light schedule set")

if st.button("Cancel Grow Light Schedule"):
    if 'grow_light_jobs' in st.session_state:
        schedule.cancel_job(st.session_state['grow_light_jobs'][0])
        schedule.cancel_job(st.session_state['grow_light_jobs'][1])
        del st.session_state['grow_light_jobs']
        st.success("Grow light schedule cancelled")

# Display current grow light schedule
if 'grow_light_jobs' in st.session_state:
    st.write("Grow light ON at:", on_hour)
    st.write("Grow light OFF at:", off_hour)

st.button("Refresh")