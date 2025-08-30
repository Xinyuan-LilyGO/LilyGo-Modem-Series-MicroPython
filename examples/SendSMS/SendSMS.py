'''
 * @file      SendSMS.py
 * @license   MIT
 * @copyright Copyright (c) 2025  Shenzhen Xin Yuan Electronic Technology Co., Ltd
 * @date      2025-08-26
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
SMS_TARGET = "+380xxxxxxxxxxx"  #Change the SMS_TARGET you want to dial

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

def connect_network(apn):
    if utilities.CURRENT_PLATFORM == "LILYGO_T_A7670X_S3_STAN":
        response = send_at_command("AT+CNMP=2")
        print(response)
        response = send_at_command("AT+CNMP=?")
        print(response)
        print("Current network mode : AUTO")
        print("Wait for the modem to register with the network.")
        response = send_at_command("AT+CEREG?")
        print(response)
        if "OK" in response:
            print("Online registration successful")
    else:
        send_at_command(f"AT+CGDCONT=1,\"IP\",\"{apn}\"")  # Set the PDP context
        send_at_command("AT+CGATT=1")  # Attach to the GPRS network
        while True:
            send_at_command("AT+NETCLOSE", wait=3)
            response = send_at_command("AT+NETOPEN",wait=3)
            if "OK" in response or "+NETOPEN: 0" in response:
                print("Online registration successful")
                break
            else:
                print("Network registration was rejected, please check if the APN is correct")

def modem_power_on():
    try:
        machine.Pin(utilities.BOARD_PWRKEY_PIN, machine.Pin.OUT).value(0)
        time.sleep(0.1)
        machine.Pin(utilities.BOARD_PWRKEY_PIN, machine.Pin.OUT).value(1)
        time.sleep(1)
        machine.Pin(utilities.BOARD_PWRKEY_PIN, machine.Pin.OUT).value(0)
    except:
        passs
        
def modem_reset():
    try:
        machine.Pin(utilities.MODEM_RESET_PIN, machine.Pin.OUT).value(not utilities.MODEM_RESET_LEVEL)
        time.sleep(0.1)
        machine.Pin(utilities.MODEM_RESET_PIN, machine.Pin.OUT).value(utilities.MODEM_RESET_LEVEL)
        time.sleep(2.6)
        machine.Pin(utilities.MODEM_RESET_PIN, machine.Pin.OUT).value(not utilities.MODEM_RESET_LEVEL)
    except:
        pass
        
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
    uart.write(("hello a76xx!" + "\r\n").encode('utf-8'))
    time.sleep(1)  
    uart.write(bytearray([0x1A]))
    time.sleep(1)
    if '>' in response:
        print("Send sms message OK")
    else:
        print("Send sms message fail")
    
def main():
    # Turn on DC boost to power on the modem
    try:
        machine.Pin(utilities.BOARD_POWERON_PIN, machine.Pin.OUT).value(1)
    except:
        pass
    # Set modem reset pin ,reset modem
    modem_reset()
    # Turn on modem
    modem_power_on()
    # Set ring pin input
    machine.Pin(utilities.MODEM_RING_PIN, machine.Pin.IN, machine.Pin.PULL_UP)
    check_modem()
    time.sleep(1)
    connect_network(APN)
    print(f"Init success, start to send message to {SMS_TARGET}");
    sendSMS(SMS_TARGET)
    while True:
        pass

if __name__ == "__main__":
    main()