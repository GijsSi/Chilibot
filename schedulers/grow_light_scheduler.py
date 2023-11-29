import schedule
import can_commands

def turn_growlight_on_job():
    can_commands.turn_growlight_on()

def turn_growlight_off_job():
    can_commands.turn_growlight_off()

def schedule_grow_light(on_hour, off_hour):
    job_on = schedule.every().day.at(on_hour).do(turn_growlight_on_job)
    job_off = schedule.every().day.at(off_hour).do(turn_growlight_off_job)
    return job_on, job_off
