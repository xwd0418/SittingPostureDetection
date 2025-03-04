# This script uses gTTS (Google Text-to-Speech) to convert text to speech and play it on the Raspberry Pi.
from gtts import gTTS
import os

distance_text = "Alert! You are sitting too close to the screen. Please move back to a safe distance."
posture_text = "Alert! Your posture is not correct. Please sit up straight."

path_audio = "."
distance_audio_path = "../../data/audio/distance_alert.mp3"
posture_audio_path = "../../data/audio/posture_alert.mp3"

print(distance_audio_path)

def text_to_speech(text, path):
    # Convert the text to speech
    tts = gTTS(text=text, lang='en')
    
    # Save the audio file
    tts.save(path)
    

def play_audio(path):
    # Play the audio file
    os.system(f"mpg123 {path}")

if __name__ == "__main__":
    # Generate and play distance alert audio
    text_to_speech(distance_text, distance_audio_path)
    play_audio(distance_audio_path)

    # Generate and play posture alert audio
    text_to_speech(posture_text, posture_audio_path)
    play_audio(posture_audio_path)
