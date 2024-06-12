import machine
import network
from time import sleep
import usocket as socket
import utime

class WlanConnection():
    attempts = 0
    def __init__(self, ssid: str, password: str):
        self._ssid = ssid
        self._password = password
        
    def connectWifi(self):
        attemps = 0
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.connect(self._ssid, self._password)
        while wlan.isconnected() == False and attemps < 50:
            print("Waiting for connection...")
            sleep(1)
            attemps = attemps + 1
            print(attemps)
        if(wlan.isconnected() == False):
            print("No connection")
        else:
            ip = wlan.ifconfig()[0]
            print(f'Connected on {ip}')
    
    def check_server_availability(self, host, port):
        try:
            addr = socket.getaddrinfo(host, port)[0][-1]
            s = socket.socket()
            s.connect(addr)
            del addr
            del s
            return True
        except OSError as e:
            print(f"Error: {e}")
            del e
            utime.sleep(5)

