'''
 * @file      LBSExample.py
 * @license   MIT
 * @copyright Copyright (c) 2025  Shenzhen Xin Yuan Electronic Technology Co., Ltd
 * @date      2025-07-14
 * @note      Not support T-SIM7672
'''
import time
import machine
import utilities
import re

# Initialize the serial interface for the modem
uart = machine.UART(1, baudrate=utilities.MODEM_BAUDRATE, tx=utilities.MODEM_TX_PIN, rx=utilities.MODEM_RX_PIN)

def send_at_command(command,wait=1):
    uart.write(command + "\r\n")
    time.sleep(wait)
    response = uart.read()
    if response:
        return response.decode("utf-8", "ignore").strip()
    return ""

def modem_power_on():
    machine.Pin(utilities.BOARD_PWRKEY_PIN, machine.Pin.OUT).value(0)
    time.sleep(0.1)
    machine.Pin(utilities.BOARD_PWRKEY_PIN, machine.Pin.OUT).value(1)
    time.sleep(1)
    machine.Pin(utilities.BOARD_PWRKEY_PIN, machine.Pin.OUT).value(0)

def modem_reset():
    machine.Pin(utilities.MODEM_RESET_PIN, machine.Pin.OUT).value(0)
    time.sleep(0.1)
    machine.Pin(utilities.MODEM_RESET_PIN, machine.Pin.OUT).value(1)
    time.sleep(2.6)
    machine.Pin(utilities.MODEM_RESET_PIN, machine.Pin.OUT).value(0)

def check_modem():
    print("Starting modem...")
    while True:
        response = send_at_command("AT")
        if "OK" in response:
            print()  # Print a newline for clarity
            break
        else:
            print(".", end="")
    
def main():
    # Turn on DC boost to power on the modem
    machine.Pin(utilities.BOARD_POWERON_PIN, machine.Pin.OUT).value(1)
    # Set modem reset pin ,reset modem
    modem_reset()
    # Turn on modem
    modem_power_on()
    # Set ring pin input
    machine.Pin(utilities.MODEM_RING_PIN, machine.Pin.IN, machine.Pin.PULL_UP)
    check_modem()
    time.sleep(10)
    while True:
        print("Requesting current GSM location")
        response = send_at_command("AT+CLBS=4,1")
        print(response)
        if 'OK' in response:
            match = re.search(r'\+CLBS: 0,([^,]+),([^,]+),([^,]+),(\d+)/(\d+)/(\d+),(\d+):(\d+):(\d+)', response)
            if match:
                # Extract each part from the matched groups
                lat = float(match.group(1))
                lon = float(match.group(2))
                accuracy = float(match.group(3))
                year = int(match.group(4))
                month = int(match.group(5))
                day = int(match.group(6))
                hour = int(match.group(7))+8  # +time zone
                minute = int(match.group(8))
                second = int(match.group(9))
                # Print the extracted data
                print(f"Latitude: {lat:.8f}")
                print(f"Longitude: {lon:.8f}")
                print(f"Accuracy: {accuracy:.2f}")
                print(f"Year: {year}\tMonth: {month}\tDay: {day}")
                print(f"Hour: {hour}\tMinute: {minute}\tSecond: {second}")
                break
            else:
                print("Couldn't get GSM location, retrying in 15s.")
    print("Retrieving GSM location again as a string")
    response = send_at_command("AT+CLBS=1,1",wait=3)
    print(response)
    if 'OK' in response:
        # Extract data using regular expressions
        match = re.search(r'\+CLBS: 0,([^,]+),([^,]+),(\d+)', response)
        if match:
            # Extract each part from the matched groups
            lat = match.group(1)
            lon = match.group(2)
            accuracy = match.group(3)
            # Format and print the location string
            location_string = f"GSM Based Location String:{lat},{lon},{accuracy}"
            print(location_string)
        else:
            print("Failed to parse location data.")
    
if __name__ == "__main__":
    main()