'''
 * @file      TextToSpeech.py
 * @license   MIT
 * @copyright Copyright (c) 2025  ShenZhen XinYuan Electronic Technology Co., Ltd
 * @date      2025-07-18
 * @note      Only support A7670X A7608X , Not support SIM7670G
'''
from machine import UART
import machine
import time
import urandom
import utilities

# Initialize Serial
uart = UART(1, baudrate=utilities.MODEM_BAUDRATE, tx=utilities.MODEM_TX_PIN, rx=utilities.MODEM_RX_PIN)

def modem_reset():
    machine.Pin(utilities.MODEM_RESET_PIN, machine.Pin.OUT).value(not utilities.MODEM_RESET_LEVEL)
    time.sleep(0.1)
    machine.Pin(utilities.MODEM_RESET_PIN, machine.Pin.OUT).value(utilities.MODEM_RESET_LEVEL)
    time.sleep(2.6)
    machine.Pin(utilities.MODEM_RESET_PIN, machine.Pin.OUT).value(not utilities.MODEM_RESET_LEVEL)

def modem_power_on():
    machine.Pin(utilities.BOARD_PWRKEY_PIN, machine.Pin.OUT).value(0)
    time.sleep(0.1)
    machine.Pin(utilities.BOARD_PWRKEY_PIN, machine.Pin.OUT).value(1)
    time.sleep(0.1)
    machine.Pin(utilities.BOARD_PWRKEY_PIN, machine.Pin.OUT).value(0)
    
def send_at_command(command,wait=1):
    uart.write(command + "\r\n")
    time.sleep(wait)
    response = uart.read()
    if response:
        return response.decode("utf-8", "ignore").strip()
    return ""

# Check if the modem is online
def check_modem():
    print("Start modem...")
    retry = 0
    while True:
        response = send_at_command("AT")
        print(response)
        if "OK" in response:
            print()  # Print a newline for clarity
            break
        else:
            print(".", end="")
        if retry > 10:
            modem_power_on()
            retry = 0
        retry += 1

def setup():
    print("Start Sketch")
    # Set modem reset pin ,reset modem
    machine.Pin(utilities.BOARD_POWERON_PIN, machine.Pin.OUT).value(1)
    modem_reset()
    modem_power_on()
    # Check if the modem is online
    check_modem()
    time.sleep(5)
    # Mode 1: Start to synthesize and play
    text = "6B228FCE4F7F75288BED97F3540862107CFB7EDF"
    response = send_at_command(f"AT+CTTS=1,{text}")
    print(response)
    if 'OK' in response:
        print("Play successfully.")

def main():
    setup()
    count = 0
    while True:
        text = "millis" + str(count)
        # Mode 2: Start to synthesize and play
        response = send_at_command(f"AT+CTTS=2,{text}")
        print(response)
        if 'OK' in response:
            print("Play successfully.")
        count += 1
        time.sleep(1)
    
if __name__ == "__main__":
    main()