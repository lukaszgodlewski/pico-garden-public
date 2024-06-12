import globals
import sys
sys.path.insert(0, '/utilities')

import network
import ujson
import devices_list
import json_helpers
import config
import urequests
import asyncio
import gc
import capaitive_soil
import machine
import ujson

async def register_device():
    try:
        url = config.REGISTER_DEVICE_ENDPOINT
        payload = {
            "unique_id": globals.global_hex_id,
            "api_key": globals.global_api_key,
            "secret_key": globals.global_secret_key
        }
        response = urequests.post(
            url, 
            headers={'Content-Type': 'application/json'}, 
            data=ujson.dumps(payload)
        )
        if response.status_code == 200 or response.status_code == 220:
            details = ujson.loads(response.content).get("detail", {})
            globals.global_mqtt_username = details.get("MQTT_USERNAME")
            globals.global_mqtt_server_ip = details.get("MQTT_BROKER")
            globals.global_mqtt_server_port = details.get("MQTT_PORT")
            print(details)
            globals.global_register_flag = True
            return
        elif response.status_code == 222:
            print(f"No user with that api_key.")
            globals.global_register_flag = False
            return

        else:
            print(f"Failed to fetch initial data: {response.status_code}")
        response.close()
    except Exception as e:
        print(f"An error occurred while fetching initial data: {e}")
        

async def check_connection():
    if network.WLAN(network.STA_IF).isconnected(): 
        try:
            server_available = globals.global_wlan.check_server_availability(config.GARDEN_SERVER_IP, config.GARDEN_SERVER_PORT)
            return server_available
        except Exception as e:
            print(f"Check server: {e}")
    return False

async def feed_watchdog():
    globals.global_wdt = machine.WDT(timeout=8388)
    while True:
        globals.global_wdt.feed()
        await asyncio.sleep(2)

def create_status_message(status, origin):
    status_message = {
        "status": status,
        "origin": origin
    }
    return ujson.dumps(status_message)

def turn_off_relay(relay_name):
    if relay_name == 'RELAY_1':
        globals.global_relay_1.value(1)
        globals.global_relay_4.value(1)
    elif relay_name == 'RELAY_2':
        globals.global_relay_2.value(1)
        globals.global_relay_4.value(1)
    elif relay_name == 'RELAY_3':
        globals.global_relay_3.value(1)
        globals.global_relay_4.value(1)
        

async def check_and_turn_off_relays():
    while True:
        now = globals.global_rtc.datetime()
        current_time_in_seconds = now[4] * 3600 + now[5] * 60 + now[6]
        
        for relay_name, relay_state in globals.global_relay_states.items():
            if relay_state['state'] is not None and relay_state['last_on'] is not None:
                last_activated_in_seconds = relay_state['last_on'][4] * 3600 + relay_state['last_on'][5] * 60 + relay_state['last_on'][6]
                if not relay_state['schedule_work'] and current_time_in_seconds - last_activated_in_seconds > 20 and relay_state['state'] == True:
                    print(f"{relay_name} is being turned off due to security reasons.")
                    topic = getattr(config, f"{relay_name}_TOPIC_CALLBACK")
                    globals.global_client.publish(topic, create_status_message("false", "machine"))
                    turn_off_relay(relay_name)
                    relay_state['state'] = False
        await asyncio.sleep(10)


def prepare_data():
    sensor_list = devices_list.SENSORS_LIST
    relays_list = devices_list.RELAYS_LIST
    json_helpers.update_device_value(devices_list.TEMPERATURE_SENSOR["name"], str(globals.global_temp_hug_sensor.measurements['t']), sensor_list=sensor_list)
    json_helpers.update_device_value(devices_list.HUMIDITY_SENSOR["name"], str(globals.global_temp_hug_sensor.measurements['rh']), sensor_list=sensor_list)
    json_helpers.update_device_value(devices_list.CPU_SENSOR["name"], str(globals.global_cpu_temp_reading), sensor_list=sensor_list)
    json_helpers.update_device_value(devices_list.SOIL_MOISTURE_1["name"], str(globals.global_soil_moisture_1), sensor_list=sensor_list)
    json_helpers.update_device_value(devices_list.SOIL_MOISTURE_2["name"], str(globals.global_soil_moisture_2), sensor_list=sensor_list)
    json_helpers.update_device_value(devices_list.SOIL_MOISTURE_3["name"], str(globals.global_soil_moisture_3), sensor_list=sensor_list)
    json_helpers.update_device_value(devices_list.RELAY_1["name"], "true" if globals.global_relay_1.value() == 0 else "false", relay_list=relays_list)
    json_helpers.update_device_value(devices_list.RELAY_2["name"], "true" if globals.global_relay_2.value() == 0 else "false", relay_list=relays_list)
    json_helpers.update_device_value(devices_list.RELAY_3["name"], "true" if globals.global_relay_3.value() == 0 else "false", relay_list=relays_list)

    json_output = json_helpers.generate_device_data_json(sensor_list, relays_list, globals.global_hex_id, config.API_KEY)
    return json_output


def prepare_data_for_db():
    sensor_list = devices_list.SENSORS_LIST
    relays_list = devices_list.RELAYS_LIST
    json_helpers.update_device_value(devices_list.TEMPERATURE_SENSOR["name"], str(globals.global_temp_hug_sensor.measurements['t']), sensor_list=sensor_list)
    json_helpers.update_device_value(devices_list.HUMIDITY_SENSOR["name"], str(globals.global_temp_hug_sensor.measurements['rh']), sensor_list=sensor_list)
    json_helpers.update_device_value(devices_list.SOIL_MOISTURE_1["name"], str(globals.global_soil_moisture_1), sensor_list=sensor_list)
    json_helpers.update_device_value(devices_list.SOIL_MOISTURE_2["name"], str(globals.global_soil_moisture_2), sensor_list=sensor_list)
    json_helpers.update_device_value(devices_list.SOIL_MOISTURE_3["name"], str(globals.global_soil_moisture_3), sensor_list=sensor_list)
    
    json_db = json_helpers.generate_device_data_json_for_database(sensor_list, globals.global_hex_id, config.API_KEY)
    return(json_db)

async def send_data_sensors_to_db():
    while True:
        try:
            url = config.DB_UPDATE_SENSORS_ENDPOINT
            data = prepare_data()
            response = urequests.post(url, headers={'Content-Type': 'application/json'}, data=data)
            if response.status_code == 200:
                print("Data sensors has been sent..")
                print(data)
            else:
                print(f"Data cannot be sent: {response.status_code} {response.text}")
        except Exception as e:
            print(f"Something went wrong: {e}")
        finally:
            response.close()
            
        await asyncio.sleep(60 * 60)
        

async def check_hour():
    while True:
        gc.collect()
        current_time = globals.global_rtc.datetime()
        print(f"{current_time[4]}:{current_time[5]}:{current_time[6]}")
        await asyncio.sleep_ms(5000)
        

def sub_callback(topic, msg):
    relay = None
    print(msg)
    relay_map = {
        'RELAY_1': globals.global_relay_1,
        'RELAY_2': globals.global_relay_2,
        'RELAY_3': globals.global_relay_3,
        'RELAY_4': globals.global_relay_4,
    }
    relay_part = topic.decode().split("/")[1]
    relay = relay_map.get(relay_part)
    
    if relay:
        if msg.decode() == "true":
            relay.value(0)
            globals.global_relay_states[relay_part]['manual_override'] = True
            globals.global_relay_states[relay_part]['state'] = True
            globals.global_relay_states[relay_part]['last_on'] = globals.global_rtc.datetime()
            topic = getattr(config, f"{relay_part}_TOPIC_CALLBACK")
            globals.global_client.publish(topic, create_status_message("true", "web_app"))
            
            if relay_part in ['RELAY_1', 'RELAY_2', 'RELAY_3']:
                globals.global_relay_4.value(0)
            
        else:
            relay.value(1)
            globals.global_relay_states[relay_part]['manual_override'] = False
            globals.global_relay_states[relay_part]['state'] = False
            globals.global_relay_states[relay_part]['last_on'] = globals.global_rtc.datetime()
            topic = getattr(config, f"{relay_part}_TOPIC_CALLBACK")
            globals.global_client.publish(topic, create_status_message("false", "web_app"))
            
            all_closed = all(not state['state'] for key, state in globals.global_relay_states.items() if key in ['RELAY_1', 'RELAY_2', 'RELAY_3'])
            if all_closed:
                globals.global_relay_4.value(1)

    print((topic, msg))
    
    
async def get_cpu_temp():
    while True:
        reading = globals.global_cpu_temp_sensor.read_u16() * (3.3 / 65535) 
        globals.global_cpu_temp_reading = 27 - (reading - 0.706) / 0.001721
        print(globals.global_cpu_temp_reading)
        await asyncio.sleep(10)
        
        
async def get_average_soil_moisture_reading():
    while True:
        globals.global_soil_moisture_1, globals.global_soil_moisture_2, globals.global_soil_moisture_3 = await asyncio.gather(
            capaitive_soil.get_soil_moisture(globals.global_sensor_1),
            capaitive_soil.get_soil_moisture(globals.global_sensor_2),
            capaitive_soil.get_soil_moisture(globals.global_sensor_3),
        )
        print("1 ", globals.global_soil_moisture_1, "2 ", globals.global_soil_moisture_2, "3 ", globals.global_soil_moisture_3)
        await asyncio.sleep(5)

async def turn_on_relay_by_schedule():
    while True:
        current_time = globals.global_rtc.datetime()
        current_hour_minute = (current_time[4], current_time[5])
        gc.collect()
        for schedule in globals.global_relay_schedule:
            relay_id = schedule['id']
            start_time = schedule['start']
            end_time = schedule['end']

            if not globals.global_relay_states[relay_id]['manual_override']:
                if start_time <= current_hour_minute <= end_time:
                    globals.global_relay_states['RELAY_1']['schedule_work'] = True
                    print(f"Turning on {relay_id} by schedule.")
                    globals.global_relay_1.value(0)
#                     globals.global_client.publish(config.RELAY_1_TOPIC_CALLBACK , {"state" : "true"})
#                     globals.global_client.publish(config.RELAY_2_TOPIC_CALLBACK , {"state" : "true"})

                else:
                    globals.global_relay_states['RELAY_1']['schedule_work'] = False
                    print(f"Turning off {relay_id} by schedule.")
                    globals.global_relay_1.value(1)
#                     globals.global_client.publish(config.RELAY_1_TOPIC_CALLBACK , {"state" : "false"})
#                     globals.global_client.publish(config.RELAY_2_TOPIC_CALLBACK , {"state" : "true"})

        await asyncio.sleep(10)

async def mqtt_sender():
    while True: 
        globals.global_client.publish(config.TOPIC, prepare_data())
        print("send")
        await asyncio.sleep(5)