'''
#   @file      HttpsBuiltlnPost.py
#   @license   MIT
#   @copyright Copyright (c) 2025  Shenzhen Xin Yuan Electronic Technology Co., Ltd
#   @date      2025-08-13
#   @note
#   Example is suitable for A7670X/A7608X/SIM7672 series
#   Connect https://httpbin.org test post request
'''
import time
import machine
import utilities
import re

# It depends on the operator whether to set up an APN. If some operators do not set up an APN,
# they will be rejected when registering for the network. You need to ask the local operator for the specific APN.
# APNs from other operators are welcome to submit PRs for filling.
APN = ""  # Replace with your APN (CHN-CT: China Telecom)

# Server URL
server_url = "https://httpbin.org/post"
lens = 0

# Initialize the serial interface for the modem
uart = machine.UART(1, baudrate=utilities.MODEM_BAUDRATE, tx=utilities.MODEM_TX_PIN, rx=utilities.MODEM_RX_PIN)
time.sleep(1)

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

# Check if the modem is online
def check_modem():
    print("Start modem...")
    while True:
        response = send_at_command("AT")
        if "OK" in response:
            print()  # Print a newline for clarity
            break
        else:
            print(".", end="")
            
# Check SIM status
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
    if utilities.CURRENT_PLATFORM == "LILYGO_T_SIM7000G" \
       or utilities.CURRENT_PLATFORM == "LILYGO_T_SIM7000G_S3_STAN" \
        or utilities.CURRENT_PLATFORM == "LILYGO_T_SIM7080G_S3_STAN":
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
        response = send_at_command("AT+CNACT?",wait=5)
        print(response)
        response = send_at_command("AT+CNACT=0,1",wait=5)
        print(response)
        response = send_at_command("AT+CNACT?",wait=5)
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

# Function to perform HTTPS POST request
def perform_https_post():
    global lens
    if utilities.CURRENT_PLATFORM == "LILYGO_T_SIM7000G" \
       or utilities.CURRENT_PLATFORM == "LILYGO_T_SIM7000G_S3_STAN" \
        or utilities.CURRENT_PLATFORM == "LILYGO_T_SIM7080G_S3_STAN":
        response = send_at_command("AT+SHDISC")   
        print(response)
        response = send_at_command('AT+CSSLCFG=\"sni\",0,1')   
        print(response)
        response = send_at_command("AT+SHCHEAD")   
        print(response)
        response = send_at_command('AT+SHCONF=\"BODYLEN\",1024')   
        print(response)
        response = send_at_command('AT+SHCONF=\"HEADERLEN\",350')   
        print(response)
        response = send_at_command('AT+SHCONF=\"IPVER\",0')   
        print(response)
        response = send_at_command('AT+SHCONF=\"TIMEOUT\",60')   
        print(response)
        response = send_at_command("AT+CSSLCFG=\"sslversion\",1,3")   
        print(response)
        response = send_at_command('AT+SHSSL=1,\"\"')   
        print(response)
        response = send_at_command('AT+SHCONF=\"URL\",\"https://httpbin.org\"',wait=5)   
        print(response)
        response = send_at_command("AT+SHCONN",wait=3)
        print(response)
        while True:
            response = send_at_command("AT+SHCONN",wait=3)
            if 'OK' in response or 'ERROR' in response:
                print(response)
                break
        response = send_at_command('AT+SHAHEAD=\"Accept-Language\",\"zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6\"',wait=8)   
        print(response)
        response = send_at_command('AT+SHAHEAD=\"Accept-Encoding\",\"gzip, deflate, br\"',wait=8)   
        print(response)
        response = send_at_command('AT+SHAHEAD=\"ACCEPT\",\"application/json\"',wait=8)   
        print(response)
        response = send_at_command('AT+SHAHEAD=\"User-Agent\",\"TinyGSM/LilyGo-A76XX\"',wait=8)   
        print(response)
        response = send_at_command('AT+SHBOD=21,10000',wait=8)   
        print(response)
        uart.write("This is post example!")
        time.sleep(3)
        uart.write(b"\r\n") 
        response = send_at_command('AT+SHREQ="/post",3',wait=5)   
        print(response)
        response = send_at_command('AT+SHREAD=0,511',wait=10)   
        print(response)
    else:
        # Prepare the data to send
        post_data = '{"message": "This is post example!"}'
        send_at_command("AT+HTTPTERM")
        time.sleep(0.5)
        send_at_command("AT+HTTPINIT") 
        # Ensure SNI is enabled
        send_at_command('+CSSLCFG="enableSNI",0,1')  # Enable SNI (ensure SSL works properly)
        # Set HTTP headers
        send_at_command('AT+HTTPPARA="ACCEPT","application/json"')
        send_at_command('AT+HTTPPARA="USERDATA","Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6"')
        send_at_command('AT+HTTPPARA="USERDATA","Accept-Encoding: gzip, deflate, br"')
        send_at_command('AT+HTTPPARA="USERDATA","User-Agent: TinyGSM/LilyGo-A76XX"')
        # Set the POST URL
        url_set = send_at_command(f'AT+HTTPPARA="URL","{server_url}"')
        if "OK" not in url_set:
            print("Failed to request :", server_url)
            time.sleep(3)
            return

        # Specify the length of the data we are going to send
        data_length = len(post_data)
        http_data_cmd = f'AT+HTTPDATA={data_length},10000'  # 10 seconds timeout
        data_cmd_response = send_at_command(http_data_cmd)
        print(f"HTTP DATA command response: {data_cmd_response}")
        
        # Now send the actual POST data
        uart.write(post_data)  # Write the data directly to the UART
        time.sleep(1)  # Wait for the data to be sent

        # Send the POST request (AT+HTTPACTION=1 means POST request)
        http_code = send_at_command("AT+HTTPACTION=1")
        if "ERROR" in http_code or "HTTPACTION" not in http_code:
            print("HTTP POST failed! Error code =", http_code)
            time.sleep(3)
            return
        
        # Check for successful response code (200)
        if "200" in http_code:
            print("HTTP POST successful")
        else:
            print(f"Unexpected HTTP status: {http_code}")

        # Wait for the response to be fully received
        time.sleep(3)

        # Get HTTP header
        header = send_at_command("AT+HTTPHEAD")
        if "OK" not in header:
            print("Failed to get HTTP header:", header)
        else:
            print("HTTP Header:")
            print(header)

        # Get HTTP response body with a specified buffer length
        body = send_at_command("AT+HTTPREAD=0,1024")  # Reading the body with a buffer size of 1024 bytes
        if "OK" not in body:
            print("Failed to get HTTP body:", body)
        else:
            print("HTTP Body:")
            print(body)

        # End of request
        time.sleep(3)

def main():
    print("Starting sketch...")
    modem_power_on()
    modem_reset()
    check_modem()
    check_sim()
    connect_network(APN)
    # To personally monitor loop of debug info
    perform_https_post()
    time.sleep(10)  # Repeat the POST every 10 seconds

if __name__ == "__main__":
    main()