import streamlit as st
from can_commands import move_motor_down, move_motor_up
import schedulers.pump_valve_scheduler as pv_scheduler

st.set_page_config(page_title="Platform control", page_icon="↕️")

st.markdown("# ↕️ Platform control")
st.sidebar.header(" ↕️ Platform control")
st.write(
    """In this page you are able to change the level of the bed where the chili plant is standing on. Keep in mind there are no emergency stops implemented. """
)

col1, col2 = st.columns(2)

with col1:
    if st.button(" :arrow_up_small:"):
        move_motor_up(5)
with col2:
    if st.button(" :arrow_down_small:"):
        move_motor_down(5)
