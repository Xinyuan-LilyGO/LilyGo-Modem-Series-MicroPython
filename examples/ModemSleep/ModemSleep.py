#   @file      ModemSleep.py
#   @license   MIT
#   @copyright Copyright (c) 2025  Shenzhen Xin Yuan Electronic Technology Co., Ltd
#   @date      2025-07-28
#   @record    https://youtu.be/2cjNsYcU6TU
#   @note      T-A7608 & T-A7608-S3 & T-A7670x VBUS of the modem is connected to VBUS.
#              When using USB power supply, the modem cannot be set to sleep mode. Please see README for details.  
import machine
import time
from machine import Pin, UART
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
        response = uart.read().decode().strip()
        return "OK" in response
    return False

def modem_sleep_enable(enable):
    cmd = 'AT+CSCLK={}\r\n'.format(1 if enable else 0)
    uart.write(cmd)
    time.sleep(0.1)
    if uart.any():
        response = uart.read().decode().strip()
        return "OK" in response
    return False

def setup():
    print("Initializing...")
    
    try:
        # Turn on DC boost to power on the modem
        poweron_pin = Pin(utilities.BOARD_POWERON_PIN, Pin.OUT)
        poweron_pin.value(1)
    except:
        pass
    
    
    wake_reason = machine.reset_cause()
    if wake_reason != machine.DEEPSLEEP_RESET:
        try:
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
            print("Power on modem PWRKEY")
            pwrkey_pin = Pin(utilities.BOARD_PWRKEY_PIN, Pin.OUT)
            pwrkey_pin.value(0)
            time.sleep(0.1)
            pwrkey_pin.value(1)
            time.sleep(0.1)
            pwrkey_pin.value(0)
        except:
            pass
    else:
        print("Wakeup modem!")
        try:
            dtr_pin = Pin(utilities.MODEM_DTR_PIN, Pin.OUT)
            dtr_pin.value(0)
            time.sleep(2)
            modem_sleep_enable(False)
            time.sleep(10)
        except:
            pass
    
    print("Check modem online.")
    while not modem_test_at():
        print(".", end='')
        time.sleep(0.5)
    print("\nModem is online!")
    time.sleep(5)
    print("Enter modem sleep mode!")
    
    try:
        dtr_pin = Pin(utilities.MODEM_DTR_PIN, Pin.OUT)
        dtr_pin.value(1)
        time.sleep(1)
    except:
        pass
    
    if not modem_sleep_enable(True):
        print("modem sleep failed!")
    else:
        print("Modem enter sleep mode!")

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
            print("\nModem is not response ,modem has sleep !")
            break

        time.sleep(1) 
    else:
        print("\nTimeout waiting for modem response.")
    
    # Prepare for deep sleep
    print("Enter esp32 goto deepsleep!")
    time.sleep(0.2)
    machine.deepsleep(TIME_TO_SLEEP * uS_TO_S_FACTOR)
    print("This will never be printed")

if __name__ == '__main__':
    setup()