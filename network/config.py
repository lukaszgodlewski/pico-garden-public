import globals
import ubinascii
import machine

globals.global_hex_id = ubinascii.hexlify(machine.unique_id()).decode('utf-8')

#### WI-FI CRED ####

SSID = ""
PASSWORD = ""

#### GARDEN SERVER ###

GARDEN_SERVER_IP = "" 
GARDEN_SERVER_PORT = 8000 
API_KEY = globals.global_api_key = ""  #### USE API_KEY GENERATED IN GARDEN_APP
SECRET_KEY = globals.global_secret_key = "device3" #### PUT RANDOM CHARACTER STRING HERE AND USE IT AGAIN IN GARDEN_APP IF U WANT ASSIGN THIS DEVICE

#### ENDPOINTS ####

DB_UPDATE_SENSORS_ENDPOINT = f"http://{GARDEN_SERVER_IP}:{GARDEN_SERVER_PORT}/api/device/update_sensors"
REGISTER_DEVICE_ENDPOINT = f"http://{GARDEN_SERVER_IP}:{GARDEN_SERVER_PORT}/api/device/register"

#### MQTT BROKER ####

MQTT_PASSWORD = globals.global_api_key
TOPIC = bytes(f"{globals.global_hex_id}", 'utf-8')
RELAY_1_TOPIC = bytes(f"{globals.global_hex_id}/RELAY_1", 'utf-8')
RELAY_1_TOPIC_CALLBACK = bytes(f"{globals.global_hex_id}/RELAY_1/CALLBACK", 'utf-8')
RELAY_2_TOPIC = bytes(f"{globals.global_hex_id}/RELAY_2", 'utf-8')
RELAY_2_TOPIC_CALLBACK = bytes(f"{globals.global_hex_id}/RELAY_2/CALLBACK", 'utf-8')
RELAY_3_TOPIC = bytes(f"{globals.global_hex_id}/RELAY_3", 'utf-8')
RELAY_3_TOPIC_CALLBACK = bytes(f"{globals.global_hex_id}/RELAY_3/CALLBACK", 'utf-8')
