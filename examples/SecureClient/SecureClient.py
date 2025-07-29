'''
 * @file      SecureClient.py
 * @license   MIT
 * @copyright Copyright (c) 2025  ShenZhen XinYuan Electronic Technology Co., Ltd
 * @date      2025-07-29
 * @note      Secure Client support A7670X/A7608X/SIM7670G
 *
 *
 * Tested on the following firmware versions
 * Model: SIM7670G-MNGV
 * Revision: 2374B05SIM767XM5A_M
 *
 * Model: A7608SA-H
 * Revision: A50C4B12A7600M7 , A7600M7_B12V01_240315
 *
 * Model: A7670SA-FASE
 * Revision: A011B07A7670M7_F,A7670M7_B07V01_240927
'''
import time
import machine
import utilities
import urequests
import re

# It depends on the operator whether to set up an APN. If some operators do not set up an APN,
# they will be rejected when registering for the network. You need to ask the local operator for the specific APN.
# APNs from other operators are welcome to submit PRs for filling.
APN = ""  # Replace with your APN (CHN-CT: China Telecom)

# Request URLs
request_urls = [
    "https://httpbin.org/get",
    "https://vsh.pp.ua/TinyGSM/logo.txt",
    "http://ipapi.co/timezone",
    "http://ip-api.com/json/23.158.104.183",
]

request_server_ports = [
    443,  # https://httpbin.org/get
    443,  # https://vsh.pp.ua/TinyGSM/logo.txt
    443,  # https://ipapi.co/timezone
    80    # http://ip-api.com/json/23.158.104.183
]

# Initialize the UART interface for the modem
uart = machine.UART(1, baudrate=utilities.MODEM_BAUDRATE, tx=utilities.MODEM_TX_PIN, rx=utilities.MODEM_RX_PIN)
time.sleep(1)

# Modem power on and reset sequence
def modem_power_on():
    try:
        machine.Pin(utilities.MODEM_DTR_PIN, machine.Pin.OUT).value(0)
    except:
        pass
    
    try:
        machine.Pin(utilities.BOARD_PWRKEY_PIN, machine.Pin.OUT).value(0)
        time.sleep(0.1)
        machine.Pin(utilities.BOARD_PWRKEY_PIN, machine.Pin.OUT).value(1)
        time.sleep(0.1)
        machine.Pin(utilities.BOARD_PWRKEY_PIN, machine.Pin.OUT).value(0)
    except:
        pass
    
def modem_reset():
    try:
        machine.Pin(utilities.MODEM_RESET_PIN, machine.Pin.OUT).value(not utilities.MODEM_RESET_LEVEL)
        time.sleep(0.1)
        machine.Pin(utilities.MODEM_RESET_PIN, machine.Pin.OUT).value(utilities.MODEM_RESET_LEVEL)
        time.sleep(2.6)
        machine.Pin(utilities.MODEM_RESET_PIN, machine.Pin.OUT).value(not utilities.MODEM_RESET_LEVEL)
    except:
        pass
    
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

def check_modem():
    print("Start modem...")
    while True:
        response = send_at_command("AT")
        if "OK" in response:
            print()  # Print a newline for clarity
            break
        else:
            print(".", end="")

def check_sim():
    while True:
        sim_status = send_at_command("AT+CPIN?",wait=2)
        if "READY" in sim_status:
            print("SIM card online")
            break
        else:
            print("The SIM card is locked. Please unlock the SIM card first.")
            time.sleep(3)

def connect_network(apn):
    if utilities.CURRENT_PLATFORM == "LILYGO_T_SIM7000G":
        response = send_at_command("AT+CNMP=2")
        print(response)
        response = send_at_command("AT+CNMP=?")
        print(response)
        print("Wait for the modem to register with the network.")
        response = send_at_command("AT+CEREG?")
        print(response)
        if "OK" in response:
            print("Online registration successful")
        response = send_at_command("AT+CPSI?")
        print(response)
        response = send_at_command("AT+CNACT?")
        print(response)
        response = send_at_command("AT+CNACT=1",wait=3)
        print(response)
        response = send_at_command("AT+CNACT?")
        print(response)
        match = re.search(r'"(\d+\.\d+\.\d+\.\d+)"', response)
        if match:
            ip_address = match.group(1)
            print("Network IP:", ip_address)
    else:
        send_at_command(f"AT+CGDCONT=1,\"IP\",\"{apn}\"")
        send_at_command("AT+CGATT=1")  # Attach to the GPRS
        while True:
            response = send_at_command("AT+NETOPEN",wait=3)
            if "OK" in response or "+NETOPEN: 0" in response:
                print("Online registration successful")
                break
            else:
                print("Network registration was rejected, please check if the APN is correct")

        # Get the IP address
        ip_response = send_at_command("AT+IPADDR")
        if ip_response:
            print("Network IP:", ip_response)
        else:
            print("Failed to retrieve IP address.")

def perform_https_requests():
    # Initialize HTTPS connection
    print("Starting HTTPS session...")
    send_at_command("AT+HTTPTERM")
    # Initialize HTTP service
    response = send_at_command("AT+HTTPINIT")
    if "OK" not in response:
        print("Failed to initialize HTTP service")
        return
    # Ensure SNI is enabled
#     send_at_command('AT+CSSLCFG="enableSNI",0,1')  # Enable SNI (ensure SSL works properly)
    for url in request_urls:
        retry = 3
        while retry > 0:
            print("Request URL :", url)
            
            # Set GET URL
            url_set = send_at_command(f'AT+HTTPPARA="URL","{url}"')
            print(url_set)
            if "OK" not in url_set:
                print("Failed to request :", url)
                retry -= 1
                time.sleep(3)
                continue  # Retry setting the URL

            # Send GET request (AT+HTTPACTION=0 means GET request)
            http_code = send_at_command("AT+HTTPACTION=0")
#             if "ERROR" in http_code or "HTTPACTION" not in http_code:
#                 print("HTTP get failed ! error code =", http_code)
#                 retry -= 1
#                 time.sleep(3)
#                 continue  # Retry sending the GET request

            # Wait for the response to be fully received
            time.sleep(3)

            # Get HTTP header
            header = send_at_command("AT+HTTPHEAD")
            if "OK" not in header:
                print("Failed to get HTTP header:", header)
            else:
                print("HTTP Header :", header)

            # Get HTTP response body with a specified buffer length
            body = send_at_command("AT+HTTPREAD=0,1024")  # Reading the body with a buffer size of 1024 bytes
            if "OK" not in body:
                print("Failed to get HTTP body:", body)
            else:
                print("HTTP body :", body)

            # End of request
            time.sleep(3)
            break  # Exit while loop if request is successful
        
        print("Server disconnected")
    print("All test done ..")
    
def main():
    print("Start Sketch")
    modem_power_on()
    modem_reset()
    check_modem()
    check_sim()
    connect_network(APN)
    perform_https_requests()

if __name__ == "__main__":
    main()