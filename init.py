from imports import *

async def init():
   
    ### MANUAL RUN GC
    gc.enable()

    ### SCHEDULE
#     globals.global_relay_schedule = schedule.globals.global_relay_schedule
    
    ### COMPONENTS
    globals.global_relay_1 = hardware_config.RELAY_1
    globals.global_relay_2 = hardware_config.RELAY_2
    globals.global_relay_3 = hardware_config.RELAY_3
    globals.global_relay_4 = hardware_config.RELAY_4
    
    globals.global_sensor_1 = hardware_config.SOIL_MOISTURE_1
    globals.global_sensor_2 = hardware_config.SOIL_MOISTURE_2
    globals.global_sensor_3 = hardware_config.SOIL_MOISTURE_3
    
    globals.global_temp_hug_sensor = hardware_config.TEMP_HUM_SENSOR
    globals.global_rtc = ds1307.DS1307(hardware_config.RTC_I2C)
    globals.global_cpu_temp_sensor = hardware_config.CPU_TEMP_SENSOR
    
    ### WLAN
    globals.global_wlan = connection.WlanConnection(config.SSID, config.PASSWORD)
    globals.global_wlan.connectWifi()

    try:
        if globals.global_wlan.check_server_availability(config.GARDEN_SERVER_IP, config.GARDEN_SERVER_PORT) and network.WLAN(network.STA_IF).isconnected():
            await functions.register_device()
            globals.global_client = MQTTClient(globals.global_hex_id, globals.global_mqtt_server_ip, port=globals.global_mqtt_server_port, user=globals.global_mqtt_username, password=config.MQTT_PASSWORD)
            globals.global_client.set_callback(sub_callback)
            lwt_message = f"{globals.global_hex_id}".encode("utf-8")
            globals.global_client.set_last_will(config.TOPIC, lwt_message, retain=True, qos=1)
            globals.global_client.connect()
            globals.global_client.subscribe(config.RELAY_1_TOPIC)
            globals.global_client.subscribe(config.RELAY_2_TOPIC)
            globals.global_client.subscribe(config.RELAY_3_TOPIC)
            print(f"Connected to {globals.global_mqtt_server_ip}, subscribed to relay topics")

    except Exception as e:
        print(f"Error init: {e}")


async def check_and_turn_off_relays():
    await functions.check_and_turn_off_relays()
        
async def get_average_soil_moisture_reading():
    await functions.get_average_soil_moisture_reading()

async def feed_watchdog():
    await functions.feed_watchdog()
    
async def get_cpu_temp():
    await functions.get_cpu_temp()
    
async def send_data_sensors_to_db():
    await functions.send_data_sensors_to_db()

def sub_callback(topic, msg):
    functions.sub_callback(topic, msg)

async def check_connection():
    if network.WLAN(network.STA_IF).isconnected(): 
        try:
            server_available = globals.global_wlan.check_server_availability(config.GARDEN_SERVER_IP, config.GARDEN_SERVER_PORT)
            return server_available
        except Exception as e:
            print(f"Check server: {e}")
    return False
    
async def check_hour():
    await functions.check_hour()

async def mqtt_sender():
    await functions.mqtt_sender()
    
async def mqtt_receiver():
    while True:
        globals.global_client.check_msg()
        await asyncio.sleep(1)