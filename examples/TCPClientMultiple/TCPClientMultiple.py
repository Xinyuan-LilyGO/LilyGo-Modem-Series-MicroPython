''' 
 * @file      TCPClientMultiple.py
 * @license   MIT
 * @copyright Copyright (c) 2025  ShenZhen XinYuan Electronic Technology Co., Ltd
 * @date      2025-07-08
 * @note      The example demonstrates multiple socket connections. The problem comes from https://github.com/Xinyuan-LilyGO/LilyGO-T-A76XX/issues/223#issuecomment-2639376887
'''
import time
import machine
import utilities
import urequests

# It depends on the operator whether to set up an APN. If some operators do not set up an APN,
# they will be rejected when registering for the network. You need to ask the local operator for the specific APN.
# APNs from other operators are welcome to submit PRs for filling.
APN = ""  # Replace with your APN (CHN-CT: China Telecom)

# Request URLs
urls = [
    "httpbin.org",
    "httpbin.org",
    "httpbin.org",
    "httpbin.org",
    "httpbin.org",
]

resource = [
    "/get",
    "/delete",
    "/patch",
    "/post",
    "/put",
]

method = [
    "GET ",
    "DELETE ",
    "PATCH ",
    "POST ",
    "PUT ",
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
    machine.Pin(utilities.MODEM_RESET_PIN, machine.Pin.OUT).value(not utilities.MODEM_RESET_LEVEL)
    time.sleep(0.1)
    machine.Pin(utilities.MODEM_RESET_PIN, machine.Pin.OUT).value(utilities.MODEM_RESET_LEVEL)
    time.sleep(2.6)
    machine.Pin(utilities.MODEM_RESET_PIN, machine.Pin.OUT).value(not utilities.MODEM_RESET_LEVEL)

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
    response = send_at_command("AT+CPSI?")
    print(f"Inquiring UE system information:{response}")
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

def perform_tcp_client():
    for i in range(len(urls)):
        print("Try connect to", urls[i])
        send_at_command(f"AT+CIPCLOSE={i}")
        send_at_command("AT+CIPRXGET=1")
        response = send_at_command(f'AT+CIPOPEN={i},"TCP","{urls[i]}",80')
        if 'OK' in response:
            print(f"client {i} connect success")
        else:
            print(f"client {i} connect failed")  
    for i in range(len(urls)):
        response = send_at_command(f"AT+CIPRXGET=4,{i}")
#         print(response)
        if 'OK' not in response:
            continue
        response = send_at_command("AT+CIPCLOSE?")
#         print(response)
        print("")
        print(f"Try get request {resource[i]}!")
        print("============================")
        req = method[i] + resource[i] + " HTTP/1.0\r\n"
        response = send_at_command(f"AT+CIPSEND={i},{len(req)}")        
#         print(response)
        uart.write(req)
        response = send_at_command("")  # Wait for the response
#         print(response)
        if 'OK' not in response:
            continue
        response = send_at_command(f"AT+CIPSEND={i},19")
#         print(response)
        uart.write("Host: " + urls[i] + "\r\n")
        response = send_at_command("")  # Wait for the response
#         print(response)
        if 'OK' not in response:
            continue     
        response = send_at_command(f"AT+CIPSEND={i},21")
#         print(response)
        uart.write("Connection: close\r\n\r\n")
        response = send_at_command("")  # Wait for the response
#         print(response)
        if 'OK' not in response:
            continue        
        response = send_at_command(f"AT+CIPRXGET=4,{i}")
#         print(response)        
        response = send_at_command("AT+CIPCLOSE?")
#         print(response)
        response = send_at_command(f"AT+CIPRXGET=4,{i}")
#         print(response)
        parts = response.split(",")
        last_part = parts[-1].strip()  
        received_data_length = int(last_part.split()[0])
        response = send_at_command(f"AT+CIPRXGET=2,{i},{received_data_length}")
        print(response)
        response = send_at_command(f"AT+CIPRXGET=4,{i}")
#         print(response)
        response = send_at_command("AT+CIPCLOSE?")
#         print(response)
        print("Request done!")
        print("============================")
        
    print("All test done ..")
    for i in range(len(urls)):
        print(f"stop client {i} connect")
        response = send_at_command(f"AT+CIPRXGET=4,{i+1}")
        if 'OK' not in response:
            continue
#         print(response)
        response = send_at_command("AT+CIPCLOSE?")
        
def main():
    print("Start Sketch")
    modem_power_on()
    modem_reset()
    check_modem()
    check_sim()
    print("Wait for the modem to register with the network.")
    connect_network(APN)
    perform_tcp_client()

if __name__ == "__main__":
    main()