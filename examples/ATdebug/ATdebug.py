'''
#   @file      ATdebug.py
#   @license   MIT
#   @copyright Copyright (c) 2025  Shenzhen Xin Yuan Electronic Technology Co., Ltd
#   @date      2025-06-11
'''
from machine import UART, Pin
import time
import sys
import select
import utilities

# Initialize UART
uart = UART(1, baudrate=115200, tx=utilities.MODEM_TX_PIN, rx=utilities.MODEM_RX_PIN, timeout=100)

def modem_init():
    # Power control
    poweron = Pin(utilities.BOARD_POWERON_PIN, Pin.OUT)
    poweron.value(1)
    
    # Reset the modem
    print("Set Reset Pin.")
    reset = Pin(utilities.MODEM_RESET_PIN, Pin.OUT)
    reset.value(not utilities.MODEM_RESET_LEVEL)
    time.sleep(0.1)
    reset.value(utilities.MODEM_RESET_LEVEL)
    time.sleep(2.6)
    reset.value(not utilities.MODEM_RESET_LEVEL)
    
    # Power key control
    print("Power on the modem PWRKEY.")
    pwrkey = Pin(utilities.BOARD_PWRKEY_PIN, Pin.OUT)
    pwrkey.value(0)
    time.sleep(0.1)
    pwrkey.value(1)
    time.sleep(0.1)
    pwrkey.value(0)
    
    # Wait for the modem to start up
    time.sleep(3)

def auto_baud():
    baudrates = [115200, 9600, 57600, 38400, 19200, 74400, 74880,
                230400, 460800, 2400, 4800, 14400, 28800]
    
    for rate in baudrates:
        print("Trying baud rate %u" % rate)
        uart.init(baudrate=rate, tx=utilities.MODEM_TX_PIN, rx=utilities.MODEM_RX_PIN)
        time.sleep(0.1)
        for _ in range(10):
            uart.write("AT\r\n")
            time.sleep(0.1)
            if uart.any():
                response = uart.read().decode()
                if "OK" in response:
                    print("Modem responded at rate:%u" % rate)
                    return rate
    return 0

def main():
    print("Start Sketch")
    modem_init()
    
    rate = auto_baud()
    if rate:
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
                response = uart.read().decode()
                print(response.strip())
            
            time.sleep(0.01)
    else:
        print("***********************************************************")
        print(" Failed to connect to the modem! Check the baud and try again.")
        print("***********************************************************\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting...")