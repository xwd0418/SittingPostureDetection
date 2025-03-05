from collections import deque
import os
import time

def play_audio(audio_path):
    os.system(f"mpg123 {audio_path}")
class recorder:
    def __init__(self, audio_path, max_len, sv):
        self.max_len = max_len
        self.data = deque(maxlen=max_len)
        self.curr_sum = 0
        self.audio_path = audio_path
        self.audio_is_playing = False
        self.sv = sv
        
    def record(self, data):
        if len(self.data) == self.max_len:
            self.curr_sum -= self.data.popleft()
        self.data.append(data)
        self.curr_sum += data

    def reset(self):
        self.data.clear()
        self.curr_sum = 0
        
    def check(self):
        if len(self.data) < self.max_len:
            return False
        # print(self.curr_sum, self.max_len)
        if self.curr_sum >=self.max_len*0.8:
            play_audio(self.audio_path)
            return True

if __name__ == "__main__":
    recorder = recorder("/home/xw0418/cse237A/SittingPostureDetection/data/audio/posture_alert.mp3", 6)
    for i in range(10):
        recorder.record(i)
        recorder.check()
        print(recorder.data, recorder.curr_sum)
    print("Done")