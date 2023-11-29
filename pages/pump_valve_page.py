import streamlit as st
from can_commands import turn_on_pump_and_valve
import schedulers.pump_valve_scheduler as pv_scheduler
import schedule

def app():
    st.title("Pump and Valve Scheduler")

    if st.button("Turn on water"):
        turn_on_pump_and_valve()

    st.subheader("Pump and Valve Scheduler")
    pump_start_time = st.time_input("Start Time for Pump and Valve")
    pump_duration = st.number_input("Duration in Seconds", min_value=1, value=30)
    pump_repeat_count = st.number_input("Repeat Count", min_value=1, value=1)

    if st.button("Set Pump and Valve Schedule"):
        start_time_str = pump_start_time.strftime("%H:%M")
        job = pv_scheduler.schedule_pump_and_valve_operation(start_time_str, pump_duration, pump_repeat_count)
        st.session_state['pump_valve_job'] = job
        st.success(f"Pump and valve scheduled to start everyday at {start_time_str}, {pump_repeat_count} times with {pump_duration} seconds duration")

    if st.button("Cancel Pump and Valve Schedule"):
        if 'pump_valve_job' in st.session_state:
            schedule.cancel_job(st.session_state['pump_valve_job'])
            del st.session_state['pump_valve_job']
            st.success("Pump and valve schedule cancelled")

    # Display current pump and valve schedule
    if 'pump_valve_job' in st.session_state:
        st.write(f"Pump and valve scheduled to start at {pump_start_time.strftime('%H:%M')}, {pump_repeat_count} times with {pump_duration} seconds duration")

    # Ensure Streamlit reruns the script to update the display
    st.button("Refresh")
