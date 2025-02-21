from gpiozero import PWMLED
import time

# # PWMLED instances for each LED
led_red = PWMLED(24)
led_green = PWMLED(23)

# This function generates the actual color
# The color intensity can be changed using the respective color variable
# After the color has been set, "time.sleep" is used to define the time for which the color in question is to be displayed
def led_light_control(red, green, pause):
    led_red.value = red
    led_green.value = green
    if pause == None:
        return
    time.sleep(pause)

    # Switch off LEDs after the pause
    led_red.value = 0
    led_green.value = 0

if __name__ == "__main__":    
    print("LED test [press CTRL+C to end the test]")
    
    led_light_control(0.0, 0.01, 2) # dim green
    # led_light_control(0.0, 0.5, 2) # bright green
    # led_light_control(0.01, 0.0, 2) # dim red
    # led_light_control(0.5, 0.0, 2) # bright red
    
    led_red.on()
    time.sleep(2)
    led_red.off()
    led_green.on()
    time.sleep(2)
    led_green.off()
