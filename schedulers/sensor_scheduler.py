import schedule
import can_commands
from db import save_sensor_values
import time

def scheduled_sensor_readings():
    soil_moisture = can_commands.get_soil_moisture()
    time.sleep(2)
    air_temperature, air_humidity = can_commands.get_air_temperature_and_humidity()
    time.sleep(2)

    water_level = can_commands.check_water_level()
    time.sleep(2)
    save_sensor_values(
        soil_moisture=soil_moisture,
        air_temperature=air_temperature,
        air_humidity=air_humidity,
        water_level=water_level
    )

def start_sensor_scheduler():
    job = schedule.every(1).minutes.do(scheduled_sensor_readings)
    return job
