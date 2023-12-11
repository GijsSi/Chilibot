from schedulers.sensor_scheduler import start_sensor_scheduler
import schedule
import time 

if __name__ == "__main__":
    start_sensor_scheduler()
    while True:
        schedule.run_pending()
        time.sleep(1)