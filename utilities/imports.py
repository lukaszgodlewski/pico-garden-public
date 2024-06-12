import globals
import sys
import gc
sys.path.insert(0, '/hardware')
sys.path.insert(0, '/network')
#sys.path.insert(0, '/lib')
sys.path.insert(0, '/utilities')
import devices_list
import config
from time import sleep
import urequests
import connection
from machine import Pin, SoftI2C, WDT
import dht20
import utime
import hardware_config
import ds1307
import logging
import schedule
import utilities
import network
import ujson
import uasyncio as asyncio
import usocket as socket
import buttons
from umqtt.simple import MQTTClient
import ubinascii
import machine
import micropython
import json_helpers
import functions
import capaitive_soil