import ujson

def generate_device_data_json(sensor_list, relay_list, hex_id, api_key):
    device_data = {
        "api_key": api_key,
        "unique_id": hex_id,
        "sensors": {},
        "relays": {},
        }
    for sensor in sensor_list:
        device_data["sensors"][sensor["name"]] = sensor
    for relay in relay_list:
        device_data["relays"][relay["name"]] = relay
    return ujson.dumps(device_data)

def generate_device_data_json_for_database(sensor_list, hex_id, api_key):
    device_data = {
        "api_key": api_key,
        "unique_id": hex_id,
        "sensors": {},
        }
    for sensor in sensor_list:
        device_data["sensors"][sensor["name"]] = sensor
    return ujson.dumps(device_data)


def update_device_value(device_name, new_value, sensor_list=None, relay_list=None, cpu_temp=None):
    if sensor_list is not None:
        for sensor in sensor_list:
            if sensor["name"] == device_name:
                sensor["value"] = new_value
                break

    if relay_list is not None:
        for relay in relay_list:
            if relay["name"] == device_name:
                relay["value"] = new_value
                break

    