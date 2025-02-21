import serial
import time, struct

arduino_port = "/dev/ttyACM0"
baud_rate = 115200
ser = serial.Serial(arduino_port, baud_rate, timeout=1)

class AduinoSense:
    def __init__(self):
        self.ser = ser

    def read_data(self):
        num_floats = 3
        byte_size = num_floats * 4  # 3 floats, each 4 bytes

        data = ser.read(byte_size)  

        if len(data) == byte_size:  # Ensure we received the expected number of bytes
            pitch, roll, tilt = struct.unpack('fff', data)
            if -180<pitch<180 and -180<roll<180 and -180<tilt<180:
                return pitch, roll, tilt
        return None

    def close(self):
        ser.close()
        
        
arduino_sensor = AduinoSense() 

if __name__ == "__main__":
    try:

        time.sleep(2)

        print("Connected to Arduino. Listening for data...")
        
        while True:
            data = arduino_sensor.read_data()
            if data:
                pitch, roll, tilt = data
                print(f"Pitch: {pitch:.2f}, Roll: {roll:.2f}, Tilt: {tilt:.2f}")
        

    except serial.SerialException as e:
        print(f"Error: {e}")

    except KeyboardInterrupt:
        print("Stopped by User")
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()
