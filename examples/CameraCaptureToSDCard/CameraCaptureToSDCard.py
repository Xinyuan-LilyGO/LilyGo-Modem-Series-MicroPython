'''
 * @file      CameraCaptureToSDCard.py
 * @license   MIT
 * @copyright Copyright (c) 2025  ShenZhen XinYuan Electronic Technology Co., Ltd
 * @date      2025-08-21
 * @note      Sketch is only suitable for LilyGo-A7670X-S3 version,Other versions are not supported
 *      This sketch is only applicable to the
 *      1. T-A7670X-S3-Standard
 *      2. T-SIM7000G-S3-Standard
 *      3. T-SIM7080G-S3-Standard
 *      4. T-SIM7670G-S3-Standard
 *      Other models are not supported
'''
import camera
import gc
import time
import os
import machine
import uos
import utilities
from machine import SoftI2C, ADC, Pin

i2c = SoftI2C(sda=machine.Pin(utilities.BOARD_SDA_PIN), scl=machine.Pin(utilities.BOARD_SCL_PIN))
I2C_ADDRESS = 0x28

# Initialize ADC
battery_adc = ADC(Pin(utilities.BOARD_BAT_ADC_PIN))  # Replace with the actual ADC pin
battery_adc.atten(ADC.ATTN_11DB)  # Set attenuation
battery_adc.width(ADC.WIDTH_12BIT)  # Set resolution to 12 bits

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

def get_battery_voltage():
    voltage = battery_voltage = battery_adc.read() * 2  # Read battery voltage and multiply by 2
    if voltage < 3000:
        print("Enter esp32 goto deepsleep!")
        machine.deepsleep(180 * 10000)
        print("This will never be printed")
    else:
        print("Voltage:{}".format(voltage))
        print("Battery voltage is normal")
        return voltage

def set_device_to_sleep():
    print("Enter esp32 goto deepsleep!")
    machine.deepsleep(180 * 1000)

def setup_sd():
    try:
        sd = machine.SDCard(slot=2, width=1,
                            sck=machine.Pin(utilities.BOARD_SCK_PIN),
                            miso=machine.Pin(utilities.BOARD_MISO_PIN),
                            mosi=machine.Pin(utilities.BOARD_MOSI_PIN),
                            cs=machine.Pin(utilities.BOARD_SD_CS_PIN),
                            freq=20000000)
        vfs = uos.VfsFat(sd)
        uos.mount(vfs, '/')
        card_info = uos.statvfs('/')
        total_size = int((card_info[0] * card_info[2]) / (1024 * 1024))
        print("SD Card Type: SDHC" if total_size > 4096 else "SD Card Type: SDSC")
        print("SD Card Size: {}MB".format(total_size))
        return vfs
    except Exception as e:
        print("Failed to initialize SD card:", e)
        return None

def setup_camera():
    try:
        camera.init(0, format=camera.JPEG, fb_location=camera.PSRAM, framesize=camera.FRAME_QVGA)
    except Exception as e:
        print("Camera initialization failed:", e)
        camera.deinit()

def capture_image(vfs, boot_count):
    buf = camera.capture()
    if buf:
        if not "camera" in uos.listdir("/"):
            uos.mkdir("/camera")
            print("Created camera directory!")
        filename = "/camera/{}.jpg".format(boot_count)
        start_time = time.ticks_ms()
        with open(filename, "wb") as f:
            f.write(buf)
        elapsed_time = time.ticks_ms() - start_time
        print("JPG created successfully,filename:{} write image data,framesize:1280 * 720JPG was written successfully, taking {} ms".format(filename, elapsed_time))
    else:
        print("Capturing camera failed!")

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

boot_count = 1
print("Boot number:", boot_count)

get_battery_voltage()
get_battery_voltage()

vfs = setup_sd()
if vfs:
    setup_camera()
    capture_image(vfs, boot_count)

print("Disbale camera")
print("ripheral is connected to the channel")
camera.deinit()
print("Power off camera")
set_device_to_sleep()
