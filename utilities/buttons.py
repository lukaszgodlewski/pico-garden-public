import hardware_config
from machine import Pin, Timer

red_button = hardware_config.RED_BUTTON
green_button = hardware_config.GREEN_BUTTON
relay_1 = hardware_config.RELAY_1

def buttonRelayOff(red_button):
    relay_1.value(1)
    print("Turned off by button.")

def buttonRelayOn(green_button):
    relay_1.value(0)
    print("Turned on by button.")
    
red_button.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler = buttonRelayOff)
green_button.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler = buttonRelayOn)