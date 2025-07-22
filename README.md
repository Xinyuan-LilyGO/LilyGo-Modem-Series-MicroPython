<div align="center" markdown="1">
  <img src="./images/LilyGo_logo.png" alt="LilyGo logo" width="100"/>
</div>

<h1 align = "center">🌟LilyGo-Modem-Series(MicroPython)🌟</h1>

[![PlatformIO CI](https://github.com/Xinyuan-LilyGO/LilyGO-T-A76XX/actions/workflows/platformio.yml/badge.svg)](https://github.com/Xinyuan-LilyGO/LilyGO-T-A76XX/actions/workflows/platformio.yml)

# News

- A7670G/A7670E/A7670SA/A7672G are collectively referred to as A7670X
- A7608SA-H/A7608E-H,A7608E,A7608SA are collectively referred to as A7608X
- **SIM7670G** uses the **Qualcomm** platform, **A7670x** uses the **Asrmicro** platform.
- The usage methods of A7670/A7670 R2 are exactly the same, but the internal chip manufacturing process of the module is different.
- **A7670E-LNXY-UBL** this version does not support voice and SMS functions.

# 1️⃣Product

| Product(PinMap)    | SOC              | Flash    | PSRAM     |
| ------------------ | ---------------- | -------- | --------- |
| [T-A7670X][1]      | ESP32-WROVER-E   | 4MB      | 8MB(QSPI) |
| [T-Call-A7670X][2] | ESP32-WROVER-E   | 4MB      | 8MB(QSPI) |
| [T-A7608][4]       | ESP32-WROVER-E   | 4MB      | 8MB(QSPI) |
| [T-A7608-S3][6]    | ESP32-S3-WROOM-1 | 16MB     | 8MB(OPI)  |
| [T-SIM7670G-S3][7] | ESP32-S3-WROOM-1 | 16MB     | 8MB(OPI)  |
| [T-PCIE-A7670][8]  | ESP32-WROVER-E   | 16MB/4MB | 8MB(QSPI) |
| [T-ETH-ELite][9]   | ESP32-S3-WROOM-1 | 16MB     | 8MB(OPI)  |

- For applications that do not require voice and SMS, it is recommended to use [T-SIM7670G-S3][7]

[1]: https://www.lilygo.cc/products/t-sim-a7670e
[2]: https://www.lilygo.cc/products/t-call-v1-4
[3]: https://lilygo.cc/products/t-a7608e-h?variant=42860532433077
[4]: https://www.lilygo.cc/products/t-a7608e-h
[5]: https://lilygo.cc/products/t-a7608e-h
[6]: https://lilygo.cc/products/t-a7608e-h?variant=43932699033781
[7]: https://www.lilygo.cc/products/t-sim-7670g-s3
[8]: https://lilygo.cc/products/a-t-pcie?variant=42335922094261
[9]: https://lilygo.cc/products/t-eth-elite-1?variant=44498205049013

## 2️⃣Examples

| Example                         | [T-A7670X][1]    | [T-Call-A7670X][2] | [T-SIM767XG-S3][6] | [T-A7608][3]    | [T-PCIE-A767X][8] | [T-A7608-S3][5] |
| ------------------------------- | ---------------- | ------------------ | ------------------ | --------------- | ----------------- | --------------- |
| ATdebug                         | ✅                |                    | ✅                  |                 |                   | ✅               |
| Blynk_Console                   | ✅                |                    | ✅                  |                 |                   | ✅               |
| GPSShield                       | ✅(Only T-A7670G) | ❌   (Can't run)    | ❌   (Can't run)    | ❌   (Can't run) | ❌   (Can't run)   | ❌   (Can't run) |
| GPS_BuiltIn                     | ✅(Except A7670G) | (Except A7670G)    | ✅                  |                 |                   | ✅               |
| GPS_BuiltInEx                   | ✅(Except A7670G) | (Except A7670G)    | ✅                  |                 |                   | ✅               |
| GPS_NMEA_Parse                  | ✅(Except A7670G) | (Except A7670G)    | ✅                  |                 |                   | ✅               |
| GPS_NMEA_Output                 | ✅(Except A7670G) | (Except A7670G)    | ✅                  |                 |                   | ✅               |
| GPS_Acceleration                | ✅(Except A7670G) | (Except A7670G)    | ✅                  |                 |                   | ✅               |
| TCPClientMultiple               | ✅                |                    | ✅                  |                 |                   | ✅               |
| TextToSpeech                    | ✅                |                    | ❌   (Can't run)    |                 |                   | ✅               |
| SecureClient                    | ✅                |                    | ✅                  |                 |                   | ✅               |
| ReadBattery                     | ✅                | ❌   (Can't run)    | ✅                  |                 | ❌   (Can't run)   | ✅               |
| DeepSleep                       | ✅                |                    | ✅                  |                 |                   | ✅               |
| ModemSleep                      | ✅                |                    | ✅                  |                 |                   | ✅               |
| ModemPowerOff                   | ✅                |                    | ✅                  |                 |                   | ✅               |
| VoiceCalls                      | ✅                |                    | ❌                  |                 |                   | ✅               |
| SDCard                          | ✅                | ❌   (Can't run)    | ✅                  |                 |                   | ✅               |
| SerialRS485                     | ✅                |                    | ✅                  |                 |                   | ✅               |
| SendSMS                         | ✅                |                    | ❌                  |                 |                   | ✅               |
| ReadSMS                         | ✅                |                    | ❌                  |                 |                   | ✅               |
| SendLocationFromSMS             | ✅                |                    | ❌                  |                 |                   | ✅               |
| SendLocationFromSMS_Use_TinyGPS | ✅                |                    | ❌                  |                 |                   | ✅               |
| LBSExample                      | ✅                |                    | ❌   (No support)   |                 |                   | ✅               |
| Network                         | ✅                |                    | ✅                  |                 |                   | ✅               |
| MqttsBuiltlnAuth                | ✅                |                    | ✅                  |                 |                   | ✅               |
| MqttsBuiltlnSSL                 | ✅                |                    | ✅                  |                 |                   | ✅               |
| MqttsBuiltlnNoSSL               | ✅                |                    | ✅                  |                 |                   | ✅               |
| MqttsBuiltlnAWS                 | ✅                |                    | ✅                  |                 |                   | ✅               |
| MqttsBuiltlnHivemq              | ✅                |                    | ✅                  |                 |                   | ✅               |
| MqttsBuiltlnEMQX                | ✅                |                    | ✅                  |                 |                   | ✅               |
| MqttsBuiltlnWill                | ✅                |                    | ✅                  |                 |                   | ✅               |
| HttpsBuiltlnGet                 | ✅                |                    | ✅                  |                 |                   | ✅               |
| HttpsBuiltlnPost                | ✅                |                    | ✅                  |                 |                   | ✅               |
| HttpsBuiltlnPut                 | ✅                |                    | ✅                  |                 |                   | ✅               |
| PowerMonitoring                 | ✅                | ❌                  | ❌(No support)      |                 | ❌                 | ✅               |
| ULP_Monitor                     | ✅                |                    | ❌                  |                 |                   | ❌               |

- [1] T-A7608-ESP32 Conflict with Solar ADC
- [2] The relay driver conflicts with the board RST and cannot work
- [3] Requires external expansion board support [T-SimHat](https://www.lilygo.cc/products/lilygo%C2%AE-t-simhat-can-rs485-relay-5v)
- [4] SIM7670G - `SIM7670G-MNGV 2374B04` version supports SMS function, but it requires the operator base station to support SMS Over SGS service to send, otherwise it will be invalid
- [5] All versions of SIM7670G do not support voice

# Quick start ⚡

## 3️⃣ RT-Thread MicroPython (Recommended)

1. Install [Python](https://www.python.org/downloads/) (according to you to download the corresponding operating system version, suggest to download version 3.7 or later), MicroPython requirement 3. X version, if you have already installed, you can skip this step).

2. Install [VisualStudioCode](https://code.visualstudio.com/Download),Choose installation based on your system type.

3. Open the "Extension" section of the Visual Studio Code software sidebar(Alternatively, use "<kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>X</kbd>" to open the extension),Search for the "RT-Thread MicroPython" extension and download it.

4. During the installation of the extension, you can go to GitHub to download the program. You can download the main branch by clicking on the "<> Code" with green text, or you can download the program versions from the "Releases" section in the sidebar.

5. After the installation of the extension is completed, open the Explorer in the sidebar(Alternatively, use "<kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>E</kbd>" go open it),Click on "Open Folder," locate the project code you just downloaded (the entire folder), and click "Add." At this point, the project files will be added to your workspace.

6. Open the VisualStudioCode terminal (or use <kbd>Ctrl</kbd>+<kbd>`</kbd>), and enter the command to install the esptools tool.

   ```
   pip install esptools
   ```

7. Erase the flash memory and enter commands in the terminal.

   ```
   python -m esptool --chip esp32s3 --port COMX erase_flash
   ```

   Note：

   1. COMX is the port number. Change it to the port number corresponding to your computer.

8. Upload the MicroPython firmware.

   ```
   python -m esptool --chip esp32s3 --port COMX --baud 460800 --before=default_reset --after=hard_reset write_flash -z 0x0 D:\LilyGO-T-A76XX-Micropython-main\firmware\LilyGO-T-A76XX-Micropython-firmware.bin
   ```

   Note：

   1. COMX is the port number. Change it to the port number corresponding to your computer.
   2. D:\T-Connect-Pro\firmware\T-Connect-Pro_MicroPython_firmware_V1.0.bin is the firmware path. Change it to the corresponding storage path.

9. Click on "<kbd>[Device Connected/Disconnected](image/1.png)</kbd>" at the lower left corner, and then click on the pop-up window "<kbd>[COMX](image/2.png)</kbd>" at the top to connect the serial port. A pop-up pops up at the lower right corner saying "<kbd>[Connection successful](image/3.png)</kbd>" and the connection is complete.

10. After opening the code, click on“<kbd>[▶](image/4.png)</kbd>”at the lower left corner to run the program“<kbd>[Run this MicroPython file directly on the device](image/5.png)</kbd>”，Or use the<kbd>Alt</kbd>+<kbd>Q</kbd>），if you want to stop the program, click on the lower left corner of the“<kbd>[⏹](image/6.png)</kbd>”stop running the program.

> \[!IMPORTANT]
>
> 1. Unable to upload any code? Please see the FAQ below

# 4️⃣ FAQ

- **ESP32 (V1.x) version [T-A7670X][1]/[T-A7608X][4]  known issue**
  - When using battery power mode, BOARD_POWERON_PIN (IO12) must be set to a high level after ESP32 starts, otherwise a reset will occur.
  - Modem cannot be put into sleep mode when powered by USB-C. For a solution, see [here](https://github.com/Xinyuan-LilyGO/LilyGO-T-A76XX/blob/main/examples/ModemSleep/README.MD)
- **Can't turn on the phone after connecting the battery for the first time?**
  - This is due to the characteristics of the onboard battery over-discharge and over-charge chip. It cannot be turned on when the battery is connected for the first time. This can be solved by inserting a USB charger or reconnecting the battery. For details, please see the remarks on [page 4](https://www.lcsc.com/datasheet/lcsc_datasheet_2010160933_Shenzhen-Fuman-Elec-DW06D_C82123.pdf) of the datasheet.
- **GPS not working?**
  - See [issue/137](https://github.com/Xinyuan-LilyGO/LilyGO-T-A76XX/issues/137)
- **How to identify whether an external GPS module is installed**
  - See [issue/56](https://github.com/Xinyuan-LilyGO/LilyGO-T-A76XX/issues/56#issuecomment-1672628977)
- **VOLTE FAQ**
  - See [issue/115](https://github.com/Xinyuan-LilyGO/LilyGO-T-A76XX/issues/115)
- **Network registration denied?**
  - When the network registration is refused, please check whether the APN is set correctly. For details, please refer to [issue/104](https://github.com/Xinyuan-LilyGO/LilyGO-T-A76XX/issues/104)
- **Can't use 2G(GSM)?**
  - LilyGo has launched a separate 4G(LTE) version that can only use 4G(LTE) network. Please check whether it is a separate 4G(LTE) version during ordering.

- **How do I connect the antenna correctly?**
   1. Check the silk screen on the board. **GPS** stands for GPS antenna. Only active GPS antenna can be connected here.
   2. **SIM** or **MAIN**, this is the main antenna interface of LTE.
   3. **AUX** This is the diversity antenna for LTE, used to enhance the signal.
- **Solar input voltage range?**
   1. **4.4 ~ 6V** , As long as the voltage matches, the solar panel power is not limited.
- **Where can I connect a solar panel to charge the battery?**
  1. Some development boards (T-A7670, T-A7608, T-A7670-S3, T-A7608-S3) have a built-in solar cell input interface. Just connect the solar panel according to the correct polarity.
  2. If the board has a battery and charging management, you can also connect an external power supply to the VBUS pin, which is the input pin of the USB power supply. Connecting to VBUS will share the 5V voltage of USB-C. Please note that when connecting an external charger, please disconnect USB-C.
- **SIM767XG sendSMS and VoiceCall?**
   1. Although the manual of SIM767XG states that it has the functions of making voice calls and sending text messages, the current firmware does not support it.
- **Unable to detect SIMCard?**
   1. All SIM series need to insert the SIMCard into the board first and then power on to detect the SIM card. If the order is reversed, it will report that the SIMCard cannot be detected.
- **How to release the limitations of ESP32-WROVER-E GPIO12?**
  1. Since the ESP32-WROVER-E module is used, the internal flash voltage of the module is 3.3V by default. IO12 controls the startup flash startup voltage. If the external device connected to IO12 defaults to the HIGH level, then the startup will fall into an infinite restart. ,
  Two solutions.
  2. Replace the IO port and connect the default low-level device to IO12.
  3. Use espefuse to forcefully set the flash voltage to 3.3V. For details, please refer [here](https://docs.espressif.com/projects/esptool/en/latest/esp32/espefuse/set-flash-voltage-cmd.html#set-flash-voltage), this can only be set once, and cannot be set incorrectly. If the setting is incorrect, the module will never start.
- **What the onboard switch does**
  - When using the internal battery pack, the switch will work normally to power/power down the board. However, if an external battery pack is used and connected to the VBAT pin, the switch will be bypassed, meaning the only way to shut down is to disconnect the battery.
  - The switch is only for battery power and has no effect when plugged into USB.
- **About VBUS Pin**
  - VBUS Pin and USB-C are on the same line. Only when USB-C is connected, VBUS has voltage.
  - When only the battery is connected, VBUS has no voltage output.
  - If you want to connect an external power supply without connecting USB-C, VBUS Pin is the only voltage input pin. Please note that the maximum input of VBUS Pin is 5V, do not exceed 5V.

# 5️⃣Resource

1. SIMCOM official website document center
   - [SIMCOM official A7670X All Datasheet](https://cn.simcom.com/product/A7670X.html)
   - [SIMCOM official A7608X All Datasheet](https://cn.simcom.com/product/A7608X-H-E_SA.html)
   - [SIMCOM official SIM7672 All Datasheet](https://en.simcom.com/product/SIM7672.html)
2. A7670/A7608-Datasheet
   - [A76xx AT Command](./datasheet/A76XX/A76XX_Series_AT_Command_Manual_V1.09.pdf)
   - [A76xx MQTT(S) Application](./datasheet/A76XX/A76XX%20Series_MQTT(S)_Application%20Note_V1.02.pdf)
   - [A76xx HTTP(S) Application](./datasheet/A76XX/A76XX%20Series_HTTP(S)_Application%20Note_V1.02.pdf)
   - [A76xx GNSS Application](./datasheet/A76XX/A76XX%20Series_GNSS_Application%20Note_V1.02.pdf)
   - [A76xx FTP Application](./datasheet/A76XX/A76XX%20Series_FTP(S)_Application%20Note_V1.02.pdf)
   - [A76xx LBS Application](./datasheet/A76XX/A76XX%20Series_LBS_Application%20Note_V1.02.pdf)
   - [A76xx SSL Application](./datasheet/A76XX/A76XX%20Series_SSL_Application%20Note_V1.02.pdf)
   - [A76xx Sleep Application](./datasheet/A76XX/A76XX%20Series_Sleep%20Mode_Application%20Note_V1.02.pdf)
   - [A76xx Hardware Design manual](./datasheet/A76XX/A7670C_R2_硬件设计手册_V1.06.pdf)
   - [A76xx TCPIP Application](./datasheet/A76XX/A76XX%20Series_TCPIP_Application%20Note_V1.02.pdf)
3. SIM7670G-Datasheet
   - [SIM7670G Hardware Design manual](./datasheet/SIM767X/SIM7672X_Series_Hardware_Design_V1.02.pdf)
   - [SIM7670G AT Command](./datasheet/SIM767X/SIM767XX%20Series_AT_Command_Manual_V1.06.pdf)
   - [SIM7670G CE Certificate](./datasheet/SIM767X/SIM7670G_CE%20Certificate_2023.pdf)
   - [SIM7670G Series CMUX USER GUIDE](./datasheet/SIM767X/SIM767XX%20Series_CMUX_USER_GUIDE_V1.00.pdf)
4. Schematic
   - [T-A7608-S3 Schematic](./schematic/T-A7608-S3-V1.0.pdf)
   - [T-A7608X-DC-S3 Schematic](./schematic/T-A7608X-DC-S3-V1.0.pdf)
   - [T-A7608X Schematic](./schematic/T-A7608X-V1.0.pdf)
   - [T-A7608X-V2 Schematic](./schematic/A7608-ESP32-V2.pdf)
   - [T-A7670X Schematic](./schematic/T-A7670X-V1.1.pdf)
   - [T-Call-A7670 Schematic](./schematic/T-Call-A7670-V1.0.pdf)
   - [T-SIM7670G-S3 Schematic](./schematic/T-SIM7670G-S3-V1.0.pdf)
5. Dimensions
   - [T-A7608-S3 DWG](./dimensions/T-A7608-S3-V1.0.dwg)
   - [T-A7608X-DC-S3 DWG](./dimensions/T-A7608X-DC-S3-V1.0.dwg)
   - [T-A7608X DWG](./dimensions/T-A7608X-V1.0.dwg)
   - [T-A7670X DWG](./dimensions/T-A7670X-V1.1.dwg)
   - [T-Call-A7670 DWG](./dimensions/T-Call-A7670-V1.0.dwg)
   - [T-SIM7672-S3 DWG](./dimensions/T-SIM7670G-S3-V1.0.dwg)

6. Schematic
   - [T-A7670X schematic](./schematic/T-A7670X-V1.1.pdf)
   - [T-Call-A7670X schematic](./schematic/T-Call-A7670-V1.0.pdf)
   - [T-A7608 schematic](./schematic/T-A7608X-V1.0.pdf)
   - [T-A7608-S3 schematic](./schematic/T-A7608-S3-V1.0.pdf)
   - [T-SIM7670G-S3 schematic](./schematic/T-SIM767XG-S3-V1.0.pdf)
   - [T-PCIE-A7670 schematic](https://github.com/Xinyuan-LilyGO/LilyGo-T-PCIE/blob/master/schematic/A7670.pdf)
   - [T-ETH-ELite schematic](https://github.com/Xinyuan-LilyGO/LilyGO-T-ETH-Series/blob/master/schematic/T-ETH-ELite-LTE-Shield.pdf)

