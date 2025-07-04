#  * @file      utilities.py
#  * @license   MIT
#  * @copyright Copyright (c) 2025  Shenzhen Xin Yuan Electronic Technology Co., Ltd
#  * @date      2025-06-10
import machine

CURRENT_PLATFORM = None
CONFIG = {}

def set_platform(platform_name):
    global CURRENT_PLATFORM
    CURRENT_PLATFORM = platform_name
    configure_platform()

def configure_platform():
    global CONFIG
    if CURRENT_PLATFORM == "LILYGO_T_SIM7670G":
        CONFIG = {
            "MODEM_BAUDRATE": 115200,
            "MODEM_DTR_PIN": 9,
            "MODEM_TX_PIN": 11,
            "MODEM_RX_PIN": 10,
            "BOARD_PWRKEY_PIN": 18,
            "BOARD_LED_PIN": 12,
            "BOARD_POWERON_PIN": 12,
            "MODEM_RING_PIN": 3,
            "MODEM_RESET_PIN": 17,
            "MODEM_RESET_LEVEL": 0,
            "BOARD_BAT_ADC_PIN": 4,
            "BOARD_SOLAR_ADC_PIN": 5,
            "BOARD_MISO_PIN": 47,
            "BOARD_MOSI_PIN": 14,
            "BOARD_SCK_PIN": 21,
            "BOARD_SD_CS_PIN": 13,
            "MODEM_GPS_ENABLE_GPIO": 4,
            "MODEM_GPS_ENABLE_LEVEL": 1,
        }
    else:
        raise ValueError("Unsupported platform")

    for key, value in CONFIG.items():
        globals()[key] = value

set_platform("LILYGO_T_SIM7670G")