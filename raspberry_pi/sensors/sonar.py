from gpiozero import OutputDevice, InputDevice
import time

class UltrasonicSensor:
    def __init__(self, trigger_pin=4, echo_pin=18):
        # Set up trigger and echo pins using gpiozero
        self.trigger = OutputDevice(trigger_pin)
        self.echo = InputDevice(echo_pin)
        
    @property
    def distance(self):
        # Send a 10us pulse to trigger pin to start the measurement
        self.trigger.off()  # Make sure trigger is LOW
        time.sleep(0.1)  # Delay to ensure trigger pin is LOW before triggering
        self.trigger.on()  # Send a HIGH pulse to trigger
        time.sleep(0.00001)  # Pulse for 10us
        self.trigger.off()  # Set trigger pin back to LOW
        
        # Wait for echo pin to go HIGH, then start measuring time
        while not self.echo.is_active:
            pulse_start = time.time()
        
        while self.echo.is_active:
            pulse_end = time.time()
        
        # Calculate the distance in cm
        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150  # Speed of sound = 34300 cm/s (divide by 2 to get distance)
        distance = round(distance, 2)
        
        return distance

# Example usage
sonar_sensor = UltrasonicSensor()

if __name__ == "__main__":
    # Read distance
    try:
        while True:
            print("Distance:", sonar_sensor.distance, "cm")
            time.sleep(1)
    except KeyboardInterrupt:
        print("Program terminated.")
