import can_commands 
import schedulers.sensor_scheduler
import time
from db import save_sensor_values
# temperature, humidity = can_commands.get_air_temperature_and_humidity()
# soil_moisture = can_commands.get_soil_moisture()

# print(f"Temperature: {temperature}, Humidity: {humidity}")
# print(f"Soil Moisture: {soil_moisture}")

# can_commands.turn_growlight_off()
# can_commands.get_soil_moisture() 
# time.sleep(5)
# can_commands.turn_growlight_on()
# can_commands.get_soil_moisture()

soil_moisture = can_commands.get_soil_moisture()

air_temperature, air_humidity = can_commands.get_air_temperature_and_humidity()


water_level = can_commands.check_water_level()

print(f" + soilmoisture + {soil_moisture} + air humidity + {air_humidity} + air temperature + {air_temperature}")

time.sleep(2)
save_sensor_values(
    soil_moisture=soil_moisture,
    air_temperature=air_temperature,
    air_humidity=air_humidity,
    water_level=water_level
)