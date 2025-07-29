'''
#   @file      ATdebug.py
#   @license   MIT
#   @copyright Copyright (c) 2025  Shenzhen Xin Yuan Electronic Technology Co., Ltd
#   @date      2025-07-28
AT+SIMCOMATI
'''
from machine import UART, Pin
import time
import sys
import select
import utilities
import machine

# Initialize UART
uart = UART(1, baudrate=115200, tx=utilities.MODEM_TX_PIN, rx=utilities.MODEM_RX_PIN, timeout=100)

def modem_init():
    # Power control
    try:
        poweron = Pin(utilities.BOARD_POWERON_PIN, Pin.OUT)
        poweron.value(1)
    except:
        pass
    
    # Reset the modem
    try:
        print("Set Reset Pin.")
        reset = Pin(utilities.MODEM_RESET_PIN, Pin.OUT)
        reset.value(not utilities.MODEM_RESET_LEVEL)
        time.sleep(0.1)
        reset.value(utilities.MODEM_RESET_LEVEL)
        time.sleep(2.6)
        reset.value(not utilities.MODEM_RESET_LEVEL)
    except:
        pass
    
    try:
        machine.Pin(utilities.MODEM_DTR_PIN, machine.Pin.OUT).value(0)
    except:
        pass
    
    # Power key control
    try:
        print("Power on the modem PWRKEY.")
        pwrkey = Pin(utilities.BOARD_PWRKEY_PIN, Pin.OUT)
        pwrkey.value(0)
        time.sleep(0.1)
        pwrkey.value(1)
        time.sleep(0.1)
        pwrkey.value(0)
    except:
        pass
    
    # Wait for the modem to start up
    time.sleep(3)

def main():
    print("Start Sketch")
    modem_init()
    
    # Set a fixed baud rate
    uart.init(baudrate=115200, tx=utilities.MODEM_TX_PIN, rx=utilities.MODEM_RX_PIN)
    time.sleep(1)  # Give some time for the modem to initialize
        
    print("***********************************************************")
    print(" You can now send AT commands")
    print(" Enter \"AT\" (without quotes), and you should see \"OK\"")
    print(" DISCLAIMER: Entering AT commands without knowing what they do")
    print(" can have undesired consequences...")
    print("***********************************************************\n")
    
    while True:
        # Check for user input
        if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
            cmd = sys.stdin.readline().strip()
            if cmd:
                uart.write(cmd + "\r\n")
        
        # Check for modem response
        if uart.any():
            response = uart.read()
            try:
                response = response.decode()
                print(response.strip())
            except UnicodeError:
                print("Received invalid data from modem")
        
        time.sleep(0.01)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting...")