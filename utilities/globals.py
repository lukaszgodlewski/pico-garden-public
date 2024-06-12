global_client = None
global_wlan = None
global_relay_schedule = None
global_relay_1 = None
global_relay_2 = None
global_relay_3 = None
global_relay_4 = None
global_relay_state = None
global_temp_hug_sensor = None
global_soil_moisture_1 = None
global_soil_moisture_2 = None
global_soil_moisture_3 = None
global_sensor_1 = None
global_sensor_2 = None
global_sensor_3 = None
global_rtc = None 
global_hex_id = None
global_cpu_temp_sensor = None
global_cpu_temp_reading = None
global_wdt = None
global_register_flag = True
global_mqtt_username = None
global_mqtt_server_ip = None
global_mqtt_server_port = None
global_api_key = None
global_secret_key = None

global_relay_states = {
    'RELAY_1': {
        'manual_override': False, 
        'override_task': None,
        'state': True if global_relay_1 is not None and global_relay_1.value() == 0 else False,
        'last_on': None,
        'last_off': None,
        'schedule_work': None,
        'manual_work': None,
        },
    
    'RELAY_2': {
        'manual_override': False,
        'override_task': None,
        'state': True if global_relay_2 is not None and global_relay_2.value() == 0 else False,
        'last_on': None,
        'last_off': None,
        'schedule_work': None,
        'manual_work': None,
        },

    'RELAY_3': {
        'manual_override': False,
        'override_task': None,
        'state': True if global_relay_3 is not None and global_relay_3.value() == 0 else False,
        'last_on': None,
        'last_off': None,
        'schedule_work': None,
        'manual_work': None,
        },
    
    'RELAY_4': {
        'manual_override': False,
        'override_task': None,
        'state': True if global_relay_4 is not None and global_relay_4.value() == 0 else False,
        'last_on': None,
        'last_off': None,
        'schedule_work': None,
        'manual_work': None,
        },
}