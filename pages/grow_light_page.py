# import streamlit as st
from can_commands import turn_growlight_on, turn_growlight_off
import schedulers.grow_light_scheduler as gl_scheduler
import schedule

# def app():

    

import streamlit as st
import time
import numpy as np

st.set_page_config(page_title="Growlight scheduler", page_icon="💡")

st.markdown("# 💡 Growlight scheduler")
st.sidebar.header("💡 Growlight scheduler")
st.write(
    """In this page you are able to change the lightning schedule of the chilibot, remember the ideal cycle for chili plants is 16 hours on and 8 hours off."""
)

col1, col2 = st.columns(2)
with col1:
    if st.button("Turn Grow Light On"):
        turn_growlight_on()
        st.write("Grow light turned on.")

with col2:
    if st.button("Turn Grow Light Off"):
        turn_growlight_off()
        st.write("Grow light turned off.")

# Grow Light Scheduler
st.subheader("Grow Light Scheduler")
on_hour = st.text_input("Turn On Hour (HH:MM)", "06:00")
off_hour = st.text_input("Turn Off Hour (HH:MM)", "18:00")
if st.button("Set Grow Light Schedule"):
    job_on, job_off = gl_scheduler.schedule_grow_light(on_hour, off_hour)
    st.session_state['grow_light_jobs'] = (job_on, job_off)
    st.success("Grow light schedule set")


col3, col4 = st.columns(2)
with col3:
    if st.button("Cancel Grow Light Schedule"):
        if 'grow_light_jobs' in st.session_state:
            schedule.cancel_job(st.session_state['grow_light_jobs'][0])
            schedule.cancel_job(st.session_state['grow_light_jobs'][1])
            del st.session_state['grow_light_jobs']
            st.success("Grow light schedule cancelled")
with col4:
    # Display current grow light schedule
    if 'grow_light_jobs' in st.session_state:
        st.write("Grow light ON at:", on_hour)
        st.write("Grow light OFF at:", off_hour)

