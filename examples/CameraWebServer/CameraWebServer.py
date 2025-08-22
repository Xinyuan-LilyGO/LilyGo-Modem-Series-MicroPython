'''
 * @file      CameraWebServer.py
 * @license   MIT
 * @copyright Copyright (c) 2025  ShenZhen XinYuan Electronic Technology Co., Ltd
 * @date      2025-08-21
 * @note      You must select partition scheme from the board menu that has at least 3MB APP space.
 *      This sketch is only applicable to the
 *      1. T-A7670X-S3-Standard
 *      2. T-SIM7000G-S3-Standard
 *      3. T-SIM7080G-S3-Standard
 *      4. T-SIM7670G-S3-Standard
 *      Other models are not supported
'''
from machine import Pin, I2C, SoftI2C, reset
from microdot import Microdot
import time
import camera
import network
import utilities

SSID = "your wifi name"
PASSWORD = "your wifi password"

I2C_ADDRESS = 0x28
i2c = I2C(0, scl=Pin(utilities.BOARD_SCL_PIN), sda=Pin(utilities.BOARD_SDA_PIN), freq=100000)

def set_camera_power(enable):
    global started
    if 'started' not in globals():
        started = False
    if not started:
        if not i2c.writeto(I2C_ADDRESS, bytearray([0x04])): 
            print("Camera power chip not found!")
            return False
    started = True
    vdd = bytearray([0x04, 0x7C, 0x7C, 0xCA, 0xB1])
    i2c.writeto(I2C_ADDRESS, vdd)
    control = bytearray([0x0E, 0x0F])
    if not enable:
        control[1] = 0x00
    i2c.writeto(I2C_ADDRESS, control)
    return True

def connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(SSID, PASSWORD)
        while not wlan.isconnected():
            pass
    ip_config = wlan.ifconfig()
    print('network ip:', ip_config[0])

def setup():
    global app
    # Turn on the camera power
    if not set_camera_power(True):
        while True:
            print("The camera PMIC failed to start.")
            time.sleep(1)
    # Disable power conservation and use maximum power      
    BOARD_POWER_SAVE_MODE_PIN = Pin(utilities.BOARD_POWER_SAVE_MODE_PIN, Pin.OUT)
    BOARD_POWER_SAVE_MODE_PIN.value(1)
    # Pull down DTR to ensure the modem is not in sleep state
    MODEM_DTR_PIN = Pin(utilities.MODEM_DTR_PIN, Pin.OUT)
    MODEM_DTR_PIN.value(0)
    print("Power on the modem PWRKEY.")
    # Turn on the modem
    MODEM_DTR_PIN = Pin(utilities.BOARD_PWRKEY_PIN, Pin.OUT)
    MODEM_DTR_PIN.value(0)
    time.sleep(0.1)
    MODEM_DTR_PIN.value(1)
    time.sleep(0.1)
    MODEM_DTR_PIN.value(0)
    connect()
    app = Microdot()
    # wait for camera ready
    for i in range(5):
        camera.deinit()
        cam = camera.init(0, format=camera.JPEG, fb_location=camera.PSRAM)

        if cam:
            print("Camera ready")
            break
        else:
            time.sleep(2)
    else:
        print('Timeout')
        reset()

setup()

@app.route('/')
def index(request):
    return '''<!doctype html>
<html>
  <head>
    <title>CameraWebServer</title>
    <style>
      body {
        display: flex;
        flex-direction: column;
        align-items: center; 
        justify-content: center; 
        height: 100vh; 
        margin: 0; 
      }
      img {
        width: 60%; 
      }
    </style>
  </head>
  <body>
    <h1>CameraWebServer</h1>
    <img src="/video_feed">
  </body>
</html>''', 200, {'Content-Type': 'text/html'}

@app.route('/video_feed')
def video_feed(request):
    def stream():
        yield b'--frame\r\n'
        while True:
            frame = camera.capture()
            yield b'Content-Type: image/jpeg\r\n\r\n' + frame + \
                b'\r\n--frame\r\n'
            time.sleep_ms(50)

    return stream(), 200, {'Content-Type':
                           'multipart/x-mixed-replace; boundary=frame'}

if __name__ == '__main__':
    app.run(debug=True, port=80)