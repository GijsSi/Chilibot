import can
import struct
import time
from db import log_command

# Set up the CAN bus
bus = can.interface.Bus(channel='can0', bustype='socketcan')



# Function to send a CAN message
def send_can_message(command, data=0):
    # message_data = struct.pack('B', command) + struct.pack('<f', data)
    message_data = struct.pack('B', command) + struct.pack('f', data)
    message = can.Message(arbitration_id=0x100, data=message_data, is_extended_id=False)
    bus.send(message)
    # print(message)

# Function to read CAN messages
def read_can_message(expected_command):
    start_time = time.time()
    while time.time() - start_time < 5:  # Wait for 5 seconds max
        message = bus.recv(1)  # Timeout in seconds
        
        if message is not None and message.arbitration_id == 0x100:
            command = message.data[0]
            if command == expected_command:
                return struct.unpack('f', message.data[1:5])[0]
    return None


def get_soil_moisture():
    send_can_message(0x03)
    return read_can_message(0x03)

def get_air_temperature_and_humidity():
    send_can_message(0x04)
    temperature = read_can_message(0x04)
    send_can_message(0x05)
    humidity = read_can_message(0x05)
    return temperature, humidity

def check_water_level():
    send_can_message(0x0B)
    log_command("get_water_level")
    return read_can_message(0x0B)

def move_motor_to_position(position):
    log_command("move_motor_to_position")
    send_can_message(0x01, float(position))

def get_average_distance():
    send_can_message(0x02)
    log_command("get_average_distance")
    return read_can_message(0x02)

def get_soil_moisture():
    send_can_message(0x03)
    log_command("get_soil_moisture")
    return read_can_message(0x03)

def get_air_temperature():
    send_can_message(0x04)
    log_command("get_air_temperature")

    return read_can_message(0x04)

def get_air_humidity():
    send_can_message(0x04)
    return read_can_message(0x05)

def turn_growlight_on():
    send_can_message(0x06)
    log_command("turn_on_growlight")

def turn_growlight_off():
    send_can_message(0x07)
    log_command("turn_off_growlight")

# TODO Add duration for the water cycle (Has to be implemented on arduino aswell) - Should send a message with data for how many seconds water should be turned on
def turn_on_pump_and_valve():
    send_can_message(0x08)
    log_command("turn_on_pump_and_valve")

def move_motor_up(cm):
    log_command("move_motor_up")
    send_can_message(0x0A, float(cm))
    
def move_motor_down(cm):
    log_command("turn_on_pump_and_valve")
    send_can_message(0x09, float(cm))




# Example usage
# average_distance = get_average_distance()
# soil_moisture = get_soil_moisture()
# temperature, humidity = get_air_temperature_and_humidity()
# water_level = check_water_level()

# print(f"Average Distance: {average_distance}")
# print(f"Soil Moisture: {soil_moisture}")
# print(f"Temperature: {temperature}, Humidity: {humidity}")
# print(f"Water Level: {water_level}")

if __name__ == "__main__":
    turn_on_pump_and_valve()
    # turn_growlight_off()
# Shutdown the CAN bus
    bus.shutdown()

