from gpiozero import Button
import time

# The input pin to which the sensor is connected
sensor = Button(18, pull_up=True)  # GPIO 18

print("Sensor test [press CTRL+C to end the test]")

try:
    while True:
        if sensor.is_pressed:
            print("LOW")  # Signal detected
        else:
            print("HIGH")  # No signal detected
        time.sleep(0.5)  # Adjust sleep time as needed

except KeyboardInterrupt:
    print("Program terminated")
