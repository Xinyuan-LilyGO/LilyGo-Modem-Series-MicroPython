from machine import Pin, UART
import time

# Constants for pin definitions
BOARD_MODEM_DTR_PIN = 25
BOARD_MODEM_TX_PIN = 26
BOARD_MODEM_RX_PIN = 27
BOARD_MODEM_PWR_PIN = 4
BOARD_ADC_PIN = 35
BOARD_POWER_ON_PIN = 12
BOARD_MODEM_RI_PIN = 33
BOARD_RST_PIN = 5
BOARD_SDCARD_MISO = 2
BOARD_SDCARD_MOSI = 15
BOARD_SDCARD_SCLK = 14
BOARD_SDCARD_CS = 13

BOARD_GPS_TX_PIN = 21
BOARD_GPS_RX_PIN = 22
BOARD_GPS_PPS_PIN = 23
BOARD_GPS_WAKEUP_PIN = 19

# Setup UART for GPS and modem communication
SerialAT = UART(1, baudrate=115200, tx=BOARD_MODEM_TX_PIN, rx=BOARD_MODEM_RX_PIN)
SerialGPS = UART(2, baudrate=9600, tx=BOARD_GPS_TX_PIN, rx=BOARD_GPS_RX_PIN)

# GPS parsing class
class TinyGPSPlus:
    def __init__(self):
        self.lat = None
        self.lng = None
        self.date = None
        self.time = None

    def encode(self, sentence):
        # Simulate parsing for GGA sentences (actual data parsing)
        if b'$GPGGA' in sentence:
            parts = sentence.split(b',')
            if len(parts) >= 6 and parts[2] and parts[4]:  # Latitude and Longitude fields
                self.lat = self._parse_lat_lon(parts[2], parts[3])
                self.lng = self._parse_lat_lon(parts[4], parts[5])
                self.date = time.localtime().tm_year, time.localtime().tm_mon, time.localtime().tm_mday
                self.time = time.localtime().tm_hour, time.localtime().tm_min, time.localtime().tm_sec
                return True
        return False

    def _parse_lat_lon(self, value, direction):
        # Convert latitude or longitude string to float
        degrees = float(value[:-2]) / 100
        if direction in (b'S', b'W'):
            degrees = -degrees
        return degrees

    def location_is_valid(self):
        return self.lat is not None and self.lng is not None

    def location(self):
        return self.lat, self.lng

    def get_date(self):
        return self.date

    def get_time(self):
        return self.time

# Create GPS instance
gps = TinyGPSPlus()

def setup():
    # Power on the module
    pin_power_on = Pin(BOARD_POWER_ON_PIN, Pin.OUT)
    pin_power_on.value(1)  # HIGH
    time.sleep(1)

    # Reset the modem
    pin_rst = Pin(BOARD_RST_PIN, Pin.OUT)
    pin_rst.value(0)  # LOW
    time.sleep(1)
    pin_rst.value(1)  # HIGH

    # Display initial messages for board and GPS
    print("This sketch is only suitable for boards without GPS function inside the modem, such as A7670G")
    print("Works only with externally mounted GPS modules.")
    print("If the purchased board includes a GPS extension module it will work, otherwise this sketch will have no effect")
    print("If the purchased modem supports GPS functionality, please use examples/TinyGSM_Net_GNSS")

    time.sleep(2)

def loop():
    while SerialGPS.any():
        c = SerialGPS.read()
        if c:
            if gps.encode(c):
                displayInfo()

    if gps.lat is None or gps.lng is None:
        print("No GPS detected: check wiring.")
        time.sleep(1)

    if SerialAT.any():
        print(SerialAT.read().decode('utf-8'), end='')

    if time.ticks_ms() > 30000 and gps.lat is None:
        print("No GPS detected: check wiring.")
        time.sleep(1)

    time.sleep(0.01)

def displayInfo():
    # Print GPS location information
    print("Location: ", end='')
    if gps.location_is_valid():
        lat, lng = gps.location()
        print(f"{lat:.6f},{lng:.6f}", end=' ')
    else:
        print("INVALID", end=' ')

    # Print GPS date and time information
    print("Date/Time: ", end='')
    if gps.get_date() and gps.get_time():
        print(f"{gps.get_date()[1]}/{gps.get_date()[2]}/{gps.get_date()[0]} {gps.get_time()[0]:02}:{gps.get_time()[1]:02}:{gps.get_time()[2]:02}")
    else:
        print("INVALID")

# Main program
setup()
while True:
    loop()