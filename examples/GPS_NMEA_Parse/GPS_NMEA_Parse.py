'''
 * @file      GPS_NMEA_Parse.py
 * @license   MIT
 * @copyright Copyright (c) 2025  Shenzhen Xin Yuan Electronic Technology Co., Ltd
 * @date      2025-07-22
 * @note      GPS only supports A7670X/A7608X (excluding A7670G and other versions that do not support positioning).
'''
import machine
import time
from machine import UART, Pin
from math import radians, sin, cos, sqrt, atan2, degrees
import utilities

# Initialize UART for modem communication
SerialAT = UART(1, baudrate=utilities.MODEM_BAUDRATE, tx=utilities.MODEM_TX_PIN, rx=utilities.MODEM_RX_PIN)

# Initialize pins
pwrkey = Pin(utilities.BOARD_PWRKEY_PIN, Pin.OUT)
poweron = Pin(utilities.BOARD_POWERON_PIN, Pin.OUT)
reset_pin = Pin(utilities.MODEM_RESET_PIN, Pin.OUT)
gps_enable = Pin(utilities.MODEM_GPS_ENABLE_GPIO, Pin.OUT)

sentences_with_fix = 0
failed_checksum = 0
last_sec2 = None

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
    
    response = send_at_command("AT+CGNSSMODE=3")
    print(response)
    
    response = send_at_command("AT+CGNSSNMEA=1,1,1,1,1,1,0,0")
    print(response)
    
    response = send_at_command("AT+CGPSNMEARATE=1")
    print(response)
    
    response = send_at_command("AT+CGNSSTST=1")
    print(response)
    
#     response = send_at_command("AT+CGNSSPORTSWITCH=0,1")
#     print(response)
    
    print("Sats HDOP  Latitude   Longitude   Fix  Date       Time     Date Alt    Course Speed Card  Distance Course Card  Chars Sentences Checksum")
    print("           (deg)      (deg)       Age                      Age  (m)    --- from GPS ----  ---- to London  ----  RX    RX        Fail")
    print("----------------------------------------------------------------------------------------------------------------------------------------")
    

def printInt(val, valid, length):
    if not valid:
        sz = '*' * length
    else:
        sz = str(val)
    
    # Handle string length
    if len(sz) > length:
        sz = sz[:length]
    elif len(sz) < length:
        sz = sz + ' ' * (length - len(sz))
    
    # Replace last character with space if length > 0
    if length > 0 and len(sz) > 0:
        sz = sz[:-1] + ' '
    
    print(sz, end='')
    smart_delay(0)

def printFloat(val, valid, length, prec):
    if not valid:
        print('*' * (length - 1) + ' ', end='')
    else:
        # Manual float formatting
        s = "{0:.{1}f}".format(val, prec)
        print(s, end='')
        
        # Calculate padding needed
        padding = length - len(s)
        if padding > 0:
            print(' ' * padding, end='')
    
    smart_delay(0)

def printDateTime(month, day, year, hour, minute, second, date_valid=True, time_valid=True):
    global age
    if not date_valid:
        print("********** ", end='')
    else:
        # Format: MM/DD/YY
        print("{:02d}/{:02d}/{:04d} ".format(
            int(month) if isinstance(month, float) else month,
            int(day) if isinstance(day, float) else day,
            int(year) % 100 if isinstance(year, float) else year), 
            end='')
    
    if not time_valid:
        print("******** ", end='')
    else:
        print("{:02d}:{:02d}:{:02d} ".format(
            int(hour) if isinstance(hour, float) else hour,
            int(minute) if isinstance(minute, float) else minute,
            int(second) if isinstance(second, float) else second), 
            end='')

    printInt(age, date_valid and time_valid, 5) 
    smart_delay(0)
 
def printStr(s, length):
    slen = len(s)
    for i in range(length):
        print(s[i] if i < slen else ' ', end='')
    smart_delay(0)

def degrees_to_cardinal(degrees):
    """
    Convert compass degrees to 16-point cardinal direction abbreviation
    
    Args:
        degrees (float): Compass bearing in degrees (0-360)
        
    Returns:
        str: 3-letter cardinal direction abbreviation (e.g. 'NNE', 'SSW')
    """
    # Normalize degrees to 0-360 range (handles negative values and over-rotations)
    degrees = (degrees + 360) % 360  
    # 16-point compass directions with angle ranges and abbreviations
    # Each tuple contains (start_angle, end_angle, direction_abbreviation)
    directions = [
        (0, 11.25, 'N'),      # North
        (11.25, 33.75, 'NNE'), # North-Northeast
        (33.75, 56.25, 'NE'),  # Northeast
        (56.25, 78.75, 'ENE'), # East-Northeast
        (78.75, 101.25, 'E'),  # East
        (101.25, 123.75, 'ESE'), # East-Southeast
        (123.75, 146.25, 'SE'), # Southeast
        (146.25, 168.75, 'SSE'), # South-Southeast
        (168.75, 191.25, 'S'),  # South
        (191.25, 213.75, 'SSW'), # South-Southwest
        (213.75, 236.25, 'SW'), # Southwest
        (236.25, 258.75, 'WSW'), # West-Southwest
        (258.75, 281.25, 'W'),  # West
        (281.25, 303.75, 'WNW'), # West-Northwest
        (303.75, 326.25, 'NW'), # Northwest
        (326.25, 348.75, 'NNW'), # North-Northwest
        (348.75, 360, 'N')      # North
    ]
    # Find which direction range the degrees fall into
    for start, end, cardinal in directions:
        if start <= degrees < end:
            return cardinal   
    return '***'  # Default return if no match (should theoretically never happen)

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great-circle distance between two points 
    on the Earth (specified in decimal degrees)
    
    Args:
        lat1, lon1: Latitude and Longitude of point 1 (in degrees)
        lat2, lon2: Latitude and Longitude of point 2 (in degrees)
        
    Returns:
        Distance between the points in meters
    """
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    radius = 6371000  # Earth radius in meters
    return radius * c

def calculate_course(lat1, lon1, lat2, lon2):
    """
    Calculate initial bearing (course) from point 1 to point 2
    Args:
        lat1, lon1: Starting point coordinates (in degrees)
        lat2, lon2: Destination point coordinates (in degrees)
        
    Returns:
        Bearing in degrees from North (0-360)
    """
    # Convert degrees to radians
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)
    dlon = lon2 - lon1
    # Calculate bearing
    y = sin(dlon) * cos(lat2)
    x = cos(lat1) * sin(lat2) - sin(lat1) * cos(lat2) * cos(dlon)
    bearing = atan2(y, x)
    # Convert from radians to degrees and normalize
    bearing = degrees(bearing)
    bearing = (bearing + 360) % 360
    return bearing

def parse_loop():
    global sentences_with_fix, last_sec2, age
    while True:
        response = send_at_command("AT+CGNSSPWR?")
#         print(response)
        response = send_at_command("AT+CGNSSINFO")
#         print("GPS/GNSS Based Location String:", response.split("\r\n")[1])
        if "+CGNSSINFO: ,,,,,,,," not in response and "ERROR" not in response:
            data = response.split("+CGNSSINFO: ")[1].split("\n")[0]
            values = data.split(",")
            
            chars_processed += len(data)  # Count characters processed
            sentences_with_fix += 20  # Increase the count of sentences with fixes                
            
            if values[17] is not "":
                satellites_value = int(values[17])
            else:
                satellites_value = 0
            hdop = float(values[15])
            lat = float(values[5])  # Latitude
            lng = float(values[7])  # Longitude
            
            date_str = values[9]  # Date
            time_str = values[10]  # Time
            year2 = int(date_str[:2]) + 2003  # Year
            month2 = int(date_str[2:4])  # Month
            day2 = int(date_str[4:6])-3  # Day
            hour2 = int(time_str[:2])  # Hour
            min2 = int(time_str[2:4])  # Minute
            sec2 = float(time_str[4:])  # Second
            if last_sec2 is not None:
                age = sec2 - last_sec2
                if age < 0:
                    age += 60 
                age = int(age*1000)
            last_sec2 = sec2
            
            # Convert UTC time to local time by adding time zone offset
            timezone_offset = 8  # CST is UTC+8
            # Adjust hours based on timezone offset
            hour2 += timezone_offset
            if hour2 >= 24:
                hour2 -= 24
            elif hour2 < 0:
                hour2 += 24
            
            if values[11] is not "":
                meters = float(values[11])
            if values[12] is not "":
                kmph = float(values[12])
            if values[13] is not "":
                deg = float(values[13])
            
            
        else:
            satellites_value = 0
            hdop = 0
            lat = 0
            lng = 0
            year2 = 0
            month2 = 0
            day2 = 0
            hour2 = 0
            min2 = 0
            sec2 = 0
            meters = 0
            deg = 0
            kmph = 0
            age = 0
            chars_processed =0
            sentences_with_fix += 2
            failed_checksum = 0
            time.sleep(10)
            
        LONDON_LAT = 51.508131
        LONDON_LON = -0.128002
        
        printInt(satellites_value, 1, 5)
        printFloat(hdop, 1, 6, 1)
        printFloat(lat, 1, 11, 6)
        printFloat(lng, 1, 12, 6)
        printInt(age, 1, 5)
        printDateTime(month2, day2, year2, hour2, min2, int(sec2))
        printFloat(meters, 1, 7, 2)
        printFloat(deg, 1, 7, 2)
        printFloat(kmph, 1, 6, 2)
        direction = degrees_to_cardinal(deg)
        printStr(direction, 6)
        distance_meters = haversine_distance(
            lat,
            lng,
            LONDON_LAT,
            LONDON_LON)
        distance_km = distance_meters / 1000
        printInt(int(distance_km), 1, 9)
        course_to_london = calculate_course(lat, lng, LONDON_LAT, LONDON_LON)
        printFloat(course_to_london, 1, 7, 2)
        cardinal_dir = degrees_to_cardinal(course_to_london)
        printStr(cardinal_dir, 6)
        printInt(chars_processed, 1, 6)  # Display chars processed
        printInt(sentences_with_fix, 1, 10)  # Display sentences with fix
        printInt(failed_checksum, 1, 9)  # Display failed checksums
        print()  # New line after each reading


def smart_delay(ms):
    start = time.ticks_ms()
    while time.ticks_diff(time.ticks_ms(), start) < ms:
        if SerialAT.any():
            data = SerialAT.read()
            # Process incoming data if needed
            pass


def main():
    global modemName
    modem_setup()
    parse_loop()
    # Just echo serial data
    while True:
        if SerialAT.any():
            print(SerialAT.read().decode(), end="")
        time.sleep(0.001)

if __name__ == "__main__":
    main()