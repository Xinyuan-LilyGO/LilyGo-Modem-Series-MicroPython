<div align="center" markdown="1">
  <img src="../../../../images/LilyGo_logo.png" alt="LilyGo logo" width="100"/>
</div>

<h1 align = "center">🌟LilyGo A7670X ESP32 MicroPython Version🌟</h1>

## Overview

* This page introduces the hardware parameters related to `LilyGo A7670X ESP32 Version`

### Product

| Product              | SOC            | Flash         | PSRAM         |
| -------------------- | -------------- | ------------- | ------------- |
| [T-A7670E ESP32][1]  | ESP32-WROVER-E | 4MB(Quad-SPI) | 8MB(Quad-SPI) |
| [T-A7670SA ESP32][1] | ESP32-WROVER-E | 4MB(Quad-SPI) | 8MB(Quad-SPI) |
| [T-A7670G ESP32][1]  | ESP32-WROVER-E | 4MB(Quad-SPI) | 8MB(Quad-SPI) |

[1]: https://lilygo.cc/products/t-sim-a7670e?_pos=1&_sid=01b963136&_ss=r&variant=42534734495925

### Modem differences

| Model           | GPS | Phone Call | SMS | Frequency band                                                                                                     |
| --------------- | --- | ---------- | --- | ------------------------------------------------------------------------------------------------------------------ |
| A7670E-FASE     | ✅   | ✅          | ✅   | LTE-FDD:B1/B3/B5/B7/B8/B20  GSM:900/1800                                                                           |
| A7670SA-FASE    | ✅   | ✅          | ✅   | LTE-FDD:B1/B2/B3/B4/B5/B7/B8/B28/B66  GSM:850/900/1800/1900                                                        |
| A7670E-LNXY-UBL | ❌   | ❌          | ❌   | LTE-FDD:B1/B3/B5/B7/B8/B20                                                                                         |
| A7670SA-LASE    | ❌   | ✅          | ✅   | LTE-FDD:B1/B2/B3/B4/B5/B7/B8/B28/B66  GSM:850/900/1800/1900                                                        |
| A7670SA-LASC    | ❌   | ✅          | ✅   | LTE-FDD:B1/B2/B3/B4/B5/B7/B8/B28/B66  GSM:850/900/1800/1900                                                        |
| A7670G-LLSE     | ❌   | ✅          | ✅   | LTE-FDD:B1/B2/B3/B4/B5/B7/B8/B20/B28/B66  LTE-TDD:B34/B38/B39/B40/B41 GSM:850/900/1800/1900                        |
| A7670G-LABE     | ❌   | ✅          | ✅   | LTE-FDD:B1/B2/B3/B4/B5/B7/B8/B12/B13/B18/B19/B20/B25/B26/B28/B66 LTE-TDD:B34/B38/B39/B40/B41 GSM:850/900/1800/1900 |
| A7670E-LASE     | ❌   | ✅          | ✅   | LTE-FDD:B1/B3/B5/B7/B8/B20  GSM:900/1800                                                                           |

> \[!IMPORTANT]
> How to check the specific model version of the modem? Sending AT+SIMCOMATI can return the firmware version and hardware version used.
>
> Please note that whether the GNSS IPEX antenna connector is on the PCB or not depends on the actual modem version. The A7670G modem does not have internal GPS functionality, regardless of whether GPS is included in your order. If you purchased the A7670G with GPS, you will need to use an external GPS module.

### RT-Thread MicroPython Quick Start

1. Install [Python](https://www.python.org/downloads/) (according to you to download the corresponding operating system version, suggest to download version 3.7 or later), MicroPython requirement 3. X version, if you have already installed, you can skip this step).
2. Install [VisualStudioCode](https://code.visualstudio.com/Download),Choose installation based on your system type.

3. Open the "Extension" section of the Visual Studio Code software sidebar(Alternatively, use "<kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>X</kbd>" to open the extension),Search for the "RT-Thread MicroPython" extension and download it.

4. During the installation of the extension, you can go to GitHub to download the program. You can download the main branch by clicking on the "<> Code" with green text, or you can download the program versions from the "Releases" section in the sidebar.

5. After the installation of the extension is completed, open the Explorer in the sidebar(Alternatively, use "<kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>E</kbd>" go open it),Click on "Open Folder," locate the project code you just downloaded (the entire folder), and click "Add." At this point, the project files will be added to your workspace.

6. Open the VisualStudioCode terminal (or use <kbd>Ctrl</kbd>+<kbd>`</kbd>), and enter the command to install the esptools tool.

   ```
   pip install esptool
   ```

7. ESP32 erase the flash memory and enter commands in the terminal:

   ```
   python -m esptool --chip esp32 --port COMX erase_flash
   ```

   Note：

   1. COMX is the port number. Change it to the port number corresponding to your computer.
   
8. ESP32 upload the MicroPython firmware:

   ```
   python -m esptool --chip esp32 --port COMX --baud 460800 --before=default_reset --after=hard_reset write_flash -z 0x1000 D:\LilyGO-T-A76XX-Micropython-main\firmware\LilyGO-T-A7670X-Micropython-firmware.bin
   ```

   Note：

   1. COMX is the port number. Change it to the port number corresponding to your computer.
   2. D:\LilyGO-T-A76XX-Micropython-main\firmware\LilyGO-T-A7670X-Micropython-firmware.bin is the firmware path. Change it to the corresponding storage path.
   3. **If you need to make your own MicroPython firmware, please refer to [Tutorial](../../../../make_firmware/README.md) for the operation.**

9. Click on "<kbd>[Device Connected/Disconnected](../../../../images/1.png)</kbd>" at the lower left corner, and then click on the pop-up window "<kbd>[COMX](../../../../images/2.png)</kbd>" at the top to connect the serial port. A pop-up pops up at the lower right corner saying "<kbd>[Connection successful](../../../../images/3.png)</kbd>" and the connection is complete.

10. After opening the code, click on“<kbd>[▶](../../../../images/4.png)</kbd>”at the lower left corner to run the program“<kbd>[Run this MicroPython file directly on the device](../../../../images/5.png)</kbd>”，Or use the<kbd>Alt</kbd>+<kbd>Q</kbd>），if you want to stop the program, click on the lower left corner of the“<kbd>[⏹](../../../../images/6.png)</kbd>”stop running the program.**(If you need to run the program automatically on the board, please copy the code to the "[main.py](../../../../examples/main.py)" file under the "exampels" folder and save it. Select the "main.py" file with the left mouse button. Right-click the mouse and select "[Download this file/folder to device](../../../../images/7.png)", then press the reset button on the board to run the program automatically.)**

> \[!IMPORTANT]
>
> 1. Unable to upload any code? Please see the FAQ below

### 📍 Pins Map

| Name                     | GPIO NUM | Free |
| ------------------------ | -------- | ---- |
| Peripheral power control | 12       | ❌    |
| Modem TX                 | 26       | ❌    |
| Modem RX                 | 27       | ❌    |
| Modem PWR                | 4        | ❌    |
| Modem RESET              | 5        | ❌    |
| Modem RING               | 33       | ❌    |
| Modem DTR                | 25       | ❌    |
| SD SCK                   | 14       | ❌    |
| SD MISO                  | 2        | ❌    |
| SD MOSI                  | 15       | ❌    |
| SD CS                    | 13       | ❌    |
| Battery ADC Pin          | 35       | ❌    |
| Solar ADC Pin            | 36       | ❌    |
| Default SDA              | 21       | ✅️    |
| Default SCL              | 22       | ✅️    |

* Peripheral power control pin. When using SD or modem, this GPIO must be set to high level, otherwise these functions cannot be used.
* ESP32 models GPIO33 and above can only be set as input, not output

> \[!IMPORTANT]
> ESP32 version Since the SD card uses IO2 as CS, you cannot upload software when you insert the SD card, so you must remove the SD card when uploading new code

### ⚡ Electrical parameters

| Features                        | Details |
| ------------------------------- | ------- |
| 🔗USB-C Input Voltage            | 5V      |
| ⚡Solar Input Voltage            | 5~6V    |
| ⚡USB-C/Solar Charge Max Current | 500mA   |
| 🔋Battery Voltage                | 3.7V    |

> \[!TIP]
>
> 1. The onboard JST2.0 interface is only used to connect the solar panel to charge the battery, and cannot provide power to the board from this interface
> 2. It is recommended to use a solar panel with an output voltage of 6V or 5V and a power of about 5-10W. Solar energy can only charge the battery. Without the battery, the panel cannot supply power.
> Please note that this is only a suggestion. It is not necessary to use a 5-10W solar panel. 1W is also acceptable.
> The size of the solar panel determines the current and speed of solar charging. Please note that depending on the environment,
> the sunshine time may not exceed one hour per day. At this time, if the solar panel is too small and the light is not sufficient, it cannot be charged.

### Button Description

| Button              | Function                            |
| ------------------- | ----------------------------------- |
| IO0(Close to esp)   | Customizable function/Download mode |
| RST                 | Reset devices button                |
| BOT(Close to modem) | Modem Upgrade mode                  |

* Press and hold the IO0 button before powering on. The board is now in waiting mode for downloading.
* Before powering on, keep the BOT button pressed to put the modem into firmware update mode.
* The above naming method is subject to the board silk screen printing

### Antenna Description

|      | Function                     |
| ---- | ---------------------------- |
| SIM  | LTE Main antenna interface   |
| GNSS | GPS active antenna interface |

* The above naming method is subject to the board silk screen printing

### LED Description

| FUNCTION            | COLOR                           |
| ------------------- | ------------------------------- |
| MODEM STATUS        | RED   (Near the modem)          |
| MODEM NETWORK STATE | RED   (Near the modem)          |
| CHARGE LED          | BLUE  (Near the battery switch) |
| CHARGE DONE LED     | BLUE  (Near the battery switch) |

* Modem Status light and network status led cannot be turned off

### Resource

* [GPS Antenna](../../../../datasheet/GPS%20Antenna%20Specifications.pdf)
* [LTE Antenna](../../../../datasheet/LTE%20Antenna%20Specifications.pdf)
* [T-A7670X Schematic](../../../../schematic/esp32/T-A7670X-V1.4.pdf)
* [SIMCOM official A7670X All Datasheet](https://cn.simcom.com/product/A7670X.html)
* [For A7670X series documentation, please visit the datasheet directory.](../../../../datasheet/A7670X/)
* [Board dimensions](../../../../dimensions/esp32/T-A760X-ESP32.dxf)
* [Case](../../../../dimensions/esp32/T-A7670X-Shell+GPS.7z)

### FAQ

* **ESP32 (V1.x) version T-A7670X  known issue**
  1. When using battery power mode, BOARD_POWERON_PIN (IO12) must be set to a high level after ESP32 starts, otherwise a reset will occur.
  2. Modem cannot be put into sleep mode when powered by USB-C. For a solution, see [here](https://github.com/Xinyuan-LilyGO/LilyGO-T-A76XX/blob/main/examples/ModemSleep/README.MD)

* **If the above method still fails to upload the sketch, please follow the method below to test whether the USB2TTL communication is normal.**
  1. Connect USB-C to PC
  2. Open the serial monitor and adjust the baud rate to 115200
  3. Press the RST button on the board to restart
  4. If you can see the startup information, it means that the USB2TTL communication is normal. If nothing is displayed in the serial monitor, it may be that the USB2TTL bridge is damaged

* **Upgrade modem firmware**
  1. [T-A76XX Upgrade docs](../../../../docs/update_fw.md) / [Video](https://youtu.be/AZkm-Z7mKn8)

* **Unable to detect SIMCard?**
   1. Need to insert the SIMCard into the board first and then power on to detect the SIM card. If the order is reversed, it will report that the SIMCard cannot be detected.

* **Can't upload any sketch，Please enter the upload mode manually.**
   1. Connect the board via the USB cable
   2. Press and hold the **IO0** button , While still pressing the **IO0** button
   3. Press **RST** button
   4. Release the **RST** button
   5. Release the **IO0** button
   6. Upload sketch

* **What the onboard switch does**
  1. When using the internal battery pack, the switch will work normally to power/power down the board. However, if an external battery pack is used and connected to the VBAT pin, the switch will be bypassed, meaning the only way to shut down is to disconnect the battery.
  2. The switch is only for battery power and has no effect when plugged into USB

* **About VBUS Pin**
  1. VBUS Pin and USB-C are on the same line. Only when USB-C is connected, VBUS has voltage
  2. When only the battery is connected, VBUS has no voltage output
  3. If you want to connect an external power supply without connecting USB-C, VBUS Pin is the only voltage input pin. Please note that the maximum input of VBUS Pin is 5V, do not exceed 5V
