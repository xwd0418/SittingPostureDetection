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
from test.PubSub import init_mqtt
mqtt_connection, message_count, message_topic, message_string = init_mqtt()
publish_count = 1


# Shared Variables with Thread Lock
shared_data = {
    "device_id": "Raspberry Pi",
    "bad_sitting_status": 0,  # should be a float number from 0 to 1. 1 means bad, 0 mean good
    "bad_desk_distance": 0,
    # "prolonged_inactivity": 0,    # 0 means ok, 1 means prolonged inactivity
    # "no_leg_motion": 0,  # 0 means ok, 1 means no leg motion
    "user_stands_up": 0 , # 0 means user is sitting, 1 means user stands up
    "audio_is_playing": False,
    "audio_finish_time": 0
}
posture_recorder = recorder("/home/xw0418/cse237A/SittingPostureDetection/data/audio/posture_alert.mp3", 15, shared_data)
distance_recorder = recorder("/home/xw0418/cse237A/SittingPostureDetection/data/audio/distance_alert.mp3", 15, shared_data)
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

        if shared_data['user_stands_up']:
            posture_recorder.reset()
            continue
        posture_recorder.record(1 if shared_data["bad_sitting_status"] else 0)
        
        if shared_data['audio_is_playing']:
            if time.time() < shared_data["audio_finish_time"]:
                posture_recorder.reset()
                continue
            else:
                with data_lock:
                    shared_data["audio_is_playing"] = False
            
        audio_is_playing = posture_recorder.check()
        
        with data_lock:
            if shared_data["bad_sitting_status"]:
                print("posture data: ", posture_recorder.data, posture_recorder.curr_sum)
            if audio_is_playing:
                shared_data["audio_finish_time"] = time.time() + 1
                shared_data["audio_is_playing"] = True
                posture_recorder.reset()
            
                

# **Thread 2: Shock Sensor (Seat Departure Detection)**
def sonar_monitor():
    while True:
        if shared_data['user_stands_up']:
            distance_recorder.reset()
            continue 
        distance = sonar_sensor.distance
        # print(f"Distance: {distance} cm")
        if distance > 10:
            bad_desk_distance = 0
        else:
            bad_desk_distance = (10 - distance)/10

        with data_lock:
            shared_data["bad_desk_distance"] = bad_desk_distance
            
        distance_recorder.record(1 if bad_desk_distance else 0)
        if shared_data['audio_is_playing']:
            if time.time() < shared_data["audio_finish_time"]:
                distance_recorder.reset()
                continue
            else:
                with data_lock:
                    shared_data["audio_is_playing"] = False
        
        audio_is_playing = distance_recorder.check()
        with data_lock:
            if shared_data["bad_desk_distance"]:
                print("distance data: ", distance_recorder.data, distance_recorder.curr_sum)
            # print(posture_recorder.data, posture_recorder.curr_sum)
            if audio_is_playing:
                shared_data["audio_is_playing"] = True
                shared_data["audio_finish_time"] = time.time() + 1
                distance_recorder.reset()
                
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
        time.sleep(0.1)

from awscrt import mqtt, http


# **Main Function**
def main():
    
    try:
        # Create threads
        threads = [
            threading.Thread(target=sitting_position_monitor),
            threading.Thread(target=sonar_monitor),
            # threading.Thread(target=motion_sensor_monitor),
            threading.Thread(target=led_control),
        ]

        # Start threads
        for thread in threads:
            thread.daemon = True  # Ensures threads stop when the main program exits
            thread.start()

        mqtt_connection, message_count, message_topic, message_string = init_mqtt()
        import json
        # sample_data = {"hi":1}
        # sample_data_json = json.dumps(sample_data, indent=4)

        if message_string:
            publish_count = 1
            while (publish_count <= message_count) or (message_count == 0):
                mqtt_connection.publish(
                    topic=message_topic,
                    payload=json.dumps(shared_data, indent=4)
,
                    qos=mqtt.QoS.AT_LEAST_ONCE)
                time.sleep(10)
                publish_count += 1

    except KeyboardInterrupt:
        print("Exiting program...")
        GPIO.cleanup()  # Cleanup GPIO on exit
        arduino_sensor.close()

if __name__ == "__main__":
    main()
    
