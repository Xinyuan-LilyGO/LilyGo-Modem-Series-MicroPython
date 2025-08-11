'''
#   @file      MqttsBuiltlnNoSSL.py
#   @license   MIT
#   @copyright Copyright (c) 2025  Shenzhen Xin Yuan Electronic Technology Co., Ltd
#   @date      2025-08-04
#   @note
#    Example is suitable for A7670X/A7608X/SIM7670G/SIM7600 series
#    TODO: SIM7000G To be fixed
#    Connect MQTT Broker as https://test.mosquitto.org/  MQTT, encrypted, unauthenticated
'''
import time
import machine
import utilities
import ubinascii
from umqtt.robust import MQTTClient
import re

# It depends on the operator whether to set up an APN. If some operators do not set up an APN,
# they will be rejected when registering for the network. You need to ask the local operator for the specific APN.
# APNs from other operators are welcome to submit PRs for filling.
# Network and MQTT settings
APN = ""  # Replace with your APN (CHN-CT: China Telecom)
mqtt_broker = "test.mosquitto.org"  # MQTT Broker address
mqtt_port = 1883  # Non-secure MQTT port
mqtt_client_id = "A76XX"
mqtt_publish_topic = "GsmMqttTest/publish"  # Publish topic
mqtt_subscribe_topic = "GsmMqttTest/subscribe"  # Subscribe topic

# Initialize the serial interface for the modem
uart = machine.UART(1, baudrate=utilities.MODEM_BAUDRATE, tx=utilities.MODEM_TX_PIN, rx=utilities.MODEM_RX_PIN)
time.sleep(1)
__ssl = 0

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
        response = send_at_command("AT+CNACT?",wait=3)
        print(response)
        response = send_at_command("AT+CNACT=1",wait=3)
        print(response)
        response = send_at_command("AT+CNACT?",wait=3)
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

# MQTT connection function
def mqtt_connect(client_index, server, port, client_id, keepalive_time=60):
    global __ssl
    if utilities.CURRENT_PLATFORM == "LILYGO_T_SIM7000G":
        response = send_at_command('AT+SMCONN')
        print(response)
        if response:
            return True
        else:
            return False
    else:
        # Set the client ID
        response_id = send_at_command(f"AT+CMQTTACCQ={client_index},\"{client_id}\",{__ssl}")
        print(response_id)
        # Set the MQTT version (3.1.1 by default)
        response_ver = send_at_command(f"AT+CMQTTCFG=\"version\",{client_index},4")
        print(response_ver)
        # Build the connection command
        while True:
            response_broker = send_at_command(f"AT+CMQTTCONNECT=0,\"tcp://{server}:{port}\",{keepalive_time},1",wait=3)
            # Check if the connection was successful
            if "+CMQTTCONNECT: 0,0" in response_broker:
                break
            else:
                print("wait mqttconnect.")
        return True

def mqtt_connected():
    if utilities.CURRENT_PLATFORM == "LILYGO_T_SIM7000G":
        response = send_at_command('AT+SMSTATE?')
        print(response)
        if "OK" in response_con:
            return True
    else:
        response_con = send_at_command("AT+CMQTTDISC?")
        if "OK" in response_con:
            return True

def mqtt_connecting(client_index, server, port, client_id, ssl, keepalive_time=60):
    global __ssl
    if utilities.CURRENT_PLATFORM == "LILYGO_T_SIM7000G":
        response = send_at_command("AT+SMDISC")
        print(response)
        print(f"Connecting to: {mqtt_broker}")
        response = send_at_command("AT+SMSSL=0")
        print(response)
        response = send_at_command('AT+SMCONF="KEEPTIME",60')
        print(response)
        response = send_at_command('AT+SMCONF="CLEANSS",1')
        print(response)
        response = send_at_command('AT+SMCONF="QOS",0')
        print(response)
        response = send_at_command('AT+SMCONF="RETAIN",1')
        print(response)
        response = send_at_command(f'AT+SMCONF="CLIENTID",{mqtt_client_id}')
        print(response)
        response = send_at_command(f'AT+SMCONF=URL,"{mqtt_broker}",{mqtt_port}')
        print(response)
        ret = mqtt_connect(client_index, mqtt_broker, mqtt_port, mqtt_client_id)
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
    else:
        __ssl = ssl
        auth_method = 0  # No authentication (0 = no authentication, 1 = server authentication, 2 = server + client authentication)
        # Start the MQTT service
        response = send_at_command("AT+CMQTTSTART")
        print(response)
        # Set the authentication mode (0 = no auth)
        response_auth = send_at_command("AT+CSSLCFG=\"authmode\",0,0")  # No SSL
        print(f"Connecting to: {mqtt_broker}", response_auth)
        print(send_at_command("AT+CMQTTREL=0"))
        ret = mqtt_connect(client_index, mqtt_broker, mqtt_port, mqtt_client_id)
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
    if utilities.CURRENT_PLATFORM == "LILYGO_T_SIM7000G":
        response = send_at_command(f'AT+SMSUB="{mqtt_subscribe_topic}",0',wait=3)
        print(response)
    else:
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
    if utilities.CURRENT_PLATFORM == "LILYGO_T_SIM7000G":
        response = send_at_command(f'AT+SMPUB="{mqtt_publish_topic}",10,0,1',wait=3)
        print(response)
        uart.write(message.encode())
        time.sleep(5)
        uart.write(b"\r\n") 
        response = send_at_command("")
        print(response)
        response = send_at_command('AT+SMSTATE?')
        print(response)
    else:
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
    # Initialize MQTT, use SSL, skip authentication server
    ssl = 0
    if mqtt_connecting(client_index, mqtt_broker, mqtt_port, mqtt_client_id, ssl):
        # Publish messages periodically
        try:
            check_connect_millis = 0
            while True:
                current_millis = time.ticks_ms()
                if current_millis > check_connect_millis:
                    check_connect_millis = current_millis + 10000
                    payload = "RunTime:" + str(current_millis // 1000)
                    mqtt_publish(client_index, mqtt_publish_topic, payload)
                time.sleep(0.005)
        except KeyboardInterrupt:
            print("Exiting MQTT loop...")
    else:
        return

if __name__ == "__main__":
    main()