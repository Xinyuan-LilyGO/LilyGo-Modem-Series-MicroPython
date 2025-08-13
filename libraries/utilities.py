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
    elif CURRENT_PLATFORM == "LILYGO_T_A7670":
        CONFIG = {
            "MODEM_BAUDRATE": 115200,
            "MODEM_DTR_PIN": 25,
            "MODEM_TX_PIN": 26,
            "MODEM_RX_PIN": 27,
            "BOARD_PWRKEY_PIN": 4,
            "BOARD_BAT_ADC_PIN": 35,
            "BOARD_POWERON_PIN": 12,
            "MODEM_RING_PIN": 33,
            "MODEM_RESET_PIN": 5,
            "BOARD_MISO_PIN": 2,
            "BOARD_MOSI_PIN": 15,
            "BOARD_SCK_PIN": 14,
            "BOARD_SD_CS_PIN": 13,
            "MODEM_RESET_LEVEL": 1,
            "MODEM_GPS_ENABLE_GPIO": 0,
            "MODEM_GPS_ENABLE_LEVEL": 0,
        }
    elif CURRENT_PLATFORM == "LILYGO_T_A7608X_S3":
        CONFIG = {
            "MODEM_BAUDRATE": 115200,
            "MODEM_DTR_PIN": 7,
            "MODEM_TX_PIN": 17,
            "MODEM_RX_PIN": 18,
            "BOARD_PWRKEY_PIN": 15,
            "BOARD_BAT_ADC_PIN": 4,
            "BOARD_POWERON_PIN": 12,
            "MODEM_RING_PIN": 6,
            "MODEM_RESET_PIN": 16,
            "BOARD_MISO_PIN": 47,
            "BOARD_MOSI_PIN": 14,
            "BOARD_SCK_PIN": 21,
            "BOARD_SD_CS_PIN": 13,
            "MODEM_RESET_LEVEL": 0,
            "BOARD_SOLAR_ADC_PIN": 3,
            "MODEM_GPS_ENABLE_GPIO": 0,
            "MODEM_GPS_ENABLE_LEVEL": 1,
        }
    elif CURRENT_PLATFORM == "LILYGO_T_SIM7000G":
        CONFIG = {
            "MODEM_BAUDRATE": 115200,
            "MODEM_DTR_PIN": 25,
            "MODEM_TX_PIN": 27,
            "MODEM_RX_PIN": 26,
            "BOARD_PWRKEY_PIN": 4,
            "BOARD_LED_PIN": 12,
            "LED_ON": 0,
            "BOARD_MISO_PIN": 2,
            "BOARD_MOSI_PIN": 15,
            "BOARD_SCK_PIN": 14,
            "BOARD_SD_CS_PIN": 13,
            "BOARD_BAT_ADC_PIN": 35,
            "BOARD_SOLAR_ADC_PIN": 36,
            "MODEM_GPS_ENABLE_GPIO": 0,
            "MODEM_GPS_ENABLE_LEVEL": 1,
            
            # //! The following pins are for SimShield and need to be used with SimShield
            # //! 以下引脚针对SimShield,需要搭配SimShield 
            "SIMSHIELD_MOSI": 23,
            "SIMSHIELD_MISO": 19,
            "SIMSHIELD_SCK": 18,
            "SIMSHIELD_SD_CS": 32,
            "SIMSHIELD_RADIO_BUSY": 39,
            "SIMSHIELD_RADIO_CS": 5,
            "SIMSHIELD_RADIO_IRQ": 34,
            "SIMSHIELD_RADIO_RST": 15,
            "SIMSHIELD_RS_RX": 13,
            "SIMSHIELD_RS_TX": 14,
            "SIMSHIELD_SDA": 21,
            "SIMSHIELD_SCL": 22,
        }
    elif CURRENT_PLATFORM == "LILYGO_T_A7670X_S3_STAN" or CURRENT_PLATFORM == "LILYGO_T_SIM7000G_S3_STAN" or CURRENT_PLATFORM == "LILYGO_T_SIM7080G_S3_STAN" or CURRENT_PLATFORM == "LILYGO_T_SIM7670G_S3_STAN":
        CONFIG = {
            "MODEM_BAUDRATE": 115200,
            "BOARD_SDA_PIN": 3,
            "BOARD_SCL_PIN": 2,

            "MODEM_DTR_PIN": 7,
            "MODEM_TX_PIN": 4,
            "MODEM_RX_PIN": 5,
            "MODEM_RING_PIN": 6,

            '''
            * GPS communication pin. If the modem has GPS function, 
            * NMEA data can be read through this IO. 
            * If an external GPS module is used, the same GPIO is used for communication.
            '''
           "MODEM_GPS_RX_PIN": 48,
           "MODEM_GPS_TX_PIN": 45,
           "MODEM_GPS_PPS_PIN": 17,

            # This IO is only used when using an external GPS module, such as A7670G+L76K GPS
           "GPS_SHIELD_WAKEUP_PIN": 0,

            # The modem boot pin needs to follow the startup sequence.
            "BOARD_PWRKEY_PIN": 46,
            
            # Analog pins are already connected to the ADC voltage divider circuit and cannot be used for other purposes
            "BOARD_BAT_ADC_PIN": 8,
            "BOARD_SOLAR_ADC_PIN": 18,

            # SD Socket pins
            "BOARD_MISO_PIN": 13,
            "BOARD_MOSI_PIN": 11,
            "BOARD_SCK_PIN": 12,
            "BOARD_SD_CS_PIN": 10,

            # Enable / disable power save mode (1 disabled, 0 enabled)
            "BOARD_POWER_SAVE_MODE_PIN": 42,

            # CAMERA_XXX_PIN is routed to the pin header and camera connector
            "CAMERA_PWDN_PIN": -1,
            "CAMERA_RESET_PIN": -1,
            "CAMERA_XCLK_PIN": 21,
            "CAMERA_SIOD_PIN": 1,
            "CAMERA_SIOC_PIN": 41,
            "CAMERA_VSYNC_PIN": 9,
            "CAMERA_HREF_PIN": 14,
            "CAMERA_PCLK_PIN": 37,
            "CAMERA_Y9_PIN": 40,
            "CAMERA_Y8_PIN": 39,
            "CAMERA_Y7_PIN": 38,
            "CAMERA_Y6_PIN": 36,
            "CAMERA_Y5_PIN": 16,
            "CAMERA_Y4_PIN": 47,
            "CAMERA_Y3_PIN": 15,
            "CAMERA_Y2_PIN": 35,
            
        }
    else:
        raise ValueError("Unsupported platform")

    for key, value in CONFIG.items():
        globals()[key] = value

# set_platform("LILYGO_T_SIM7670G")
# set_platform("LILYGO_T_A7670")
# set_platform("LILYGO_T_A7608X_S3")
# set_platform("LILYGO_T_SIM7000G")
# set_platform("LILYGO_T_A7670X_S3_STAN")
# set_platform("LILYGO_T_SIM7000G_S3_STAN")
# set_platform("LILYGO_T_SIM7080G_S3_STAN")
set_platform("LILYGO_T_SIM7670G_S3_STAN")