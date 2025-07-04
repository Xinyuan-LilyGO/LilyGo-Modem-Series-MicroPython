'''
#   @file      MqttsBuiltlnAuth.py
#   @license   MIT
#   @copyright Copyright (c) 2025  Shenzhen Xin Yuan Electronic Technology Co., Ltd
#   @date      2025-06-18
#   @note
#   Example is suitable for A7670X/A7608X/SIM7672 series
#   Connect MQTT Broker as https://www.emqx.com/zh/mqtt/public-mqtt5-broker
'''
import time
import machine
import utilities
import ubinascii
from umqtt.robust import MQTTClient
from emqxCa import EmqxRootCa

# It depends on the operator whether to set up an APN. If some operators do not set up an APN,
# they will be rejected when registering for the network. You need to ask the local operator for the specific APN.
# APNs from other operators are welcome to submit PRs for filling.
# Network and MQTT settings
APN = ""  # Replace with your APN (CHN-CT: China Telecom)
mqtt_broker = "broker.emqx.io"  # MQTT Broker address
mqtt_port = 8883  # Secure MQTT port (SSL)
mqtt_client_id = "A76XX"  # Unique client ID for MQTT
mqtt_publish_topic = "GsmMqttTest/publish"  # Topic for publishing messages
mqtt_subscribe_topic = "GsmMqttTest/subscribe"  # Topic for subscribing to messages

# Initialize the serial interface for the modem
uart = machine.UART(1, baudrate=utilities.MODEM_BAUDRATE, tx=utilities.MODEM_TX_PIN, rx=utilities.MODEM_RX_PIN)
time.sleep(1)
__ssl = 0  # SSL flag

# Function to send AT commands to the modem
def send_at_command(command, wait=1):
    uart.write(command + "\r")  # Send the AT command
    time.sleep(wait)  # Wait for a response
    response = uart.read()  # Read the response
    if response:
        return response.decode("utf-8", "ignore").strip()  # Decode and return the response
    return ""

# Function to power on the modem
def modem_power_on():
    machine.Pin(utilities.BOARD_PWRKEY_PIN, machine.Pin.OUT).value(0)  # Activate power key
    time.sleep(0.1)
    machine.Pin(utilities.BOARD_PWRKEY_PIN, machine.Pin.OUT).value(1)  # Deactivate power key
    time.sleep(0.1)
    machine.Pin(utilities.BOARD_PWRKEY_PIN, machine.Pin.OUT).value(0)  # Set power key low again

# Function to reset the modem
def modem_reset():
    machine.Pin(utilities.MODEM_RESET_PIN, machine.Pin.OUT).value(0)  # Pull reset pin low
    time.sleep(0.1)
    machine.Pin(utilities.MODEM_RESET_PIN, machine.Pin.OUT).value(1)  # Pull reset pin high
    time.sleep(2)  # Wait for modem to reset

# Function to check if the modem is ready
def check_modem():
    print("Starting modem...")
    while True:
        response = send_at_command("AT")  # Send basic AT command
        if "OK" in response:  # Check if modem responds with OK
            print()  # Print a newline for clarity
            break
        else:
            print(".", end="", flush=True)  # Print dots until modem responds

# Function to verify SIM status
def check_sim():
    while True:
        sim_status = send_at_command("AT+CPIN?")  # Check the SIM PIN status
        if "READY" in sim_status:  # SIM is ready to use
            print("SIM card online")
            break
        elif "SIM not inserted" in sim_status:
            print("SIM not inserted.")  # SIM card not detected
        else:
            print("The SIM card is locked. Please unlock the SIM card first.")
            time.sleep(3)  # Wait before checking again

# Function to connect to the network using specified APN
def connect_network(apn):
    send_at_command(f"AT+CGDCONT=1,\"IP\",\"{apn}\"")  # Set the PDP context
    send_at_command("AT+CGATT=1")  # Attach to the GPRS network
    response = send_at_command("AT+NETOPEN")  # Open the network connection
    if "OK" in response or "+NETOPEN: 0" in response:  # Check for successful connection
        print("Online registration successful")
    else:
        print("Network registration was rejected, please check if the APN is correct")
        return
    # Get the IP address assigned to the device
    ip_response = send_at_command("AT+IPADDR")
    if ip_response:
        print("Network IP:", ip_response)  # Print the IP address
    else:
        print("Failed to retrieve IP address.")

# MQTT connection function
def mqtt_connect(client_index, server, port, client_id, keepalive_time=60):
    global __ssl
    # Set the MQTT client ID
    response_id = send_at_command(f"AT+CMQTTACCQ={client_index},\"{client_id}\",{__ssl}")
    print(response_id)
    # Set the MQTT version (3.1.1 by default, indicated by '4')
    response_ver = send_at_command(f"AT+CMQTTCFG=\"version\",{client_index},4")
    print(response_ver)
    # Build the connection command
    response_broker = send_at_command(f"AT+CMQTTCONNECT={client_index},\"tcp://{server}:{port}\",{keepalive_time},1", wait=5)
    print(response_broker)
    # Check if the connection was successful
    if "+CMQTTCONNECT: 0,0" in response_broker:
        return True
    else:
        return False

# Function to check if already connected to MQTT
def mqtt_connected():
    response_con = send_at_command("AT+CMQTTDISC?")  # Check MQTT connection status
    if "OK" in response_con:
        return True  # Connected to MQTT

# Function to set SSL certificates for secure connection
def mqtt_set_certificate(ca_file, client_cert_file=None, client_cert_key=None):
    global cert_pem, client_cert_pem, client_key_pem
    cert_pem = ca_file  # CA root certificate
    client_cert_pem = client_cert_file  # Client certificate (if applicable)
    client_key_pem = client_cert_key  # Client certificate key (if applicable)

# Full MQTT connection process with SSL
def mqtt_connecting(client_index, server, port, client_id, ssl, keepalive_time=60):
    global __ssl, cert_pem
    __ssl = ssl
    auth_method = 0  # No authentication (0 = no authentication, 1 = server authentication, 2 = server + client authentication)
    # Start the MQTT service
    response = send_at_command("AT+CMQTTSTART")
    print(response)
    print(f"Connecting to: {mqtt_broker}")
    
    # Set up EMQX ROOT certificate
    mqtt_set_certificate(EmqxRootCa)

    if (cert_pem or client_cert_pem or client_key_pem):
        if (cert_pem):
            response = send_at_command(f"AT+CCERTDOWN=\"ca_cert.pem\",{len(cert_pem)}")  # Download CA certificate
            print(response)
            if ">" not in response:
                return False  # Error if not waiting for prompt
            uart.write(cert_pem)  # Send CA certificate to modem
            uart.write(b"\r\n")  # End the certificate with a newline
            response = send_at_command("")  # Wait for the response
            print(response)
            if "OK" not in response:
                return False  # Error if CA certificate was not accepted
            response = send_at_command("AT+CSSLCFG=\"cacert\",0,\"ca_cert.pem\"")  # Configure CA for SSL
            print(response)
        
        if (client_cert_pem):
            response = send_at_command(f"AT+CCERTDOWN=\"cert.pem\",{len(client_cert_pem)}")  # Download CA certificate
            print(response)
            if ">" not in response:
                return False  # Error if not waiting for prompt
            uart.write(client_cert_pem)  # Send CA certificate to modem
            uart.write(b"\r\n")  # End the certificate with a newline
            response = send_at_command("")  # Wait for the response
            print(response)
            if "OK" not in response:
                return False  # Error if CA certificate was not accepted
            response = send_at_command("AT+CSSLCFG=\"clientcert\",0,\"cert.pem\"")  # Configure CA for SSL
            print(response)
        
        if (client_key_pem):
            response = send_at_command(f"AT+CCERTDOWN=\"key_cert.pem\",{len(client_key_pem)}")  # Download CA certificate
            print(response)
            if ">" not in response:
                return False  # Error if not waiting for prompt
            uart.write(client_key_pem)  # Send CA certificate to modem
            uart.write(b"\r\n")  # End the certificate with a newline
            response = send_at_command("")  # Wait for the response
            print(response)
            if "OK" not in response:
                return False  # Error if CA certificate was not accepted
            response = send_at_command("AT+CSSLCFG=\"clientkey\",0,\"key_cert.pem\"")  # Configure CA for SSL
            print(response)

        # Determine the authentication method based on provided certificates
        if (client_cert_pem and client_key_pem and not cert_pem):
            authMethod = 3  # Client authentication only
        elif (client_cert_pem and client_key_pem and cert_pem):
            authMethod = 2  # Server + client authentication
        elif (cert_pem):
            authMethod = 1  # Server authentication only
        else:
            authMethod = 0  # No authentication
        
        response = send_at_command("AT+CSSLCFG=\"sslversion\",0,4")  # Set SSL version to TLS 1.2
        print(response)
        response = send_at_command(f"AT+CMQTTSSLCFG={client_index},0")  # Enable SSL for MQTT
        print(response)
        __ssl = 1  # Set SSL flag
        
    # Set the authentication mode
    response_auth = send_at_command(f"AT+CSSLCFG=\"authmode\",0,{authMethod}")  # Authentication mode
    print(response_auth)
    
    print(send_at_command("AT+CMQTTREL=0"))  # Release any previous connection
    ret = mqtt_connect(client_index, mqtt_broker, mqtt_port, mqtt_client_id)  # Connect to MQTT
    if ret:
        print("Successfully connected.")
    else:
        print("Failed to connect")
        return False

    # Check MQTT connection status
    if mqtt_connected():
        print("MQTT has connected!")
    else:
        return False
    
    mqtt_subscribe(client_index, mqtt_publish_topic)  # Subscribe to the publish topic
    return True

# Function to subscribe to an MQTT topic
def mqtt_subscribe(client_index, mqtt_publish_topic, qos=0, dup=0):
    command_sub = "AT+CMQTTSUB={},{},{},{}".format(client_index, len(mqtt_publish_topic), qos, dup)
    response_sub = send_at_command(command_sub)  # Send subscribe command
    print(response_sub)
    if ">" not in response_sub:  # Wait for response prompt
        return False
    uart.write(mqtt_publish_topic.encode())  # Send the topic as bytes
    uart.write(b"\r\n")  # Send the topic with a newline
    response = send_at_command("")  # Wait for response to the topic
    print(response)
    if "OK" not in response:
        return False  # If not acknowledged

# Function to publish a message to an MQTT topic
def mqtt_publish(client_index, topic, message):
    # Step 1: Send the topic
    command = f"AT+CMQTTTOPIC={client_index},{len(topic)}"
    response = send_at_command(command)  # Send topic command
    print(response)
    if ">" not in response:  # Wait for ">" prompt
        return False
    uart.write(topic.encode())  # Send topic as bytes
    uart.write(b"\r\n")  # Send the topic with a newline
    response = send_at_command("")  # Wait for response to the topic
    print(response)
    if "OK" not in response:
        return False

    # Send the message (message body)
    command = f"AT+CMQTTPAYLOAD={client_index},{len(message)}"
    response = send_at_command(command)  # Send message payload command
    print(response)
    if ">" not in response:  # Wait for ">" prompt
        return False
    uart.write(message.encode())  # Send message as bytes
    uart.write(b"\r\n")  # Send the message with a newline
    response = send_at_command("")  # Wait for response to the message
    print(response)
    if "OK" not in response:
        return False
    
    # Send the publish command with QoS and timeout
    qos = 0  # Quality of service level
    timeout = 60  # Timeout for the publish
    command = f"AT+CMQTTPUB={client_index},{qos},{timeout},0,0"
    response = send_at_command(command)  # Send publish command
    print(response)
    if "OK" not in response:
        return False  # If not acknowledged
    return True  # Publish was successful

# Main function that orchestrates the modem operation and MQTT connection
def main():
    print("Starting sketch...")
    modem_power_on()  # Power on the modem
    modem_reset()  # Reset the modem
    check_modem()  # Verify the modem is operational
    check_sim()  # Check SIM card status
    print("Wait for the modem to register with the network.")
    send_at_command("AT+CREG?")  # Query network registration status
    send_at_command("AT+SIMCOMATI")  # Request modem version
    connect_network(APN)  # Connect to the network with the specified APN

    # MQTT Client Index
    client_index = 0  # Set the client index to 0 (can be adjusted if needed)
    
    # Initialize MQTT, use SSL
    ssl = 1  # Enable SSL
    if mqtt_connecting(client_index, mqtt_broker, mqtt_port, mqtt_client_id, ssl):
        # Publish messages periodically
        try:
            check_connect_millis = 0
            while True:
                current_millis = time.ticks_ms()  # Get current time in milliseconds
                if current_millis > check_connect_millis:
                    check_connect_millis = current_millis + 10000  # Check every 10 seconds
                    if not mqtt_connected():  # If not connected, attempt to reconnect
                        mqtt_connecting(client_index, mqtt_broker, mqtt_port, mqtt_client_id, ssl)
                    else:
                        payload = "RunTime:" + str(current_millis // 1000)  # Prepare payload with runtime
                        mqtt_publish(client_index, mqtt_publish_topic, payload)  # Publish the payload
                time.sleep(0.005)  # Small delay to avoid busy loop
        except KeyboardInterrupt:
            print("Exiting MQTT loop...")  # Handle exit gracefully
    else:
        return

if __name__ == "__main__":
    main()  # Run the main function