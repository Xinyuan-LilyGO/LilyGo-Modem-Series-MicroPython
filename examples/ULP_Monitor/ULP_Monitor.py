'''
 * @file      ULP_Monitor.py
 * @license   MIT
 * @copyright Copyright (c) 2025  ShenZhen XinYuan Electronic Technology Co., Ltd
 * @date      2025-07-15
'''
from machine import ADC, Pin
import machine
import time
import utilities

# Setup ADC
adc = ADC(Pin(utilities.BOARD_BAT_ADC_PIN))
adc.atten(ADC.ATTN_11DB)  # Configure attenuation to 11dB
adc.width(ADC.WIDTH_12BIT)  # Set ADC width to 12 bits
# Constants
RTC_SLOW_MEM = [0] * 11  # Simulated RTC memory
ADC_THRESHOLD = 1900  # Threshold for the ADC

def ulp_program():
    # Simulating the ULP program functionality
    RTC_SLOW_MEM[1] = 0  # Sample count
    for _ in range(200):  # Simulate the loop delay
        time.sleep(0.005)  # Approximately simulate the delay of 5 ms
        RTC_SLOW_MEM[1] += 1  # Increment sample count
        RTC_SLOW_MEM[2] = adc.read()  # Read ADC value
        # Compare to threshold, if met, we exit loop early
        if RTC_SLOW_MEM[2] >= ADC_THRESHOLD:
            break

def main():
    print("Wakeup was not caused by deep sleep: 0")
    # Run the ULP program simulation
    ulp_program()
    adc_result = RTC_SLOW_MEM[2]  # Get the ADC result
    print("Wakeup caused by ULP program")
    print(f"adc result = {adc_result}")
    print("===========================")
    for i in range(11):
        print(f"[{i:02d}] {RTC_SLOW_MEM[i]:4d}")  # Print RTC slow memory in required format
    print(f"ULP program occupied {len(RTC_SLOW_MEM)} 32-bit words of RTC_SLOW_MEM, make sure you put your variables after this.")
    print("===========================")
    for _ in range(6):  # Simulate collecting battery voltage readings
        battery_voltage = adc.read() * 2  # Simulating battery voltage (you may need to adjust this)
        print(f"Battery:{battery_voltage}mV")
        time.sleep(1)
    print("Sleeping...")
    # Simulate deep sleep
    machine.deepsleep(10000)  # Sleep for 10 seconds as an example

if __name__ == "__main__":
    main()