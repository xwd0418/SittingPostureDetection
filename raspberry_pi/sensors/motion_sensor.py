from gpiozero import Button
import time

# The input pin to which the sensor is connected
sensor = Button(18, pull_up=True)  # GPIO 18

class MotionSensor:
    def __init__(self):
        self.sensor = sensor

    @property
    def is_pressed(self):
        return sensor.is_pressed
    
motion_sensor = MotionSensor()





if __name__ == "__main__":
# print("sensor test [press CTRL+C to end the test]")

    try:
        while True:
            if sensor.is_pressed:
                print("LOW")  # Signal detected
            else:
                print("HIGH")  # No signal detected
            time.sleep(0.1)  # Adjust sleep time as needed

    except KeyboardInterrupt:
        print("Program terminated")

    # def ausgabeFunktion():
    #     print("Signal recognized")

    # # When a signal is detected (falling signal edge), the output function is triggered
    # sensor.when_pressed = ausgabeFunktion

    # # Main program loop
    # try:
    #     while True:
    #         time.sleep(1)

    # # Clean-up work after the program has been completed
    # except KeyboardInterrupt:
    #     print("Program terminated")
