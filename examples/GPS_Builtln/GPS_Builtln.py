'''
 * @file      GPS_BuiltIn.py
 * @license   MIT
 * @copyright Copyright (c) 2025  Shenzhen Xin Yuan Electronic Technology Co., Ltd
 * @date      2025-08-13
 * @note      GPS only supports A7670X/A7608X/SIM7000G/SIM7600 series (excluding A7670G and other versions that do not support positioning).
'''
import machine
import time
from machine import UART, Pin
import utilities

# Initialize UART for modem communication
SerialAT = UART(1, baudrate=utilities.MODEM_BAUDRATE, tx=utilities.MODEM_TX_PIN, rx=utilities.MODEM_RX_PIN)

# Initialize pins
try:
    pwrkey = Pin(utilities.BOARD_PWRKEY_PIN, Pin.OUT)
except:
    pass

try:
    poweron = Pin(utilities.BOARD_POWERON_PIN, Pin.OUT)
except:
    pass

try:
    reset_pin = Pin(utilities.MODEM_RESET_PIN, Pin.OUT)
except:
    pass

try:
    gps_enable = Pin(utilities.MODEM_GPS_ENABLE_GPIO, Pin.OUT)
except:
    pass

def send_at_command(command, wait=1):
    SerialAT.write(command + "\r\n")
    time.sleep(wait)
    response = SerialAT.read()
#     print("Raw response:", response)  # Debug line
    if response:
        if isinstance(response, bytes) and len(response) > 0:
            try:
                return response.decode("utf-8", "ignore").strip()
            except:  # This should be fine
                return ""
    return ""

def modem_setup():
    # Turn on DC boost to power on the modem
    try:
        poweron.value(1)
    except:
        pass
    
    # Set modem reset pin ,reset modem
    try:
        reset_pin.value(not utilities.MODEM_RESET_LEVEL)
        time.sleep(0.1)
        reset_pin.value(utilities.MODEM_RESET_LEVEL)
        time.sleep(2.6)
        reset_pin.value(not utilities.MODEM_RESET_LEVEL)
    except:
        pass
    
    try:
        machine.Pin(utilities.MODEM_DTR_PIN, machine.Pin.OUT).value(0)
    except:
        pass
    
    # Turn on modem
    try:
        pwrkey.value(0)
        time.sleep(0.1)
        pwrkey.value(1)
        time.sleep(1)
        pwrkey.value(0)
    except:
        pass
    
    print("Start modem...")
    time.sleep(3)
    retry = 0
    while True:
        response = send_at_command("AT")
        if "OK" in response:
            break
        print(".")
        retry += 1
        if retry > 10:
            try:
                pwrkey.value(0)
                time.sleep(0.1)
                pwrkey.value(1)
                time.sleep(1)
                pwrkey.value(0)
            except:
                pass
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
    
#     A7608 B08 firmware has GPS positioning problems. If it is B08 version, you need to upgrade the A7608 firmware.
#     
#     Manufacturer: INCORPORATED
#     Model: A7608SA-H
#     Revision: A50C4B08A7600M7
#     A7600M7_B08V02_220929
#     QCN:
#     IMEI: xxxxxxxxxxxxx
#     MEID:
#     +GCAP: +CGSM,+FCLASS,+DS
#     DeviceInfo:
#     
#     +CGNSSINFO: 2,04,00,21.xxxxx,N,114.xxxxxxxx,E,020924,094145.00,-34.0,1.403,,6.9,6.8,1.0,03
    
    print("Enabling GPS/GNSS/GLONASS")
    if utilities.CURRENT_PLATFORM == "LILYGO_T_SIM7000G" \
       or utilities.CURRENT_PLATFORM == "LILYGO_T_SIM7000G_S3_STAN" \
        or utilities.CURRENT_PLATFORM == "LILYGO_T_SIM7080G_S3_STAN":
        response = send_at_command("AT+CGPIO=0,48,1,1")
        print(response)
        while True:
            try:
                gps_enable.value(utilities.MODEM_GPS_ENABLE_LEVEL)
            except:
                pass
            response = send_at_command("AT+CGNSPWR=1")
            print(response)
            if 'OK' in response:
                break
            print(".", end="")
        print("\nGPS Enabled")
    else:
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
    if utilities.CURRENT_PLATFORM == "LILYGO_T_SIM7000G" \
       or utilities.CURRENT_PLATFORM == "LILYGO_T_SIM7000G_S3_STAN" \
        or utilities.CURRENT_PLATFORM == "LILYGO_T_SIM7080G_S3_STAN":
        while True:
            print("Requesting current GPS/GNSS/GLONASS location")
            response = send_at_command("AT+CGNSINF",wait=3)
            print(response)
            if "+CGNSINF: ,,,,,,,," not in response and "ERROR" not in response and ",,,,,,," not in response:
                data = response.split("+CGNSINF: ")[1].split("\n")[0] 
                values = data.split(",")
                if len(values) >= 1:  
                    fixMode = values[8]  # Fix mode
                    lat2 = float(values[3])  # Latitude
                    lon2 = float(values[4])  # Longitude
                    if values[6] is not "":
                        speed2 = float(values[6])  # Speed
                    else:
                        speed2 = 0.0
                    alt2 = float(values[5])  # Altitude
                    vsat2 = int(values[14])  # Visible satellites
                    usat2 = 0  # GPS_BuiltIn cannot get the number of used satellites
                    accuracy2 = float(values[11])  # Accuracy
                    
                    date_str = values[2]  # Date Time
                    year2 = int(date_str[:4]) # Year
                    month2 = int(date_str[4:6])  # Month
                    day2 = int(date_str[6:8])  # Day
                    hour2 = int(date_str[8:10])  # Hour
                    min2 = int(date_str[10:12])  # Minute
                    sec2 = float(date_str[12:14])  # Second
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
        gps_raw = send_at_command("AT+CGNSINF")
        print("GPS/GNSS Based Location String:", gps_raw.split("\r\n")[1])
        print("Disabling GPS")
        response = send_at_command("AT+CGNSPWR=0")
        print(response)
    else:
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
        response = send_at_command("AT+CGNSSPWR=0")
        print(response)

def main():
    modem_setup()
    get_gps_data()
    # Just echo serial data
    while True:
        if SerialAT.any():
            print(SerialAT.read().decode(), end="")
        time.sleep(0.001)

if __name__ == "__main__":
    main()