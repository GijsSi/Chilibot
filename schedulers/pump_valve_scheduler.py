import schedule
import can_commands
import time

# TODO Add duration for the water cycle (Has to be implemented on arduino aswell)
def operate_pump_and_valve(repeat_count):
    for _ in range(repeat_count):
        can_commands.turn_on_pump_and_valve()
        # ? Maybe add this to the arduino code to customize the time the pump should run for. 
        time.sleep(10)
        # can_commands.turn_off_pump_and_valve()

def schedule_pump_and_valve_operation(start_time, repeat_count):
    job = schedule.every().day.at(start_time).do(operate_pump_and_valve, repeat_count)
    return job
