import schedule
import can_commands
from db import save_sensor_values

def scheduled_sensor_readings():
    average_distance = can_commands.get_average_distance()
    soil_moisture = can_commands.get_soil_moisture()
    air_temperature, air_humidity = can_commands.get_air_temperature_and_humidity()
    water_level = can_commands.check_water_level()

    save_sensor_values(
        average_distance=average_distance,
        soil_moisture=soil_moisture,
        air_temperature=air_temperature,
        air_humidity=air_humidity,
        water_level=water_level
    )

def start_sensor_scheduler():
    job = schedule.every(30).minutes.do(scheduled_sensor_readings)
    return job
