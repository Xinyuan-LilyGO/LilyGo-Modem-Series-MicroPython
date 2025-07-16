'''
 * @file      SendSMS.py
 * @license   MIT
 * @copyright Copyright (c) 2025  Shenzhen Xin Yuan Electronic Technology Co., Ltd
 * @date      2025-07-11
 * @note      SIM7670G - SIM7670G-MNGV 2374B04 version supports SMS function,
 *            but it requires the operator base station to support SMS Over SGS service to send, otherwise it will be invalid
 *            `A7670E-LNXY-UBL` this version does not support voice and SMS functions.
'''
import time
import machine
import utilities

# Initialize the serial interface for the modem
uart = machine.UART(1, baudrate=utilities.MODEM_BAUDRATE, tx=utilities.MODEM_TX_PIN, rx=utilities.MODEM_RX_PIN)
# It depends on the operator whether to set up an APN. If some operators do not set up an APN,
# they will be rejected when registering for the network. You need to ask the local operator for the specific APN.
# APNs from other operators are welcome to submit PRs for filling.
APN = ""  # Replace with your APN (CHN-CT: China Telecom)
SMS_TARGET = "+380xxxxxxxxx"  #Change the SMS_TARGET you want to dial

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

def sendSMS(SMS_TARGET):
    response = send_at_command("AT+GSN")
    print(response)
    response = send_at_command("AT+CMGF=1")
    print(response)
    response = send_at_command("AT+CSCS=\"GSM\"")
    print(response)
    response = send_at_command(f"AT+CMGS=\"{SMS_TARGET}\"")
    print(response)
    uart.write(("hello a7670e!" + "\r\n").encode('utf-8'))
    time.sleep(1)  
    uart.write(bytearray([0x1A]))
    time.sleep(1)
    if '>' in response:
        print("Send sms message OK")
    else:
        print("Send sms message fail")
    
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
    time.sleep(1)
    print(f"Init success, start to send message to {SMS_TARGET}");
    sendSMS(SMS_TARGET)
    while True:
        pass

if __name__ == "__main__":
    main()