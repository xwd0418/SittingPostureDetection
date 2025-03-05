import threading
import time,sys
import RPi.GPIO as GPIO
sys.path.append('/home/xw0418/venv/lib/python3.11/site-packages')
import os  # For speaker sound execution

from sensors.arduinonNano33BleSense import arduino_sensor  
from sensors.sonar import sonar_sensor
# from sensors.motion_sensor import motion_sensor
from sensors.LED import led_red, led_green, led_light_control
# from sensors.speaker import speaker
# 
from utils.utils import recorder
posture_recorder = recorder("/home/xw0418/cse237A/SittingPostureDetection/data/audio/posture_alert.mp3", 6)
distance_recorder = recorder("/home/xw0418/cse237A/SittingPostureDetection/data/audio/distance_alert.mp3", 30)

SLEEP_TIME = 0.1  # 0.1 second

# Shared Variables with Thread Lock
shared_data = {
    "bad_sitting_status": 0,  # should be a float number from 0 to 1. 1 means bad, 0 mean good
    "bad_desk_distance": 0,
    # "prolonged_inactivity": 0,    # 0 means ok, 1 means prolonged inactivity
    # "no_leg_motion": 0,  # 0 means ok, 1 means no leg motion
    "user_stands_up": 0  # 0 means user is sitting, 1 means user stands up
}
data_lock = threading.Lock()



# **Thread 1: Arduino BLR Sitting Position Check**
def sitting_position_monitor():
    while True:
        bad_sitting_status  = arduino_sensor.update_seat_status()
        if bad_sitting_status is None:
            continue
        with data_lock:
            shared_data["bad_sitting_status"] = max(bad_sitting_status-0.5, 0) #/0.6 
            shared_data["user_stands_up"] = arduino_sensor.standing
            # print(f"Sitting Status: {bad_sitting_status}")
        # time.sleep(SLEEP_TIME)
        posture_recorder.record(1 if shared_data["bad_sitting_status"] else 0)
        with data_lock:
            print(posture_recorder.data, posture_recorder.curr_sum)
            posture_recorder.check()

# **Thread 2: Shock Sensor (Seat Departure Detection)**
def sonar_monitor():
    while True:
        distance = sonar_sensor.distance
        # print(f"Distance: {distance} cm")
        if distance > 10:
            bad_desk_distance = 0
        else:
            bad_desk_distance = (10 - distance)/10

        with data_lock:
            shared_data["bad_desk_distance"] = bad_desk_distance
        # distance_recorder.record(1 if bad_desk_distance else 0)
        # with data_lock:
        #     distance_recorder.check()
        time.sleep(0.2)

# # **Thread 3: Motion Sensor (Leg Movement Check)**
# def motion_sensor_monitor():
#     while True:
#         if_no_motion = motion_sensor.update_if_inactive()
#         with data_lock:
#             shared_data["no_leg_motion"] = if_no_motion
#         time.sleep(SLEEP_TIME)

# **Thread 4: LED Light Control**
def led_control():
    while True:
        with data_lock:
            bad_sitting_status = shared_data["bad_sitting_status"] 
            bad_desk_distance = shared_data["bad_desk_distance"]
            user_stands_up = shared_data["user_stands_up"]
        if user_stands_up:
            led_red.off()
            led_green.off()
      
        else: # Bad sitting position
            led_green.off()
            led_light_control(bad_sitting_status, bad_desk_distance, None) #red for tilted back, and green for sitting too close
        time.sleep(0.2)

# **Thread 5: Speaker Alert**
def speaker_alert():
    while True:
        with data_lock:
            if shared_data["bad_sitting_status"] == "Incorrect":
                os.system("aplay alert_sound.wav")  # Replace with actual sound file
        time.sleep(SLEEP_TIME)  # Avoid continuous sound spam


# **Main Function**
def main():
    try:
        # Create threads
        threads = [
            threading.Thread(target=sitting_position_monitor),
            threading.Thread(target=sonar_monitor),
            # threading.Thread(target=motion_sensor_monitor),
            threading.Thread(target=led_control),
            # threading.Thread(target=speaker_alert)
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
        arduino_sensor.close()

if __name__ == "__main__":
    main()
