'''
 * @file      SerialRS485.py
 * @license   MIT
 * @copyright Copyright (c) 2025  Shenzhen Xin Yuan Electronic Technology Co., Ltd
 * @date      2025-07-01
 * @note      Simple demonstration of how to use Serial2
'''
import time
from machine import UART, Pin
import utilities

# You can freely choose unused GPIO as RS485 TX, RX
RS485_RX_PIN = 15
RS485_TX_PIN = 16
# GPIO above ESP32 GPIO33 can only be used as input, ESP32S3 has no restrictions
# RS485_RX_PIN = 34
# RS485_TX_PIN = 32

def setup():
    global SerialAT, SerialRS485
    SerialAT = UART(1, baudrate=115200, tx=Pin(utilities.MODEM_TX_PIN), rx=Pin(utilities.MODEM_RX_PIN))
    SerialRS485 = UART(2, baudrate=9600, tx=Pin(RS485_TX_PIN), rx=Pin(RS485_RX_PIN))
    
def loop():
    global SerialAT, SerialRS485
    while True:
        if SerialRS485.any():
            SerialAT.write(SerialRS485.read())
        if SerialAT.any():
            SerialRS485.write(SerialAT.read())

if __name__ == "__main__":
    setup()
    loop()
