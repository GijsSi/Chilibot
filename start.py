import subprocess
import schedule
import time
from schedulers.sensor_scheduler import start_sensor_scheduler

def set_up_can_bus():
    command = ['sudo', 'ip', 'link', 'set', 'can0', 'up', 'type', 'can', 'bitrate', '500000']
    subprocess.run(command)

def start_streamlit_dashboard():
    command = ['nohup', 'streamlit', 'run', 'dashboard.py']
    subprocess.Popen(command)

if __name__ == "__main__":
    set_up_can_bus()
    start_streamlit_dashboard()
    start_sensor_scheduler()

    while True:
        schedule.run_pending()
        time.sleep(1)
