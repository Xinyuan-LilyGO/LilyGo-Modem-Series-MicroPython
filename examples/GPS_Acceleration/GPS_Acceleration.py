''' 
 * @file      GPS_Acceleration.py
 * @license   MIT
 * @copyright Copyright (c) 2025  Shenzhen Xin Yuan Electronic Technology Co., Ltd
 * @date      2025-07-22
 * @note
 *            GPS acceleration only supports A7670X/A7608X (excluding A7670G and other versions that do not support positioning).
'''
import machine
import time
from machine import UART, Pin
import utilities

# It depends on the operator whether to set up an APN. If some operators do not set up an APN,
# they will be rejected when registering for the network. You need to ask the local operator for the specific APN.
# APNs from other operators are welcome to submit PRs for filling.
APN = ""  # Replace with your APN (CHN-CT: China Telecom)

# Initialize UART for modem communication
SerialAT = UART(1, baudrate=utilities.MODEM_BAUDRATE, tx=utilities.MODEM_TX_PIN, rx=utilities.MODEM_RX_PIN)

# Initialize pins
pwrkey = Pin(utilities.BOARD_PWRKEY_PIN, Pin.OUT)
poweron = Pin(utilities.BOARD_POWERON_PIN, Pin.OUT)
reset_pin = Pin(utilities.MODEM_RESET_PIN, Pin.OUT)
gps_enable = Pin(utilities.MODEM_GPS_ENABLE_GPIO, Pin.OUT)

def send_at_command(command, wait=1):
    SerialAT.write(command + "\r\n")
    time.sleep(wait)
    response = SerialAT.read()
    if response:
        if isinstance(response, bytes) and len(response) > 0:
            try:
                return response.decode("utf-8", "ignore").strip()
            except: 
                return ""
    return ""

def check_modem():
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
            print("The SIM card is locked, please unlock the SIM card first. Or wait minutes. ")
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

    # Get the IP address
    ip_response = send_at_command("AT+IPADDR")
    if ip_response:
        print("Network IP:", ip_response)
    else:
        print("Failed to retrieve IP address.")
        
def modem_setup():
    # Turn on DC boost to power on the modem
    poweron.value(1)
    
    # Set modem reset pin ,reset modem
    reset_pin.value(not utilities.MODEM_RESET_LEVEL)
    time.sleep(0.1)
    reset_pin.value(utilities.MODEM_RESET_LEVEL)
    time.sleep(2.6)
    reset_pin.value(not utilities.MODEM_RESET_LEVEL)
    
    # Turn on modem
    pwrkey.value(0)
    time.sleep(0.1)
    pwrkey.value(1)
    time.sleep(1)
    pwrkey.value(0)
    
    print("Start modem...")
    check_modem()
    check_sim()
    send_at_command("AT+SIMCOMATI")
    connect_network(APN)    
    time.sleep(3)
    
    retry = 0
    while True:
        response = send_at_command("AT")
        if "OK" in response:
            break
        print(".")
        retry += 1
        if retry > 10:
            pwrkey.value(0)
            time.sleep(0.1)
            pwrkey.value(1)
            time.sleep(1)
            pwrkey.value(0)
            retry = 0
    print()
    time.sleep(0.2)
    
    # Get modem info
    modem_name = "UNKNOWN"
    while True:
        response = send_at_command("AT+CGMM")
        print(response)
        if "OK" in response:
            modem_name = response.split("\r\n")[1]
            if "A7670G" in modem_name:
                while True:
                    print("A7670G does not support built-in GPS function, please run examples/GPSShield")
                    time.sleep(1)
            else:
                print("Model Name:", modem_name)
                break
        else:
            print("Unable to obtain module information normally, try again")
            time.sleep(1)
        time.sleep(5)
    
    # Send SIMCOMATI command
    response = send_at_command("AT+SIMCOMATI")
    print(response)
    
    '''
    A7608 B08 firmware has GPS positioning problems. If it is B08 version, you need to upgrade the A7608 firmware.
    
    Manufacturer: INCORPORATED
    Model: A7608SA-H
    Revision: A50C4B08A7600M7
    A7600M7_B08V02_220929
    QCN:
    IMEI: xxxxxxxxxxxxx
    MEID:
    +GCAP: +CGSM,+FCLASS,+DS
    DeviceInfo:
    
    +CGNSSINFO: 2,04,00,21.xxxxx,N,114.xxxxxxxx,E,020924,094145.00,-34.0,1.403,,6.9,6.8,1.0,03
    '''
    
    print("Enabling GPS/GNSS/GLONASS")
    response = send_at_command("AT+CVAUXS=1")
    print(response)
    response = send_at_command("AT+CGPSHOT")
    print(response)
    while True:
        gps_enable.value(utilities.MODEM_GPS_ENABLE_LEVEL)
        response = send_at_command("AT+CGNSSPWR=1")
        print(response)
        if response:
            break
        print(".", end="")
        
    print("\nGPS Enabled")

    # Set GPS Baud to 115200
    response = send_at_command("AT+CGNSSIPR=115200")
    print(response)

def get_gps_data():
    while True:
        print("Requesting current GPS/GNSS/GLONASS location")
        response = send_at_command("AT+CGNSSINFO",wait=3)
        print(response)
        if "+CGNSSINFO: ,,,,,,,," not in response and "ERROR" not in response:
            data = response.split("+CGNSSINFO: ")[1].split("\n")[0] 
            values = data.split(",")
            if len(values) >= 1:  
                fixMode = values[0]  # Fix mode
                lat2 = float(values[5])  # Latitude
                lon2 = float(values[7])  # Longitude
                if values[12] is not "":
                    speed2 = float(values[12])  # Speed
                else:
                    speed2 = 0.0
                alt2 = float(values[11])  # Altitude
                vsat2 = int(values[1])  # Visible satellites
                usat2 = 0  # GPS_BuiltIn cannot get the number of used satellites
                accuracy2 = float(values[16])  # Accuracy
                
                date_str = values[9]  # Date
                time_str = values[10]  # Time
                year2 = int(date_str[4:6])  # Year
                month2 = int(date_str[2:4])  # Month
                day2 = int(date_str[:2])  # Day
                hour2 = int(time_str[:2])  # Hour
                min2 = int(time_str[2:4])  # Minute
                sec2 = float(time_str[4:])  # Second
                
                # Convert UTC time to local time by adding time zone offset
                timezone_offset = 8  # CST is UTC+8

                # Adjust hours based on timezone offset
                hour2 += timezone_offset
                if hour2 >= 24:
                    hour2 -= 24
                elif hour2 < 0:
                    hour2 += 24

                print("FixMode:", fixMode)
                print("Latitude:", lat2, "\tLongitude:", lon2)
                print("Speed:", speed2, "\tAltitude:", alt2)
                print("Visible Satellites:", vsat2, "\tUsed Satellites:", usat2)
                print("Accuracy:", accuracy2)
                print("Year:", year2, "\tMonth:", month2, "\tDay:", day2)
                print("Hour:", hour2, "\tMinute:", min2, "\tSecond:", int(sec2))
                break
        else:
            print("Couldn't get GPS/GNSS/GLONASS location, retrying in 15s.")
            time.sleep(15)
    
    print("Retrieving GPS/GNSS/GLONASS location again as a string")
    gps_raw = send_at_command("AT+CGNSSINFO")
    print("GPS/GNSS Based Location String:", gps_raw.split("\r\n")[1])
    print("Disabling GPS")
#     gps_enable.value(not utilities.MODEM_GPS_ENABLE_LEVEL)
    response = send_at_command("AT+CGNSSPWR=0")
    print(response)

def main():
    modem_setup()
    print("GPS acceleration is enabled")
    response = send_at_command("AT+CGNSSPWR?")
    print(response)
    response = send_at_command("AT+CAGPS")
    print(response)
    if 'OK' in response:
        print(" success!!!")
    else:
        print(" failed!!!")
    get_gps_data()
    # Just echo serial data
    while True:
        if SerialAT.any():
            print(SerialAT.read().decode(), end="")
        time.sleep(0.001)

if __name__ == "__main__":
    main()