'''
  Download latest Blynk library here:
    https://github.com/blynkkk/blynk-library/releases/latest

  Blynk is a platform with iOS and Android apps to control
  Arduino, Raspberry Pi and the likes over the Internet.
  You can easily build graphic interfaces for all your
  projects by simply dragging and dropping widgets.

    Downloads, docs, tutorials: http://www.blynk.cc
    Sketch generator:           http://examples.blynk.cc
    Blynk community:            http://community.blynk.cc
    Follow us:                  http://www.fb.com/blynkapp
                                http://twitter.com/blynk_app

  Blynk library is licensed under MIT license
  This example code is in public domain.

 *************************************************************
  Attention! Please check out TinyGSM guide:
    https://tiny.cc/tinygsm-readme

  Change GPRS apm, user, pass, and Blynk auth token to run :)
  Feel free to apply it to any other example. It's simple!
'''

import BlynkLib
import network
import machine
import time

# Fill in information from Blynk Device Info here
WIFI_SSID = 'LilyGo-AABB'
WIFI_PASS = 'xinyuandianzi'
BLYNK_AUTH = 'MSuP9IBAtT_lBlhxmf-ist6z0T7sjRJA'

LED_PIN = 12 
led = machine.Pin(LED_PIN, machine.Pin.OUT)
led.value(1)

print("Connecting to WiFi network '{}'".format(WIFI_SSID))
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(WIFI_SSID, WIFI_PASS)

while not wifi.isconnected():
    time.sleep(1)
    print('WiFi connect retry ...')

print('WiFi IP:', wifi.ifconfig()[0])
print("Connecting to Blynk...")
blynk = BlynkLib.Blynk(BLYNK_AUTH)

@blynk.on("connected")
def blynk_connected(ping):
    print('Blynk ready. Ping:', ping, 'ms')

@blynk.on("V0") 
def switch_LED(value):
    if value[0] == '1':
        led.value(0)  
        print("LED is ON")
    else:
        led.value(1) 
        print("LED is OFF")

def runLoop():
    while True:
        blynk.run()
        machine.idle()

runLoop()
