'''
#   @file      HttpsBuiltlnGet.py
#   @license   MIT
#   @copyright Copyright (c) 2025  Shenzhen Xin Yuan Electronic Technology Co., Ltd
#   @date      2025-07-08
#   @note
#   Example is suitable for A7670X/A7608X/SIM7672 series
#   Connect https://httpbin.org test get request
'''
import time
import machine
import utilities

# It depends on the operator whether to set up an APN. If some operators do not set up an APN,
# they will be rejected when registering for the network. You need to ask the local operator for the specific APN.
# APNs from other operators are welcome to submit PRs for filling.
APN = ""  # Replace with your APN (CHN-CT: China Telecom)

# Request URLs
request_urls = [
    "https://httpbin.org/get",
    "https://vsh.pp.ua/TinyGSM/logo.txt",
    "https://ipapi.co/timezone",
    "http://ip-api.com/json/23.158.104.183",
    "https://ikfu.azurewebsites.net/api/GetUtcTime"
]

# Initialize the UART interface for the modem
uart = machine.UART(1, baudrate=utilities.MODEM_BAUDRATE, tx=utilities.MODEM_TX_PIN, rx=utilities.MODEM_RX_PIN)
time.sleep(1)

# Modem power on and reset sequence
def modem_power_on():
    machine.Pin(utilities.BOARD_PWRKEY_PIN, machine.Pin.OUT).value(0)
    time.sleep(0.1)
    machine.Pin(utilities.BOARD_PWRKEY_PIN, machine.Pin.OUT).value(1)
    time.sleep(0.1)
    machine.Pin(utilities.BOARD_PWRKEY_PIN, machine.Pin.OUT).value(0)

def modem_reset():
    machine.Pin(utilities.MODEM_RESET_PIN, machine.Pin.OUT).value(0)
    time.sleep(0.1)
    machine.Pin(utilities.MODEM_RESET_PIN, machine.Pin.OUT).value(1)
    time.sleep(2)

def send_at_command(command,wait=1):
    uart.write(command + "\r\n")
    time.sleep(wait)
    response = uart.read()
    if response:
        return response.decode("utf-8", "ignore").strip()
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
    send_at_command(f"AT+CGDCONT=1,\"IP\",\"{apn}\"")
    send_at_command("AT+CGATT=1")  # Attach to the GPRS
    while True:
        response = send_at_command("AT+NETOPEN",wait=3)
        if "OK" in response or "+NETOPEN: 0" in response:
            print("Online registration successful")
            break
        else:
            print("Network registration was rejected, please check if the APN is correct")
#             return

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
    send_at_command('+CSSLCFG="enableSNI",0,1')  # Enable SNI (ensure SSL works properly)

    for url in request_urls:
        retry = 3
        while retry > 0:
            print("Request URL :", url)
            
            # Set GET URL
            url_set = send_at_command(f'AT+HTTPPARA="URL","{url}"')
            if "OK" not in url_set:
                print("Failed to request :", url)
                retry -= 1
                time.sleep(3)
                continue  # Retry setting the URL

            # Send GET request (AT+HTTPACTION=0 means GET request)
            http_code = send_at_command("AT+HTTPACTION=0")
            if "ERROR" in http_code or "HTTPACTION" not in http_code:
                print("HTTP get failed ! error code =", http_code)
                retry -= 1
                time.sleep(3)
                continue  # Retry sending the GET request

            # Check for successful response code (200)
            if "200" in http_code:
                print("HTTP GET successful")
            else:
                print(f"Unexpected HTTP status: {http_code}")

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

        print("-------------------------------------")

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