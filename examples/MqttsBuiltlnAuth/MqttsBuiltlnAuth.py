'''
#   @file      MqttsBuiltlnAuth.py
#   @license   MIT
#   @copyright Copyright (c) 2025  Shenzhen Xin Yuan Electronic Technology Co., Ltd
#   @date      2025-06-16
#   @note
#   Example is suitable for A7670X/A7608X/SIM7672 series
#   Connect MQTT Broker as https://test.mosquitto.org/
'''
import time
import machine
import utilities
import ubinascii
from umqtt.robust import MQTTClient

# It depends on the operator whether to set up an APN. If some operators do not set up an APN,
# they will be rejected when registering for the network. You need to ask the local operator for the specific APN.
# APNs from other operators are welcome to submit PRs for filling.
# Network and MQTT settings
APN = ""  # Replace with your APN (CHN-CT: China Telecom)
mqtt_broker = "test.mosquitto.org"  # MQTT Broker address
mqtt_port = 8885  # Non-secure MQTT port
mqtt_client_id = "A76XX"
mqtt_username = "rw"  # MQTT username
mqtt_password = "readwrite"  # MQTT password
mqtt_publish_topic = "GsmMqttTest/publish"  # Publish topic
mqtt_subscribe_topic = "GsmMqttTest/subscribe"  # Subscribe topic

# Initialize the serial interface for the modem
uart = machine.UART(1, baudrate=utilities.MODEM_BAUDRATE, tx=utilities.MODEM_TX_PIN, rx=utilities.MODEM_RX_PIN)
time.sleep(1)

def send_at_command(command):
    uart.write(command + "\r")
    time.sleep(1)
    response = uart.read()
    if response:
        return response.decode("utf-8", "ignore").strip()
    return ""

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

def check_modem():
    print("Starting modem...")
    while True:
        response = send_at_command("AT")
        if "OK" in response:
            print()  # Print a newline for clarity
            break
        else:
            print(".", end="", flush=True)

def check_sim():
    while True:
        sim_status = send_at_command("AT+CPIN?")
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
    response = send_at_command("AT+NETOPEN")
    if "OK" in response or "+NETOPEN: 0" in response:
        print("Online registration successful")
    else:
        print("Network registration was rejected, please check if the APN is correct")
        return
    # Get the IP address
    ip_response = send_at_command("AT+IPADDR")
    if ip_response:
        print("Network IP:", ip_response)
    else:
        print("Failed to retrieve IP address.")

# MQTT connection function
def mqtt_connect(client_index, server, port, client_id, username=None, password=None, keepalive_time=60):
    # Set the client ID
    response_id = send_at_command(f"AT+CMQTTACCQ={client_index},\"{client_id}\",1")
    print(response_id)
    # Set the MQTT version (3.1.1 by default)
    response_ver = send_at_command(f"AT+CMQTTCFG=\"version\",{client_index},4")
    print(response_ver)
    # Build the connection command
    if username and password:
        connection_command = f"AT+CMQTTCONNECT=0,\"tcp://{server}:{port}\",{keepalive_time},1,\"{username}\",\"{password}\""
        send_at_command(connection_command)
    else:
        connection_command = f"AT+CMQTTCONNECT=0,\"tcp://{server}:{port}\",{keepalive_time},1"
        send_at_command(connection_command)
    response_broker = send_at_command(connection_command)
#     print(response_broker)
    # Check if the connection was successful
    if "+CMQTTCONNECT: 0,0" in response_broker:
        return True
    else:
        return False
    
def mqtt_connected():
    response_con = send_at_command("AT+CMQTTDISC?")
    if "OK" in response_con:
        return True

def mqtt_connecting(client_index, server, port, client_id, username=None, password=None, keepalive_time=60):
    auth_method = 0  # No authentication (0 = no authentication, 1 = server authentication, 2 = server + client authentication)
    # Start the MQTT service
    response = send_at_command("AT+CMQTTSTART")
    print(response)
    # Set the authentication mode (0 = no auth)
    response_auth = send_at_command("AT+CSSLCFG=\"authmode\",0,0")  # No SSL
    print(f"Connecting to: {mqtt_broker}", response_auth)
    print(send_at_command("AT+CMQTTREL=0"))
    ret = mqtt_connect(client_index, mqtt_broker, mqtt_port, mqtt_client_id, mqtt_username, mqtt_password)
    if ret:
        print("successfully.")
    else:
        print("Failed")
        return False
    if mqtt_connected:
        print("MQTT has connected!")
    else:
        return False
    mqtt_subscribe(client_index,mqtt_publish_topic)
    return True

def mqtt_subscribe(client_index, mqtt_publish_topic, qos=0, dup=0):
    command_sub = "AT+CMQTTSUB={},{},{},{}".format(client_index, len(mqtt_publish_topic), qos, dup)
    response_sub = send_at_command(command_sub)
    print(response_sub)
    if ">" not in response_sub:
        return False
    uart.write(mqtt_publish_topic.encode()) 
    uart.write(b"\r\n") 
    response = send_at_command("")
    print(response)
    if "OK" not in response:
        return False


# MQTT Publish function
def mqtt_publish(client_index, topic, message):
    # Step 1: Send the topic
    command = f"AT+CMQTTTOPIC={client_index},{len(topic)}"
    response = send_at_command(command)
    print(response)
    if ">" not in response:  # Waiting for ">" prompt
        return False
    uart.write(topic.encode())  # Send topic as bytes
    uart.write(b"\r\n")  # Send the topic with a newline
    response = send_at_command("")  # Wait for the response to the topic
    print(response)
    if "OK" not in response:
        return False
    # Step 2: Send the message (message body)
    command = f"AT+CMQTTPAYLOAD={client_index},{len(message)}"
    response = send_at_command(command)
    print(response)
    if ">" not in response:  # Waiting for ">" prompt
        return False
    uart.write(message.encode())  # Send message as bytes
    uart.write(b"\r\n")  # Send the message with a newline
    response = send_at_command("")  # Wait for the response to the message
    print(response)
    if "OK" not in response:
        return False
    # Step 3: Send the publish command with QoS and timeout
    qos = 0
    timeout = 60
    command = f"AT+CMQTTPUB={client_index},{qos},{timeout},0,0"
    response = send_at_command(command)
    print(response)
    if "OK" not in response:
        return False
    return True
    
def main():
    print("Starting sketch...")
    modem_power_on()
    modem_reset()
    check_modem()
    check_sim()
    print("Wait for the modem to register with the network.")
    send_at_command("AT+CREG?")
    send_at_command("AT+SIMCOMATI")
    connect_network(APN)
    # MQTT Client Index
    client_index = 0  # Set the client index to 0 (can be adjusted if needed)
    # Connect to MQTT using port 1883 (non-SSL)
    if mqtt_connecting(client_index, mqtt_broker, mqtt_port, mqtt_client_id, mqtt_username, mqtt_password):
        # Publish messages periodically
        try:
            check_connect_millis = 0
            while True:
                current_millis = time.ticks_ms()
                if current_millis > check_connect_millis:
                    check_connect_millis = current_millis + 10000
                    if not mqtt_connected():
                        mqtt_connecting()
                    else:
                        payload = "RunTime:" + str(current_millis // 1000)
                        mqtt_publish(client_index, mqtt_publish_topic, payload)
                time.sleep(0.005)
        except KeyboardInterrupt:
            print("Exiting MQTT loop...")
    else:
        return

if __name__ == "__main__":
    main()