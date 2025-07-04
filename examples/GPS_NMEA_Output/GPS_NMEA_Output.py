'''
 * @file      GPS_NMEA_Output.py
 * @license   MIT
 * @copyright Copyright (c) 2025  Shenzhen Xin Yuan Electronic Technology Co., Ltd
 * @date      2025-06-25
 * @note      GPS only supports A7670X/A7608X (excluding A7670G and other versions that do not support positioning).
'''
import machine
import time
from machine import UART, Pin
import utilities

# Initialize UART for modem communication
SerialAT = UART(1, baudrate=utilities.MODEM_BAUDRATE, tx=utilities.MODEM_TX_PIN, rx=utilities.MODEM_RX_PIN)

# Initialize pins
pwrkey = Pin(utilities.BOARD_PWRKEY_PIN, Pin.OUT)
poweron = Pin(utilities.BOARD_POWERON_PIN, Pin.OUT)
reset_pin = Pin(utilities.MODEM_RESET_PIN, Pin.OUT)
gps_enable = Pin(utilities.MODEM_GPS_ENABLE_GPIO, Pin.OUT)

def send_at_command(command,wait=1):
    SerialAT.write(command + "\r")
    time.sleep(wait)
    response = SerialAT.read()
    if response:
        return response.decode("utf-8", "ignore").strip()
    return ""

def modem_setup():
    global modemName
    # Turn on DC boost to power on the modem
    poweron.value(1)
    
    # Set modem reset pin ,reset modem
    reset_pin.value(not utilities.MODEM_RESET_LEVEL)
    time.sleep(0.1)
    reset_pin.value(utilities.MODEM_RESET_LEVEL)
    time.sleep(2.6)
    reset_pin.value(not utilities.MODEM_RESET_LEVEL)
    
    # Turn on modem
    pwrkey.value(0)
    time.sleep(0.1)
    pwrkey.value(1)
    time.sleep(1)
    pwrkey.value(0)
    
    print("Start modem...")
    time.sleep(3)
    
    retry = 0
    while True:
        response = send_at_command("AT")
        if "OK" in response:
            break
        print(".")
        retry += 1
        if retry > 10:
            pwrkey.value(0)
            time.sleep(0.1)
            pwrkey.value(1)
            time.sleep(1)
            pwrkey.value(0)
            retry = 0
    print()
    time.sleep(0.2)
    
    # Get modem info
    modemName = "UNKNOWN"
    while True:
        response = send_at_command("AT+CGMM")
        print(response)
        if "OK" in response:
            modemName = response.split("\r\n")[1]
            if "A7670G" in modemName:
                while True:
                    print("A7670G does not support built-in GPS function, please run examples/GPSShield")
                    time.sleep(1)
            else:
                print("Model Name:", modemName)
                break
        else:
            print("Unable to obtain module information normally, try again")
            time.sleep(1)
        time.sleep(5)
    
    print("Enabling GPS/GNSS/GLONASS")
    response = send_at_command("AT+CGDRT=4,1")
    print(response)
    response = send_at_command("AT+CGSETV=4,1")
    print(response)
    while True:
        gps_enable.value(utilities.MODEM_GPS_ENABLE_LEVEL)
        response = send_at_command("AT+CGNSSPWR=1")
        print(response)
        if response:
            break
        print(".", end="")
        
    print("\nGPS Enabled")

    # Set GPS Baud to 115200
    response = send_at_command("AT+CGNSSIPR=115200")
    print(response)
    
    response = send_at_command("AT+CGNSSMODE=3")
    print(response)
    
    response = send_at_command("AT+CGNSSNMEA=1,1,1,1,1,1,0,0")
    print(response)
    
    response = send_at_command("AT+CGPSNMEARATE=1")
    print(response)
    
    response = send_at_command("AT+CGNSSTST=1")
    print(response)
    
    response = send_at_command("AT+CGNSSPORTSWITCH=0,1")
    print(response)
    
    print("Next you should see NMEA sentences in the serial monitor");


def output_loop():
    response = send_at_command("AT+CGNSSPWR?")
    print(response)
    time.sleep(1)

def main():
    global modemName
    modem_setup()
    output_loop()
    # Just echo serial data
    while True:
        if SerialAT.any():
            print(SerialAT.read().decode(), end="")
        time.sleep(0.001)

if __name__ == "__main__":
    main()
