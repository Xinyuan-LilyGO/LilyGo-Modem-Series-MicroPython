'''
 * @file      GPS_BuiltInEx.py
 * @license   MIT
 * @copyright Copyright (c) 2025  Shenzhen Xin Yuan Electronic Technology Co.,
 * Ltd
 * @date      2025-08-06
 * @note      GPS only supports A7670X/A7608X (excluding A7670G and other
 * versions that do not support positioning).
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

def modem_setup():
    global modemName
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
    modemName = "UNKNOWN"
    while True:
        response = send_at_command("AT+CGMM")
        print(response)
        if "OK" in response:
            modemName = response.split("\r\n")[1]
            if "A7670G" in modemName:
                while True:
                    print("A7670G does not support built-in GPS function, please run examples/GPSShield")
                    time.sleep(1)
            else:
                print("Model Name:", modemName)
                break
        else:
            print("Unable to obtain module information normally, try again")
            time.sleep(1)
        time.sleep(5)
    # Send SIMCOMATI command
    response = send_at_command("AT+SIMCOMATI")
    print(response)
    print("Enabling GPS/GNSS/GLONASS")
    if utilities.CURRENT_PLATFORM == "LILYGO_T_SIM7000G":
        response = send_at_command("AT+CGPIO=0,48,1,1")
        print(response)
        while True:
            gps_enable.value(utilities.MODEM_GPS_ENABLE_LEVEL)
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
    
def loopGPS(gnss_mode):
    if utilities.CURRENT_PLATFORM == "LILYGO_T_SIM7000G":
        print("=========================") 
        print(f"Set GPS Mode : {gnss_mode}")
        if gnss_mode==1:
            response = send_at_command(f"AT+CGNSMOD=1,1,0,0",wait=3)
            print(response)
        elif gnss_mode==3:
            response = send_at_command(f"AT+CGNSMOD=1,1,1,0",wait=3)
            print(response)
        elif gnss_mode==5:
            response = send_at_command(f"AT+CGNSMOD=1,1,0,1",wait=3)
            print(response)
        elif gnss_mode==9:
            response = send_at_command(f"AT+CGNSMOD=1,1,0,0",wait=3)
            print(response)
        elif gnss_mode==13:
            response = send_at_command(f"AT+CGNSMOD=1,1,0,1",wait=3)
            print(response)
        elif gnss_mode==15:
            response = send_at_command(f"AT+CGNSMOD=1,1,1,1",wait=3)
            print(response)
        print("Requesting current GPS/GNSS/GLONASS location")
        while True:
            response = send_at_command("AT+CGNSINF",wait=3)
            print(response)
            if "+CGNSINF: ,,,,,,,," not in response and "ERROR" not in response and ",,,,,,," not in response:
                data = response.split("+CGNSINF: ")[1].split("\n")[0] 
                values = data.split(",")
                try:
                    if len(values) >= 1:  
                        fixMode = values[10]  # Fix mode
                        latitude = float(values[3])  # Latitude
                        longitude = float(values[4])  # Longitude
                        if values[6] is not "":
                            speed = float(values[6])  # Speed
                        else:
                            speed = 0.0
                        altitude = float(values[5])  # Altitude
                        if values[14] == "":
                            gps_satellite_num = 0
                        else:
                            gps_satellite_num = int(values[14])
                        if values[15] == "":
                            beidou_satellite_num = 0
                        else:
                            beidou_satellite_num = int(values[15])
                        if values[16] == "":
                            glonass_satellite_num = 0
                        else:
                            glonass_satellite_num = int(values[16])
                        if values[17] == "":
                            galileo_satellite_num = 0
                        else:
                            galileo_satellite_num = int(values[17])
                        course = 1.0
                        if values[11] == "":
                            PDOP = 0.0
                        else:
                            PDOP = float(values[11])
                        HDOP = float(values[10])
                        VDOP = float(values[12])
                        date_str = values[2]  # Date Time
                        year2 = int(date_str[0:4])  # Year
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
                        print("Latitude:", latitude)
                        print("tLongitude:", longitude)
                        print("Speed:", speed)
                        print("Altitude:", altitude)
                        print("Visible Satellites:")
                        print(" GPS Satellites:", gps_satellite_num)
                        print(" BEIDOU Satellites:", beidou_satellite_num)
                        print(" GLONASS Satellites:", glonass_satellite_num)
                        print(" GALILEO Satellites:", galileo_satellite_num)
                        print("Date Time:")
                        print("Year:", year2,)
                        print("Month:", month2)
                        print("Day:", day2)
                        print("Hour:", hour2)
                        print("Minute:", min2)
                        print("Second:", int(sec2))
                        print("Course:", course)
                        print("PDOP:", PDOP)
                        print("HDOP:", HDOP)
                        print("VDOP:", VDOP)
                        gps_raw = send_at_command("AT+CGNSINF")
                        print("GPS/GNSS Based Location String:", gps_raw.split("\r\n")[1])
                        break
                except:
                    pass
    else:
        print("=========================") 
        print(f"Set GPS Mode : {gnss_mode}")
        response = send_at_command(f"AT+CGNSSMODE={gnss_mode}",wait=3)
        print(response)
        print("Requesting current GPS/GNSS/GLONASS location")
        while True:
            response = send_at_command("AT+CGNSSINFO",wait=3)
            print(response)
            if "+CGNSSINFO: ,,,,,,,," not in response and "ERROR" not in response:
                data = response.split("+CGNSSINFO: ")[1].split("\n")[0] 
                values = data.split(",")
                if len(values) >= 1:  
                    fixMode = values[0]  # Fix mode
                    latitude = float(values[5])  # Latitude
                    longitude = float(values[7])  # Longitude
                    if values[12] is not "":
                        speed = float(values[12])  # Speed
                    else:
                        speed = 0.0
                    altitude = float(values[11])  # Altitude
                    if values[1] == "":
                        gps_satellite_num = 0
                    else:
                        gps_satellite_num = int(values[1])
                    if values[2] == "":
                        beidou_satellite_num = 0
                    else:
                        beidou_satellite_num = int(values[2])
                    if values[3] == "":
                        glonass_satellite_num = 0
                    else:
                        glonass_satellite_num = int(values[3])
                    if values[4] == "":
                        galileo_satellite_num = 0
                    else:
                        galileo_satellite_num = int(values[4])
                    course = 1.0
                    PDOP = float(values[14])
                    HDOP = float(values[15])
                    VDOP = float(values[16])
                    date_str = values[9]  # Date
                    time_str = values[10]  # Time
                    year2 = int(date_str[4:6]) + 2000  # Year
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
                    print("Latitude:", latitude)
                    print("tLongitude:", longitude)
                    print("Speed:", speed)
                    print("Altitude:", altitude)
                    print("Visible Satellites:")
                    print(" GPS Satellites:", gps_satellite_num)
                    print(" BEIDOU Satellites:", beidou_satellite_num)
                    print(" GLONASS Satellites:", glonass_satellite_num)
                    print(" GALILEO Satellites:", galileo_satellite_num)
                    print("Date Time:")
                    print("Year:", year2,)
                    print("Month:", month2)
                    print("Day:", day2)
                    print("Hour:", hour2)
                    print("Minute:", min2)
                    print("Second:", int(sec2))
                    print("Course:", course)
                    print("PDOP:", PDOP)
                    print("HDOP:", HDOP)
                    print("VDOP:", VDOP)
                    gps_raw = send_at_command("AT+CGNSSINFO")
                    print("GPS/GNSS Based Location String:", gps_raw.split("\r\n")[1])
                    break

def main():
    global modemName
    modem_setup()
    gnss_length = 0
    a76xx_gnss_mode = [1, 2, 3, 4]
    sim767x_gnss_mode = [1, 3, 5, 9, 13, 15]
    gnss_mode = None
    if modemName.startswith("A767"):  # Correct method name: startswith
        gnss_mode = a76xx_gnss_mode
        gnss_length = len(a76xx_gnss_mode)
    else:
        gnss_mode = sim767x_gnss_mode
        gnss_length = len(sim767x_gnss_mode)
    # Print the result to verify
    print("GNSS Modes:", gnss_mode)
    print("GNSS Length:", gnss_length)
    for i in range(gnss_length):
        '''
          Model: A76XX
          1 - GPS L1 + SBAS + QZSS
          2 - BDS B1
          3 - GPS + GLONASS + GALILEO + SBAS + QZSS
          4 - GPS + BDS + GALILEO + SBAS + QZSS.
         
          Model: SIM7670G
          1  -  GPS
          3  -  GPS + GLONASS
          5  -  GPS + GALILEO
          9  -  GPS + BDS
          13 -  GPS + GALILEO + BDS
          15 -  GPS + GLONASS + GALILEO + BDS
        '''
        loopGPS(gnss_mode[i])
    print("Disabling GPS")
    if utilities.CURRENT_PLATFORM == "LILYGO_T_SIM7000G":
        response = send_at_command("AT+CGNSPWR=0")
        print(response)  
    else:
        response = send_at_command("AT+CGNSSPWR=0")
        print(response)   
    # Just echo serial data
    while True:
        if SerialAT.any():
            print(SerialAT.read().decode(), end="")
        time.sleep(0.001)

if __name__ == "__main__":
    main()