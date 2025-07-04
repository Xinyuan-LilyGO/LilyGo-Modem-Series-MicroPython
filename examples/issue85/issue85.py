from machine import Pin, reset, deepsleep
import time
import machine

uS_TO_S_FACTOR = 1000000  # Conversion factor for microseconds to seconds
TIME_TO_SLEEP = 30        # Time ESP32 will go to sleep (in seconds)

PWRKEY_PIN = 4
MODEM_RESET_PIN = 5
POW_PIN = 12
MODEM_DTR_PIN = 25
MODEM_TX_PIN = 26
MODEM_RX_PIN = 27
MODEM_RING_PIN = 33
VBAT_PIN = 35
MODEM_RESET_LEVEL = 1

SER_BAUD = 115200

# Reset causes
NO_MEAN = 0
SW_RST = 1
DEEPSLEEP_RST = 2
RTCWDT_RST = 3

# Setup
def setup():
    # Serial Setup
    print("Serial Started")

    # Check the reset cause
    reset_cause = machine.reset_cause()
    if reset_cause == DEEPSLEEP_RST:
        print("Woken up from deep sleep")
        countdown_and_start_modem()
    else:
        print("Not woken from deep sleep, starting modem right away")
        countdown_and_start_modem()

    # Release reset GPIO hold
    reset_pin = Pin(MODEM_RESET_PIN, Pin.OUT)
    reset_pin.value(MODEM_RESET_LEVEL)
    
    # Reset modem
    reset_modem()

    # Power on modem
    power_on_modem()

    # Wait for modem to power up
    time.sleep(20)

    # Power off modem
    power_off_modem()

    # Hold reset low during deep sleep
    reset_pin.value(0)
    reset_pin.init(Pin.IN)
    
    print("Enter esp32 goto deep sleep!")
    deepsleep(TIME_TO_SLEEP * uS_TO_S_FACTOR)

def countdown_and_start_modem():
    for i in range(30, 0, -1):
        print(f"Modem will start in {i} seconds")
        time.sleep(1)
    print("TurnON Modem!")

# Modem Reset Logic
def reset_modem():
    print("Resetting Modem")
    reset_pin = Pin(MODEM_RESET_PIN, Pin.OUT)
    reset_pin.value(0)
    time.sleep(0.1)
    reset_pin.value(MODEM_RESET_LEVEL)
    time.sleep(2.6)
    reset_pin.value(0)

# Modem Power On Logic
def power_on_modem():
    print("Power on the modem")
    pwr_key_pin = Pin(PWRKEY_PIN, Pin.OUT)
    pwr_key_pin.value(0)
    time.sleep(0.1)
    pwr_key_pin.value(1)
    time.sleep(0.3)
    pwr_key_pin.value(0)

# Modem Power Off Logic
def power_off_modem():
    print("Power off the modem")
    pwr_key_pin = Pin(PWRKEY_PIN, Pin.OUT)
    pwr_key_pin.value(1)
    time.sleep(2)
    pwr_key_pin.value(0)
    time.sleep(5)

# Main loop (not needed for sleep)
def loop():
    pass

# Execute setup
setup()
