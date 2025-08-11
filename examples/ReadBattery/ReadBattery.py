'''
#   @file      ReadBattery.py
#   @license   MIT
#   @copyright Copyright (c) 2025  Shenzhen Xin Yuan Electronic Technology Co., Ltd
#   @date      2025-06-11
#   @note      Reading the battery voltage information is only applicable to the V1.2 version.
#              T-A7670x :  The V1.1 version does not have a battery voltage divider.
#                           If V1.1 needs to be read, then you need to add a 100K 1% voltage divider resistor between the battery and GND
#                           When connected to the USB, the battery voltage data read is not the real battery voltage, so the battery
#                           voltage is sent to the UDP Server through UDP. When using it, please disconnect the USB-C
#              T-A7670x :  Only version V1.4 has the resistor divider connected to the solar input, other versions IO38 is not connected
#   @note      Only support T-A7670 ,T-A7608X, T-SIM7672G board , not support T-Call A7670 , T-PCIE-A7670
#
#              The AT+CBC command only supports the following versions , Other versions cannot read it because the hardware is not connected.
#                1. T-A7670X-S3-Standard
#                2. T-SIM7000G-S3-Standard
#                3. T-SIM7080G-S3-Standard
#                4. T-SIM7670G-S3-Standard
'''
import network
import socket
import time
from machine import ADC, Pin
import utilities

# Wi-Fi network information
network_name = "your-ssid"
network_password = "your-password"

# UDP address and port
udp_address = "192.168.36.188"  # Replace with your receiver's IP
udp_port = 3336

# Initialize ADC
battery_adc = ADC(Pin(utilities.BOARD_BAT_ADC_PIN))  # Replace with the actual ADC pin
battery_adc.atten(ADC.ATTN_11DB)  # Set attenuation
battery_adc.width(ADC.WIDTH_12BIT)  # Set resolution to 12 bits

# Connect to Wi-Fi
def connect_to_wifi(ssid, pwd):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, pwd)

    print(f"Connecting to WiFi network: {ssid}")
    while not wlan.isconnected():
        time.sleep(1)
    print(f"WiFi connected! IP address: {wlan.ifconfig()[0]}")

# Initialize UDP
def init_udp():
    addr_info = socket.getaddrinfo(udp_address, udp_port)
    addr = addr_info[0][-1]
    
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)  # Allow broadcast
    return udp_socket, addr

# Main loop
def main():
    connect_to_wifi(network_name, network_password)
    udp_socket, addr = init_udp()

    while True:
        time.sleep(1)  # Check once every second
        battery_voltage = battery_adc.read() * 2  # Read battery voltage and multiply by 2
        
        # Print battery voltage
        buf = f"Battery:{battery_voltage}mV"
        print(buf)

        # Send UDP data
        try:
            udp_socket.sendto(buf.encode('utf-8'), (udp_address, udp_port))
        except OSError as e:
            print(f"Error sending data: {e}")

# Testing and running
try:
    main()
except KeyboardInterrupt:
    print("Program stopped")