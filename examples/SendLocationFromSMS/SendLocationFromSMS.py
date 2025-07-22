'''
 * @file      SendLocationFromSMS.py
 * @license   MIT
 * @copyright Copyright (c) 2025  Shenzhen Xin Yuan Electronic Technology Co., Ltd
 * @date      2025-07-22
 * @note      SIM7670G does not support SMS and voice functions
'''
import time
import machine
import utilities

# Initialize the serial interface for the modem
uart = machine.UART(1, baudrate=utilities.MODEM_BAUDRATE, tx=utilities.MODEM_TX_PIN, rx=utilities.MODEM_RX_PIN)
# It depends on the operator whether to set up an APN. If some operators do not set up an APN,
# they will be rejected when registering for the network. You need to ask the local operator for the specific APN.
# APNs from other operators are welcome to submit PRs for filling.
APN = ""  # Replace with your APN (CHN-CT: China Telecom)
SMS_TARGET = "+380xxxxxxxxx"  #Change the SMS_TARGET you want to dial

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
    machine.Pin(utilities.BOARD_PWRKEY_PIN, machine.Pin.OUT).value(0)
    time.sleep(0.1)
    machine.Pin(utilities.BOARD_PWRKEY_PIN, machine.Pin.OUT).value(1)
    time.sleep(1)
    machine.Pin(utilities.BOARD_PWRKEY_PIN, machine.Pin.OUT).value(0)

def modem_reset():
    machine.Pin(utilities.MODEM_RESET_PIN, machine.Pin.OUT).value(not utilities.MODEM_RESET_LEVEL)
    time.sleep(0.1)
    machine.Pin(utilities.MODEM_RESET_PIN, machine.Pin.OUT).value(utilities.MODEM_RESET_LEVEL)
    time.sleep(2.6)
    machine.Pin(utilities.MODEM_RESET_PIN, machine.Pin.OUT).value(not utilities.MODEM_RESET_LEVEL)

def check_modem():
    print("Starting modem...")
    while True:
        response = send_at_command("AT")
        if "OK" in response:
            print()  # Print a newline for clarity
            break
        else:
            print(".", end="")

def connect_network(apn):
    send_at_command(f"AT+CGDCONT=1,\"IP\",\"{apn}\"")
    response = send_at_command("AT+CEREG?",wait=3)  # Attach to the GPRS
    print(response)
    if "OK" in response:
        print("Online registration successful")
    else:
        print("Network registration was rejected, please check if the APN is correct")

def loopGPS():
    global lon2,lat2,year2,month2,day2,hour2,min2,sec2
    print("Requesting current GPS/GNSS/GLONASS location")
    response = send_at_command("AT+CGNSSINFO")
    print(response)
    if "+CGNSSINFO: ,,,,,,,," not in response and "ERROR" not in response:
        data = response.split("+CGNSSINFO: ")[1].split("\n")[0] 
        values = data.split(",")
        if len(values) >= 1:  
            fixMode = values[0]  # Fix mode
            lat2 = float(values[5])  # Latitude
            lon2 = float(values[7])  # Longitude
            speed2 = float(values[12])  # Speed
            alt2 = float(values[11])  # Altitude
            vsat2 = int(values[1])  # Visible satellites
            usat2 = 0  # GPS_BuiltIn cannot get the number of used satellites
            accuracy2 = float(values[16])  # Accuracy
            date_str = values[9]  # Date
            time_str = values[10]  # Time
            year2 = int(date_str[:2]) + 2003  # Year
            month2 = int(date_str[2:4])  # Month
            day2 = int(date_str[4:6])-3  # Day
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
            return True
    return False

def deepsleep(ms):
    # Enable deep sleep mode
    machine.deepsleep(ms)

def lightsleep(ms):
    # Enable timer wakeup
    machine.sleep(ms)

def main():
    global lon2,lat2,year2,month2,day2,hour2,min2,sec2
    # Turn on DC boost to power on the modem
    machine.Pin(utilities.BOARD_POWERON_PIN, machine.Pin.OUT).value(1)
    # Set modem reset pin ,reset modem
    modem_reset()
    # Turn on modem
    modem_power_on()
    # Set ring pin input
    machine.Pin(utilities.MODEM_RING_PIN, machine.Pin.IN, machine.Pin.PULL_UP)
    check_modem()
    print("Enabling GPS/GNSS/GLONASS")
    response = send_at_command("AT+CGNSSPWR=1",wait=5)
    print(response)
    print("GPS Enabled")
    response = send_at_command("AT+CGNSSIPR=115200",wait=2)
    print(response)
    print("Wait for the modem to register with the network.")
    connect_network(APN)
    time.sleep(1)
    while True:
        if loopGPS():
            print(f"The location was obtained successfully and sent to the {SMS_TARGET} number.")
            msg_str = f"Longitude: {lon2:.6f}\n"
            msg_str += f"Latitude: {lat2:.6f}\n"
            msg_str += f"UTC Date: {year2}/{month2}/{day2}\n"
            msg_str += f"UTC Time: {hour2}:{min2}:{int(sec2)}\n"
            print("MESSAGE:", msg_str)
            response = send_at_command("AT+CMGF=1")
            print(response)
            response = send_at_command("AT+CSCS=\"GSM\"")
            print(response)
            response = send_at_command(f"AT+CMGS=\"{SMS_TARGET}\"")
            print(response)
            uart.write(msg_str.encode('utf-8'))
            time.sleep(1)  
            uart.write(bytearray([0x1A]))
            time.sleep(1)
            if '>' in response:
                print("Send sms message OK")
            else:
                print("Send sms message fail")
            time.sleep(3)
            # Deep sleep, wake up every 60 seconds for positioning
            deepsleep(60 * 1000) # 60 Second    
            
if __name__ == "__main__":
    main()