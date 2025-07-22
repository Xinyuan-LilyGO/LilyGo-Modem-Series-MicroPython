'''
 * @file      PowerMonitoring.py
 * @license   MIT
 * @copyright Copyright (c) 2025  Shenzhen Xin Yuan Electronic Technology Co., Ltd
 * @date      2025-07-10
 * @note      Reading the battery voltage information is only applicable to the V1.2 version.
 *            T-A7670x :  The V1.1 version does not have a battery voltage divider.
 *                         If V1.1 needs to be read, then you need to add a 100K 1% voltage divider resistor between the battery and GND
 *                         When connected to the USB, the battery voltage data read is not the real battery voltage, so the battery
 *                         voltage is sent to the UDP Server through UDP. When using it, please disconnect the USB-C
 *            T-A7670x :  Only version V1.4 has the resistor divider connected to the solar input, other versions IO38 is not connected
 * @note      Only support T-A7670 ,T-A7608X, T-SIM7672G board , not support T-Call A7670 , T-PCIE-A7670
'''
import time
import machine
import utilities
from machine import ADC, sleep, deepsleep

LOW_VOLTAGE_LEVEL = 3600  
WARN_VOLTAGE_LEVEL = 3700  
SLEEP_MINUTE = 60

# Initialize the serial interface for the modem
uart = machine.UART(1, baudrate=utilities.MODEM_BAUDRATE, tx=utilities.MODEM_TX_PIN, rx=utilities.MODEM_RX_PIN)
adc = ADC(machine.Pin(utilities.BOARD_BAT_ADC_PIN))
APN = ""  # Replace with your APN (CHN-CT: China Telecom)

def get_battery_voltage():
    readings = []
    for _ in range(30):
        val = adc.read()  # raw ADC value (0-4095)
        voltage = (val / 4095) * 3300  # convert ADC value to mV
        readings.append(voltage)
        time.sleep(0.03)  # 30ms delay
    readings.sort()
    readings = readings[1:-1]  # remove the min and max values
    average_voltage = sum(readings) / len(readings)
    return average_voltage * 2  # Return the average in mV

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
    send_at_command(f"AT+CGDCONT=1,\"IP\",\"{apn}\"")
    send_at_command("AT+CGATT=1")  # Attach to the GPRS
    while True:
        response = send_at_command("AT+NETOPEN",wait=3)
        if "OK" in response or "+NETOPEN: 0" in response:
            print("Online registration successful")
            break
        else:
            print("Network registration was rejected, please check if the APN is correct")

def main():
    machine.Pin(utilities.BOARD_POWERON_PIN, machine.Pin.OUT).value(1)
    battery_voltage_mv = get_battery_voltage()
    if battery_voltage_mv < LOW_VOLTAGE_LEVEL:
        deepsleep(SLEEP_MINUTE * 60 * 1000)
    print(f"Battery voltage is {battery_voltage_mv:.0f} mv")
    modem_reset()
    modem_power_on()
    machine.Pin(utilities.MODEM_RING_PIN, machine.Pin.IN, machine.Pin.PULL_UP)
    check_modem()
    check_sim()
    print("Wait for the modem to register with the network.")
    send_at_command("AT+CREG?")
    send_at_command("AT+SIMCOMATI")
    connect_network(APN)
    voltage_interval = 0
    while True:
        # Check voltage every 30 seconds
        if time.ticks_ms() > voltage_interval:
            voltage_interval = time.ticks_ms()+3000
            battery_voltage_mv = get_battery_voltage()
            if battery_voltage_mv < LOW_VOLTAGE_LEVEL:
                print(f"Battery voltage is too low ,{battery_voltage_mv:.0f} mv, entering sleep mode")
                response = send_at_command("AT+CPOF")
                print(response)
                deepsleep(SLEEP_MINUTE * 60 * 1000)
            elif battery_voltage_mv < WARN_VOLTAGE_LEVEL:
                print("Battery voltage reaches the warning voltage")
        sleep(1000)

if __name__ == "__main__":
    main()