'''
#   @file      Network.py
#   @license   MIT
#   @copyright Copyright (c) 2025  Shenzhen Xin Yuan Electronic Technology Co., Ltd
#   @date      2025-07-07
'''
import time
import machine
import utilities

# It depends on the operator whether to set up an APN. If some operators do not set up an APN,
# they will be rejected when registering for the network. You need to ask the local operator for the specific APN.
# APNs from other operators are welcome to submit PRs for filling.
APN = ""  # Replace with your APN (CHN-CT: China Telecom)

# Server URL
server_url = "https://httpbin.org/put"

# Initialize the serial interface for the modem
uart = machine.UART(1, baudrate=utilities.MODEM_BAUDRATE, tx=utilities.MODEM_TX_PIN, rx=utilities.MODEM_RX_PIN)
time.sleep(1)

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
    uart.write(command + "\r")
    time.sleep(wait)
    response = uart.read()
    if response:
        return response.decode("utf-8", "ignore").strip()
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

def main():
    print("Starting sketch...")
    modem_power_on()
    modem_reset()
    check_modem()
    check_sim()
    send_at_command("AT+SIMCOMATI")
    connect_network(APN)
    dest_addr_type = 1
    num_pings = 1
    data_packet_size = 64
    interval_time = 1000
    wait_time = 10000
    url= "www.baidu.com"
    for i in range(20):
        command = f'AT+CPING="{url}",{dest_addr_type},{1},{data_packet_size},{interval_time},{wait_time}'
        response = send_at_command(command,wait=3)
        if "+CPING:" in response:
            # print("Raw Response:", response)
            # Clean the response to remove any extra characters like \r\n, OK, etc.
            cleaned_response = response.split('+CPING:')[1].strip()  # Strip out the '+CPING:' part and clean any extra spaces/newlines
            # Split the cleaned response by commas
            parts = cleaned_response.split(',')
            # Ensure there are enough parts to extract the needed information
            if len(parts) >= 5:
                sequence_number = parts[0]  # Sequence number
                resolved_ip_addr = parts[1]  # Resolved IP address
                bytes_received = int(parts[2])  # Bytes received
                trip_time = int(parts[3])  # Round-trip time
                ttl = int(parts[4]) if len(parts) > 4 and parts[4].isdigit() else 0  # TTL value
                print(f"Reply from {resolved_ip_addr}: bytes={bytes_received} time={trip_time}ms TTL={ttl}")
            else:
                print("Error: Invalid response format.")
        else:
            # Handle unexpected responses, like errors
            error_code = response.split(':')[-1].strip() if ':' in response else response
            print(f"Error code: {error_code}")

        time.sleep(1)  # Optional sleep to avoid flooding the network


if __name__ == "__main__":
    main()