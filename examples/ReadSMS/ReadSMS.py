'''
 * @file      ReadSMS.py
 * @license   MIT
 * @copyright Copyright (c) 2025  Shenzhen Xin Yuan Electronic Technology Co., Ltd
 * @date      2025-07-18
 * @note      SIM7670G does not support SMS and voice functions
 *            `A7670E-LNXY-UBL` this version does not support voice and SMS functions.
 * ! Only read data, not decode data. For detailed SMS operation, please refer to A76XX_Series_AT_Command_Manual
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

def send_at_command(command,wait=1):
    uart.write(command + "\r\n")
    time.sleep(wait)
    response = uart.read()
    if response:
        return response.decode("utf-8", "ignore").strip()
    return ""

def readSMS_send_at(command, timeout=10000):
    uart.write((command + "\r\n").encode('utf-8'))
    time.sleep(1)
    data = ""
    start_time = time.ticks_ms()
    while time.ticks_ms() - start_time < timeout:
        if uart.any():
            data += uart.read().decode('utf-8')
            if "OK" in data or "ERROR" in data:
                break
    return data

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

def check_sim():
    while True:
        sim_status = send_at_command("AT+CPIN?",wait=3)
        if "READY" in sim_status:
            print("SIM card online")
            break
        elif "SIM not inserted" in sim_status:
            print("SIM not inserted.")
        else:
            print("The SIM card is locked. Please unlock the SIM card first.")
            time.sleep(3)

def connect_network(apn):
    send_at_command(f"AT+CGDCONT=1,\"IP\",\"{apn}\"")
    send_at_command("AT+CGATT=1")  # Attach to the GPRS
    while True:
        response = send_at_command("AT+NETOPEN",wait=3)
        if "OK" in response or "+NETOPEN: 0" in response:
            print("Online registration successful")
            break
        else:
            print("Network registration was rejected, please check if the APN is correct")

def readSMS():
    #! Only read data, not decode data. For detailed SMS operation, please refer to A76XX_Series_AT_Command_Manual
    #! Only read data, not decode data. For detailed SMS operation, please refer to A76XX_Series_AT_Command_Manual
    #! Only read data, not decode data. For detailed SMS operation, please refer to A76XX_Series_AT_Command_Manual
    #! Only read data, not decode data. For detailed SMS operation, please refer to A76XX_Series_AT_Command_Manual
    #! Only read data, not decode data. For detailed SMS operation, please refer to A76XX_Series_AT_Command_Manual
    
    # A76XX_Series_AT_Command_Manual_V1.12.pdf : https://github.com/Xinyuan-LilyGO/LilyGO-T-A76XX-MicroPython/blob/main/datasheet/A76XX/A76XX_Series_AT_Command_Manual_V1.12.pdf
    # A76XX Series_SMS_Application Note_V3.00.pdf : https://github.com/Xinyuan-LilyGO/LilyGO-T-A76XX-MicroPython/blob/main/datasheet/A76XX/A76XX%20Series_SMS_Application%20Note_V3.00.pdf

    # Set SMS system into text mode
    response = send_at_command("AT+CMGF=1",wait=3)
    print(response)
    time.sleep(10)
    # Listing all SMS messages
    response = readSMS_send_at("AT+CMGL=\"ALL\"")
    print(response)
    time.sleep(3)
    if 'OK' in response:
        print("ALL MSG Data:")
        response = response.replace("\r\nOK\r\n", "").replace("\rOK\r", "").strip()
#         response = response.replace("\r\nOK\r\n", "").replace("\rOK\r", "").strip()
        print(response)
    else:
        print("Read all messages failed")
    print("==================================")
    time.sleep(3)
    # Reading the message again changes the status to "READ" from "UNREAD"
    response = readSMS_send_at("AT+CMGR=1",timeout=1000)
    print(response)
    if 'OK' in response:
        print("Last Data:")
        response = response.replace("\r\nOK\r\n", "").replace("\rOK\r", "").strip()
#         response = response.replace("\r\nOK\r\n", "").replace("\rOK\r", "").strip()
        print(response)
    else:
        print("Read message failed")
    print("==================================")
    time.sleep(3)
    # Read the second to last SMS message
    response = readSMS_send_at("AT+CMGR=2",timeout=1000)
    print(response)
    if 'OK' in response:
        print("Sec 2 Data:")
        response = response.replace("\r\nOK\r\n", "").replace("\rOK\r", "").strip()
#         response = response.replace("\r\nOK\r\n", "").replace("\rOK\r", "").strip()
        print(response)
    else:
        print("Read message failed")
    print("==================================")
    
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
    print("Wait for the modem to register with the network.")
    response = send_at_command("AT+SIMCOMATI")
    print(response)
    time.sleep(1)
    response = send_at_command("AT+CREG?")
    print(response)
    check_sim()
    connect_network(APN)
    readSMS()
    while True:
        time.sleep(0.01)

if __name__ == "__main__":
    main()