from machine import ADC
import uasyncio as asyncio
import sys

humidity_in_air = 44570
humidity_in_water = 11178

def calculate_moisture(value):
    value = max(min(value, humidity_in_air), humidity_in_water)
    humidity_percent = (value - humidity_in_water) / (humidity_in_air - humidity_in_water) * 100
    humidity_percent = 100 - humidity_percent
    return humidity_percent

async def get_soil_moisture(sensor):
    data = []
    for _ in range(5):
        data.append(sensor.read_u16())
        await asyncio.sleep(1)
    average_reading = sum(data) / len(data)
    return calculate_moisture(average_reading)
