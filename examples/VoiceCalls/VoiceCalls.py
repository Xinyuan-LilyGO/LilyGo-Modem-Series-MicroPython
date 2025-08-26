'''
 * @file      Voice_Call.py
 * @license   MIT
 * @copyright Copyright (c) 2025  Shenzhen Xin Yuan Electronic Technology Co., Ltd
 * @date      2025-07-21
 * @note      Not support T-SIM7670G,SIM7000G
 * * Voice calls require external welding of the condenser microphone and speaker.
 * * Generally, the board silk screen is marked SPK. The speaker needs to be welded,
 * * and the MIC silk screen position needs to weld the condenser microphone.
 * *  Although the manual of SIM7672G/SIM7670G states that it has the functions of making voice calls and sending text messages,
 * * the current firmware does not support it.
 * * `A7670E-LNXY-UBL` this version does not support voice and SMS functions.
'''
import time
import machine
import utilities

# Initialize the serial interface for the modem
uart = machine.UART(1, baudrate=utilities.MODEM_BAUDRATE, tx=utilities.MODEM_TX_PIN, rx=utilities.MODEM_RX_PIN)
APN = ""  # Replace with your APN (CHN-CT: China Telecom)
number = "+86xxxxxxxxx"  #Change the number you want to dial

def send_at_command(command, wait=1):
    uart.write(command + "\r\n")
    time.sleep(wait)
    response = uart.read()
    if response:
        if isinstance(response, bytes) and len(response) > 0:
            try:
                return response.decode("utf-8", "ignore").strip()
            except: 
                return ""
    return ""

def modem_power_on():
    machine.Pin(utilities.BOARD_PWRKEY_PIN, machine.Pin.OUT).value(0)
    time.sleep(0.1)
    machine.Pin(utilities.BOARD_PWRKEY_PIN, machine.Pin.OUT).value(1)
    time.sleep(1)
    machine.Pin(utilities.BOARD_PWRKEY_PIN, machine.Pin.OUT).value(0)

def modem_reset():
    machine.Pin(utilities.MODEM_RESET_PIN, machine.Pin.OUT).value(not utilities.MODEM_RESET_LEVEL)
    time.sleep(0.1)
    machine.Pin(utilities.MODEM_RESET_PIN, machine.Pin.OUT).value(utilities.MODEM_RESET_LEVEL)
    time.sleep(2.6)
    machine.Pin(utilities.MODEM_RESET_PIN, machine.Pin.OUT).value(not utilities.MODEM_RESET_LEVEL)

def check_modem():
    print("Starting modem...")
    while True:
        response = send_at_command("AT")
        if "OK" in response:
            print()  # Print a newline for clarity
            break
        else:
            print(".", end="")

def callNumber(number):
    response = send_at_command(f"ATD{number};")
    print(response)
    
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
    print(f"Init success, start to call {number}");
    callNumber(number)
    while True:
        if machine.Pin(utilities.MODEM_RING_PIN, machine.Pin.IN, machine.Pin.PULL_UP).value() == 0:
            print("Incoming call...")
        time.sleep(0.01)

if __name__ == "__main__":
    main()
