import os, subprocess, sys
# from models.posture_data import PostureData
sys.path.append('/home/xw0418/venv/lib/python3.11/site-packages')

# from playsound3 import playsound

# playsound("/home/xw0418/cse237A/SittingPostureDetection/data/audio/posture_alert.mp3")

posture = True
distance = False

if __name__ == "__main__":
    if (posture):
        # Play the posture alert audio
        # subprocess.call("mpg123 /home/xw0418/cse237A/SittingPostureDetection/data/audio/posture_alert.mp3", shell=True)
        # os.system("mpg123 -o alsa /home/xw0418/cse237A/SittingPostureDetection/data/audio/posture_alert.mp3")
        os.system("mpg123 /home/xw0418/cse237A/SittingPostureDetection/data/audio/distance_alert.mp3")
        # os.system("sudo XDG_RUNTIME_DIR=/run/user/$(id -u) DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/$(id -u)/bus PULSE_SERVER=unix:/run/user/$(id -u)/pulse/native python test-audio.py")
    if (distance):
        # Play the distance alert audio
        os.system("mpg123 /home/xw0418/cse237A/SittingPostureDetection/data/audio/distance_alert.mp3")