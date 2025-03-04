import os
# from models.posture_data import PostureData

posture = True
distance = False

if __name__ == "__main__":
    if (posture):
        # Play the posture alert audio
        os.system("mpg123 ../../data/audio/posture_alert.mp3")
    if (distance):
        # Play the distance alert audio
        os.system("mpg123 ../../data/audio/distance_alert.mp3")