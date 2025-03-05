import serial
import time, struct

arduino_port = "/dev/ttyACM0"
baud_rate = 115200
ser = serial.Serial(arduino_port, baud_rate, timeout=1)
from pathlib import Path
import sys, os, numpy as np
data_dir = Path(__file__).parent.parent
sys.path.append(str(data_dir.parent))
from data.ML_utils import kfold_split

class AduinoSense:
    def __init__(self):
        self.ser = ser
        self.old_accX = None
        self.old_delta = None
        self.setup_ml_model()
        self.standing = False
        self.dont_change_until = time.time() + 2 # 5 seconds

    def read_data(self):
        num_floats = 6  # 3 floats for pitch, roll, tilt, 3 floats for acceleration
        byte_size = num_floats * 4  # 3 floats, each 4 bytes

        data = ser.read(byte_size)  

        if len(data) == byte_size:  # Ensure we received the expected number of bytes
            pitch, roll, tilt, accX, accY, accZ = struct.unpack('ffffff', data)
            # print(f"Pitch: {pitch:.2f}, Roll: {roll:.2f}, Tilt: {tilt:.2f}")
            if -180<pitch<180 and -180<roll<180 and -180<tilt<180:
                return pitch, roll, tilt, accX, accY, accZ
        return None

    def close(self):
        ser.close()
        
    def setup_ml_model(self):
        from sklearn.neighbors import KNeighborsClassifier

        good_dir = "/home/xw0418/cse237A/SittingPostureDetection/data/dataset/good_posture"
        bad_dir = "/home/xw0418/cse237A/SittingPostureDetection/data/dataset/bad_posture"
        good_files = os.listdir(good_dir)
        bad_files = os.listdir(bad_dir)
        good_matrices = [ np.load(os.path.join(good_dir, gf))  for gf in good_files]
        good_matrices = np.vstack(good_matrices)
        bad_matrices = [ np.load(os.path.join(bad_dir, bf))  for bf in bad_files]
        bad_matrices = np.vstack(bad_matrices)

        for X_train, X_test, y_train, y_test in kfold_split(good_matrices, bad_matrices):
        
            # K-Nearest Neighbors
            self.knn = KNeighborsClassifier(n_neighbors=5)
            self.knn.fit(X_train, y_train)
            break
    
    def update_seat_status(self):
        data = self.read_data()
        if data is None:
            return None
        self.check_stand_or_sit(data)
        prob_bad, prob_good = self.knn.predict_proba(np.array(data[:3]).reshape(1, -1))[0]
        return prob_bad 
    
    def check_stand_or_sit(self, data):
        if time.time() < self.dont_change_until:
            return
        pitch, roll, tilt, accX, accY, accZ = data

        if self.old_accX is not None:
            delta = accX - self.old_accX
            # print(f"Delta: {delta:.2f}")
            if self.old_delta is not None:
                # if delta < -0.1 and old_delta > 0.1:
                #     print(f"Maxima detected")
                # elif delta > 0.1 and old_delta < -0.1:
                #     print(f"Minima detected")
                if abs(self.old_delta-delta) > 0.5:
                    self.standing = not self.standing
                    print(f"{self.standing=}")
                    self.dont_change_until = time.time() + 5
            self.old_delta = delta
        self.old_accX = accX
                
                
arduino_sensor = AduinoSense() 


if __name__ == "__main__":
    try:

        # time.sleep(2)

        # Define states
        ABOVE_ONE = 1    # accX > 1
        BELOW_ONE = 2    # accX < 1 (after being above)
        STABLE = 3       # accX ≈ 1 (stabilized)
        
        kinda_standing = False
        kinda_sitting = False   
        
        # Parameters
        stability_threshold = 0.1  # How close to 1.0 is considered "stable"
        stability_count = 0         # Counter for consecutive stable readings
        required_stable_readings = 3 # Number of readings needed to confirm stability
        
        # Initialize state
        current_state = STABLE
        last_state = STABLE
    
        print("Connected to Arduino. Listening for data...")
        old_accX, old_accY, old_accZ = None, None, None
        old_delta = None
        from collections import deque
        recent_fives = deque(maxlen=5)
        while True:
            data = arduino_sensor.read_data()
            if data:
                pitch, roll, tilt, accX, accY, accZ = data
                # print(f"Pitch: {pitch:.2f}, Roll: {roll:.2f}, Tilt: {tilt:.2f}")
                # calculate derivatives 
                if old_accX is not None:
                    delta = accX - old_accX
                    # print(f"Delta: {delta:.2f}")
                    if old_delta is not None:
                        # if delta < -0.1 and old_delta > 0.1:
                        #     print(f"Maxima detected")
                        # elif delta > 0.1 and old_delta < -0.1:
                        #     print(f"Minima detected")
                        if abs(old_delta-delta) > 0.4:
                            print(f"Maxima detected")
                    old_delta = delta
                old_accX = accX
                print(f"accX: {accX:.2f}, AccY: {accY:.2f}, AccZ: {accZ:.2f}")
                
                
                
                
                
                
                
                # if current_state == STABLE:
                #     last_state = STABLE
                #     if accX > 1.0 + 2*stability_threshold:
                #         print(f"stand up detected")
                #         current_state = ABOVE_ONE
                #     elif accX < 1.0 - 2*stability_threshold:
                #         print(f"sit down detected")
                #         current_state = BELOW_ONE
                #     elif accX > 1.0 + stability_threshold:
                #         if kinda_standing:
                #             print(f"stand up detected")
                #             current_state = ABOVE_ONE
                #             kinda_standing = False
                #         else:     
                #             kinda_standing = True
                #     elif accX < 1.0 - stability_threshold:
                #         if kinda_sitting:
                #             print(f"sit down detected")
                #             current_state = BELOW_ONE
                #             kinda_sitting = False
                #         else:
                #             kinda_sitting = True
                        
                # elif current_state == ABOVE_ONE:
                #     if accX < 1.0 - 2*stability_threshold:
                #         print(f"stable state detected")
                #         current_state = STABLE
                #     elif accX < 1.0 - stability_threshold:
                #         if kinda_sitting:
                #             print(f"stable state detected")
                #             current_state = STABLE
                #         else:
                #             kinda_sitting = True
                        
                        
                # elif current_state == BELOW_ONE:
                #     if accX > 1.0 + 2*stability_threshold:
                #         print(f"stable state detected")
                #         current_state = STABLE
                #     elif accX > 1.0 + stability_threshold:
                #         if kinda_standing:
                #             print(f"stable state detected")
                #             current_state = STABLE
                #         else:
                #             kinda_standing = True
    

        
        # prev_state = None  # Track previous state (None, "sitting", "standing")

        # while True:
        #     data = arduino_sensor.read_data()
        #     if data:
        #         pitch, roll, tilt, accX, accY, accZ = data

        #         # Determine current state
        #         current_state = "sitting" if accX > 0.85 else "standing"

        #         # Print only when there is a transition
        #         if prev_state and current_state != prev_state:
        #             if current_state == "standing":
        #                 print("User stood up 🚶‍♂️")
        #             else:
        #                 print("User sat down 🪑")

        #         prev_state = current_state  # Update previous state
        
        

    except serial.SerialException as e:
        print(f"Error: {e}")

    except KeyboardInterrupt:
        print("Stopped by User")
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()
