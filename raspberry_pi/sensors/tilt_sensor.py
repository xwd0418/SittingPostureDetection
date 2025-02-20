from gpiozero import Button
import time

# The input pin to which the sensor is connected is declared here.
# The button object uses the internal pull-up resistor of the Pi.
sensor = Button(25, pull_up=True)

print("Sensor test [press CTRL+C to end the test]")

# This output function is executed when a signal is detected
def ausgabeFunktion():
    print("Signal recognized")

# When a signal is detected (falling signal edge), the output function is triggered
sensor.when_pressed = ausgabeFunktion

# Main program loop
try:
    while True:
        time.sleep(1)

# Clean-up work after the program has been completed
except KeyboardInterrupt:
    print("Program terminated")
