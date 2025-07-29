'''
#   @file      DeepSleep.py
#   @license   MIT
#   @copyright Copyright (c) 2025  Shenzhen Xin Yuan Electronic Technology Co., Ltd
#   @date      2025-07-28
#   @record    T-A7608-S3 : https://youtu.be/5G4COjtKsFU
#   T-A7608-S3 DeepSleep ~ 368 uA
#   T-A7608-ESP32  DeepSleep ~ 240 uA
#   T-A7670-ESP32  DeepSleep ~ 157 uA
'''

import time
from machine import Pin, UART
import machine
import utilities

# Constants
uS_TO_S_FACTOR = 1000000  # Conversion factor for microseconds to seconds
TIME_TO_SLEEP = 30        # Time ESP32 will go to sleep (in seconds)

# Initialize UART for modem communication
uart = UART(1, baudrate=utilities.MODEM_BAUDRATE, tx=utilities.MODEM_TX_PIN, rx=utilities.MODEM_RX_PIN)

def modem_test_at():
    uart.write('AT\r\n')
    time.sleep(0.1)
    if uart.any():
        response = uart.read()
        return True
    return False

def modem_poweroff():
    uart.write('AT+CPOF\r\n')
    time.sleep(0.1)
    if uart.any():
        response = uart.read().decode().strip()
        return "OK" in response
    return False

def setup():
    print("Initializing...")
    
    # Check wakeup reason
    wake_reason = machine.reset_cause()
    if wake_reason == machine.DEEPSLEEP_RESET:
        print("Wakeup from timer")
        i = 30
        while i > 0:
            print("Modem will start in %d seconds" % i)
            time.sleep(1)
            i -= 1
        print("TurnON Modem!")
    
    try:
        # Turn on DC boost to power on the modem
        poweron_pin = Pin(utilities.BOARD_POWERON_PIN, Pin.OUT)
        poweron_pin.value(1)
        time.sleep(2)
    except:
        pass
    
    try:
        # Handle modem reset
        reset_pin = Pin(utilities.MODEM_RESET_PIN, Pin.OUT)
        print("Set Reset Pin.")
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
        print("Power on the modem PWRKEY.")
        pwrkey_pin = Pin(utilities.BOARD_PWRKEY_PIN, Pin.OUT)
        pwrkey_pin.value(0)
        time.sleep(0.1)
        pwrkey_pin.value(1)
        time.sleep(0.3)
        pwrkey_pin.value(0)
    except:
        pass
    
    try:
        # Pull up DTR to put the modem into sleep
        dtr_pin.value(1)
    except:
        pass
    
    # Delay sometime...
    time.sleep(10)
    
    print("Check modem online.")
    while not modem_test_at():
        print(".", end='')
        time.sleep(0.5)
    print("\nModem is online!")
    
    time.sleep(5)
    
    print("Enter modem power off!")
    if modem_poweroff():
        print("Modem enter power off mode!")
    else:
        print("modem power off failed!")
    
    time.sleep(5)
    
    print("Check modem response.")
    start_time = time.time()
    timeout = 10 
    while (time.time() - start_time) < timeout:
        if uart.any():
            response = uart.read().decode().strip()
            if "OK" in response: 
                print(".", end='')
        else:
            break
        time.sleep(1) 
    print("\nModem is not response, modem has power off!")
    
    time.sleep(5)
    
    try:
        # Turn off DC boost to power off the modem
        poweron_pin.value(0)
    except:
        pass
    
    try:
        # Prepare for deep sleep
        reset_pin.value(not utilities.MODEM_RESET_LEVEL)
        # Note: MicroPython doesn't have direct gpio_hold_en equivalent
        # You might need to handle this differently based on your ESP32 port
    except:
        pass
    
    print("Enter esp32 goto deepsleep!")
    time.sleep(0.2)
    
    # Configure deep sleep
    machine.deepsleep(TIME_TO_SLEEP * uS_TO_S_FACTOR)
    # The following line will never be reached
    print("This will never be printed")

if __name__ == '__main__':
    setup()