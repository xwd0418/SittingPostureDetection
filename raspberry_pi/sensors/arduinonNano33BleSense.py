import serial
import time

arduino_port = "/dev/ttyACM0"
baud_rate = 115200

try:
    ser = serial.Serial(arduino_port, baud_rate, timeout=1)
    time.sleep(2)

    print("Connected to Arduino. Listening for data...")
    
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            print(f"Received: {line}")

except serial.SerialException as e:
    print(f"Error: {e}")

except KeyboardInterrupt:
    print("Stopped by User")
finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()
