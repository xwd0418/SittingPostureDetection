from gpiozero import Button
import time

# The input pin to which the sensor is connected is declared here.
# The button object uses the internal pull-up resistor of the Pi.
sensor = Button(4, pull_up=True)

class ShockSensor:
    def __init__(self):
        self.sensor = sensor

    @property
    def is_pressed(self):
        return sensor.is_pressed

shock_sensor = ShockSensor()






if __name__ == "__main__":

    print("sensor test [press CTRL+C to end the test]")
    print("sensor test [press CTRL+C to end the test]")
    
    try:
        while True:
            if sensor.is_pressed:
                print("LOW")  # Signal detected
                
            # else:
            #     print("HIGH")  # No signal detected
            # # time.sleep(0.1)  # Adjust sleep time as needed

    except KeyboardInterrupt:
        print("Program terminated")
