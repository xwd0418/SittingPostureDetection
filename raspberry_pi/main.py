import threading
import time
import RPi.GPIO as GPIO
from gpiozero import LED, Button
import serial
import os  # For speaker sound execution


import arduino 
from sensors.shock_sensor import shock_sensor
from sensors.motion_sensor import motion_sensor
from sensors.LED import led_red, led_green, led_light_control
from sensors.speaker import speaker


SLEEP_TIME = 0.1  # 0.1 second

# Shared Variables with Thread Lock
shared_data = {
    "sitting_status": 0,  # should be a float number from -1 to 1. -1 means bad, 1 mean good
    "prolonged_inactivity": 0,    # 0 means ok, 1 means prolonged inactivity
    "no_leg_motion": 0,  # 0 means ok, 1 means no leg motion
    "user_stands_up": 0  # 0 means user is sitting, 1 means user stands up
}
data_lock = threading.Lock()

# **Thread 1: Arduino BLR Sitting Position Check**
def sitting_position_monitor():
    while True:
        sitting_status  = arduino.update_seat_status()
        with data_lock:
            shared_data["sitting_status"] = sitting_status
        time.sleep(SLEEP_TIME)

# **Thread 2: Shock Sensor (Seat Departure Detection)**
def shock_sensor_monitor():
    while True:
        if_no_motion = shock_sensor.update_if_inactive()
        with data_lock:
            shared_data["prolonged_inactivity"] = if_no_motion
        time.sleep(SLEEP_TIME)

# **Thread 3: Motion Sensor (Leg Movement Check)**
def motion_sensor_monitor():
    while True:
        if_no_motion = motion_sensor.update_if_inactive()
        with data_lock:
            shared_data["no_leg_motion"] = if_no_motion
        time.sleep(SLEEP_TIME)

# **Thread 4: LED Light Control**
def led_control():
    while True:
        with data_lock:
            sitting_status = shared_data["sitting_status"] 
            user_stands_up = shared_data["user_stands_up"]
        if user_stands_up:
            led_red.off()
            led_green.off()
        elif sitting_status > 0: # Good sitting position
            led_red.off()
            led_light_control(0.0, sitting_status, None) # dim green
        else: # Bad sitting position
            led_green.off()
            led_light_control(abs(sitting_status), 0.0, None)
        time.sleep(SLEEP_TIME)

# **Thread 5: Speaker Alert**
def speaker_alert():
    while True:
        with data_lock:
            if shared_data["sitting_status"] == "Incorrect":
                os.system("aplay alert_sound.wav")  # Replace with actual sound file
        time.sleep(SLEEP_TIME)  # Avoid continuous sound spam

# **Main Function**
def main():
    try:
        # Create threads
        threads = [
            threading.Thread(target=sitting_position_monitor),
            threading.Thread(target=shock_sensor_monitor),
            threading.Thread(target=motion_sensor_monitor),
            threading.Thread(target=led_control),
            threading.Thread(target=speaker_alert)
        ]

        # Start threads
        for thread in threads:
            thread.daemon = True  # Ensures threads stop when the main program exits
            thread.start()

        while True:
            time.sleep(1)  # Keep the main program running

    except KeyboardInterrupt:
        print("Exiting program...")
        GPIO.cleanup()  # Cleanup GPIO on exit
        if arduino:
            arduino.close()

if __name__ == "__main__":
    main()
