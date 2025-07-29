#   @file      ModemPowerOff.py
#   @license   MIT
#   @copyright Copyright (c) 2025  Shenzhen Xin Yuan Electronic Technology Co., Ltd
#   @date      2025-07-28
#   @note      Known issues, ESP32 (V1.2) version of T-A7670, T-A7608,
#              when using battery power supply mode, BOARD_POWERON_PIN (IO12) must be set to high level after esp32 starts, otherwise a reset will occur.

import machine
import time
from machine import Pin, UART
import utilities

# Initialize UART for modem communication
uart = UART(1, baudrate=utilities.MODEM_BAUDRATE, tx=utilities.MODEM_TX_PIN, rx=utilities.MODEM_RX_PIN)

def modem_test_at():
    uart.write('AT\r\n')
    time.sleep(0.1)
    if uart.any():
        response = uart.read().decode().strip()
        return "OK" in response
    return False

def modem_poweroff():
    if utilities.CURRENT_PLATFORM == "LILYGO_T_SIM7000G":
        uart.write('AT+CPOWD=1\r\n')
        time.sleep(3)
        if uart.any():
            response = uart.read().decode().strip()
            print(response)
            return "NORMAL POWER DOWN" in response
        return False
    else:
        uart.write('AT+CPOF\r\n')
        time.sleep(3)
        if uart.any():
            response = uart.read().decode().strip()
            print(response)
            return "OK" in response
        return False

def setup():
    print("Start Sketch")
    
    try:
        # Set Power control pin output (important for battery power)
        poweron_pin = Pin(utilities.BOARD_POWERON_PIN, Pin.OUT)
        poweron_pin.value(1)
        print("Set BOARD_POWERON_PIN high to prevent reset")
    except:
        pass
    
    try:
        # Set modem reset pin, reset modem
        reset_pin = Pin(utilities.MODEM_RESET_PIN, Pin.OUT)
        reset_pin.value(not utilities.MODEM_RESET_LEVEL)
        time.sleep(0.1)
        reset_pin.value(utilities.MODEM_RESET_LEVEL)
        time.sleep(2.6)
        reset_pin.value(not utilities.MODEM_RESET_LEVEL)
    except:
        pass
    
    try:
        machine.Pin(utilities.MODEM_DTR_PIN, machine.Pin.OUT).value(0)
    except:
        pass
    
    try:
        # PowerKey Control modem power on
        pwrkey_pin = Pin(utilities.BOARD_PWRKEY_PIN, Pin.OUT)
        pwrkey_pin.value(0)
        time.sleep(0.1)
        pwrkey_pin.value(1)
        time.sleep(0.1)
        pwrkey_pin.value(0)
    except:
        pass
    
    # Test modem connected
    print("Waiting for modem to respond...")
    while not modem_test_at():
        time.sleep(0.001)
    
    print("Modem has power on!")
    
    # Countdown before poweroff
    for i in range(10, 0, -1):
        print("Turn off the modem after %d seconds" % i)
        time.sleep(1)
    
    # AT Command send poweroff cmd
    print("Send power off!")
    if modem_poweroff():
        print("Modem power off command accepted")
    else:
        print("Modem power off command failed")
    
    time.sleep(10)

if __name__ == '__main__':
    setup()
    # Empty loop similar to Arduino version
    while True:
        time.sleep(0.01)