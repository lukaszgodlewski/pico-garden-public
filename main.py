"""
Asynchronic system of ARM Cortex M0+ for operating relays and collecting information from sensors (pico-garden)
https://github.com/lukaszgodlewski/pico-garden

MIT License
Copyright (c) 2024 Łukasz Godlewski

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import sys
sys.path.insert(0, '/utilities')
from imports import *
import globals
import init

    
async def main():
    while True:
        try:
            await init.init()
            if await init.check_connection():
                if(globals.global_register_flag == True):
                    sender_task = asyncio.create_task(init.mqtt_sender())
                    receiver_task = asyncio.create_task(init.mqtt_receiver())
                    #turn_on_relay_by_schedule_task = asyncio.create_task(turn_on_relay_by_schedule())
                    check_hour_task = asyncio.create_task(init.check_hour())
                    check_and_turn_off_relays_task = asyncio.create_task(init.check_and_turn_off_relays())
                    get_average_soil_moisture_reading_task = asyncio.create_task(init.get_average_soil_moisture_reading())
                    send_data_to_db_task = asyncio.create_task(init.send_data_sensors_to_db())
                    get_cpu_temp_task = asyncio.create_task(init.get_cpu_temp())
                    watchdog_task = asyncio.create_task(init.feed_watchdog())

                    await asyncio.gather(
                        sender_task,
                        receiver_task,
                        #turn_on_relay_by_schedule_task
                        check_hour_task,
                        check_and_turn_off_relays_task,
                        get_average_soil_moisture_reading_task,
                        send_data_to_db_task,
                        get_cpu_temp_task,
                        watchdog_task
                    )
               
            else:
                print("Connection failed. Trying again soon.")
                await asyncio.sleep(10)
        except Exception as e:
            print(f"An error occurred: {e}. Retrying in 10 seconds...")
            await asyncio.sleep(10)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Interrupted')
    finally:
        print('Finalizing. Please wait...')