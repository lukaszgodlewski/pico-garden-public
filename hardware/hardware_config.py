from machine import Pin, SoftI2C, Timer, ADC
import dht20
from time import sleep

RELAY_1 = Pin(16, Pin.OUT)
RELAY_2 = Pin(17, Pin.OUT)
RELAY_3 = Pin(18, Pin.OUT)
RELAY_4 = Pin(19, Pin.OUT)
TEMP_HUM_SENSOR = dht20.DHT20(56, SoftI2C(sda=Pin(4), scl=Pin(5), freq=200000))
RTC_I2C = SoftI2C(sda=Pin(20), scl=Pin(21), freq=200000)
RED_BUTTON = Pin(0, Pin.IN, Pin.PULL_UP)
YELLOW_BUTTON = Pin(1, Pin.IN, Pin.PULL_UP)
GREEN_BUTTON = Pin(2, Pin.IN, Pin.PULL_UP)


SOIL_MOISTURE_1 = ADC(Pin(26))
SOIL_MOISTURE_2 = ADC(Pin(27))
SOIL_MOISTURE_3 = ADC(Pin(28))

RELAY_1.value(1)
RELAY_2.value(1)
RELAY_3.value(1)
RELAY_4.value(1)

CPU_TEMP_SENSOR = ADC(4)
