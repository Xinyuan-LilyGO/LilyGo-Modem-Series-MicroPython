<div align="center" markdown="1">
  <img src="../../../../images/LilyGo_logo.png" alt="LilyGo logo" width="100"/>
</div>


<h1 align = "center">🌟LilyGo SIM7670G ESP32S3 Version🌟</h1>

## Overview

* This page introduces the hardware parameters related to `LilyGo SIM7670G ESP32S3 Version`

### Product

| Product                 | SOC              | Flash          | PSRAM    |
| ----------------------- | ---------------- | -------------- | -------- |
| [T-SIM7670G ESP32S3][1] | ESP32-S3-WROOM-1 | 16MB(Quad-SPI) | 8MB(OPI) |

[1]: https://www.lilygo.cc/products/t-sim-7670g-s3

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

7. ESP32S3 erase the flash memory and enter commands in the terminal:

   ```
   python -m esptool --chip esp32s3 --port COMX erase_flash
   ```

   Note：

   1. COMX is the port number. Change it to the port number corresponding to your computer.

8. ESP32S3 upload the MicroPython firmware:

   ```
   python -m esptool --chip esp32s3 --port COMX --baud 460800 --before=default_reset --after=hard_reset write_flash -z 0x0 D:\LilyGO-T-A76XX-Micropython-main\firmware\LilyGO-T-SIM7670G-S3-STAN-Micropython-firmware.bin
   ```

   Note：

   1. COMX is the port number. Change it to the port number corresponding to your computer.
   2. D:\LilyGO-T-A76XX-Micropython-main\firmware\LilyGO-T-SIM7670G-S3-STAN-Micropython-firmware.bin is the firmware path. Change it to the corresponding storage path.
   3. **If you need to make your own MicroPython firmware, please refer to [Tutorial](../../../../make_firmware/README.md) for the operation.**

9. Click on "<kbd>[Device Connected/Disconnected](../../../../images/1.png)</kbd>" at the lower left corner, and then click on the pop-up window "<kbd>[COMX](../../../../images/2.png)</kbd>" at the top to connect the serial port. A pop-up pops up at the lower right corner saying "<kbd>[Connection successful](../../../../images/3.png)</kbd>" and the connection is complete.

10. After opening the code, click on“<kbd>[▶](../../../../images/4.png)</kbd>”at the lower left corner to run the program“<kbd>[Run this MicroPython file directly on the device](../../../../images/5.png)</kbd>”，Or use the<kbd>Alt</kbd>+<kbd>Q</kbd>），if you want to stop the program, click on the lower left corner of the“<kbd>[⏹](../../../../images/6.png)</kbd>”stop running the program.**(If you need to run the program automatically on the board, please copy the code to the "[main.py](../../../../examples/main.py)" file under the "exampels" folder and save it. Select the "main.py" file with the left mouse button. Right-click the mouse and select "[Download this file/folder to device](../../../../images/7.png)", then press the reset button on the board to run the program automatically.)**

> \[!IMPORTANT]
>
> 1. Unable to upload any code? Please see the FAQ below

### 📍 Pins Map

| Name            | GPIO NUM | Free |
| --------------- | -------- | ---- |
| Modem TX        | 11       | ❌    |
| Modem RX        | 10       | ❌    |
| Modem PWRKEY    | 18       | ❌    |
| Modem RESET     | 17       | ❌    |
| Modem RING      | 3        | ❌    |
| Modem DTR       | 9        | ❌    |
| Board LED       | 12       | ❌    |
| Battery ADC Pin | 4        | ❌    |
| Solar ADC Pin   | 5        | ❌    |
| SD SCK          | 21       | ❌    |
| SD MISO         | 47       | ❌    |
| SD MOSI         | 14       | ❌    |
| SD CS           | 13       | ❌    |

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

| Button                   | Function                            |
| ------------------------ | ----------------------------------- |
| BOOT(Close to esp)       | Customizable function/Download mode |
| RST                      | Reset devices button                |
| SIM-BOOT(Close to modem) | Modem Upgrade mode                  |

* Press and hold the `BOOT` button before powering on. The board is now in waiting mode for downloading.
* Before powering on, keep the `SIM-BOOT` button pressed to put the modem into firmware update mode.
* The above naming method is subject to the board silk screen printing

### Antenna Description

|      | Function                     |
| ---- | ---------------------------- |
| SIM  | LTE Main antenna interface   |
| GNSS | GPS active antenna interface |

* When using, you only need to connect the LTE antenna you wear to the SIM IPEX first generation interface. The AUX antenna does not need to be connected.
* The above naming method is subject to the board silk screen printing

### LED Description

| FUNCTION            | COLOR                           |
| ------------------- | ------------------------------- |
| MODEM STATUS        | RED   (Near the modem)          |
| MODEM NETWORK STATE | RED   (Near the modem)          |
| CHARGE LED          | BLUE  (Near the battery switch) |
| CHARGE DONE LED     | BLUE  (Near the battery switch) |
| ON BOARD LED        | BLUE  (Near the RST button)     |

* Modem Status light and network status led cannot be turned off

### Resource

* [GPS Antenna](../../../../datasheet/GPS%20Antenna%20Specifications.pdf)
* [LTE Antenna](../../../../datasheet/LTE%20Antenna%20Specifications.pdf)
* [T-SIM7670G Schematic](../../../../schematic/esp32s3/T-SIM7670G-S3-V1.1.pdf)
* [SIMCOM official SIM7670G All Datasheet](https://cn.simcom.com/product/SIM7670X.html)
* [For SIM7670G series documentation, please visit the datasheet directory.](../../../../datasheet/SIM767X/)
* [Board dimensions](../../../../dimensions/esp32s3/T-SIM7670G-S3.dxf)

### FAQ

* **Upgrade modem firmware**
  1. [T-A76XX Upgrade docs](../../../../docs/update_fw.md) / [Video](https://youtu.be/AZkm-Z7mKn8)

* **Unable to detect SIMCard?**
   1. Need to insert the SIMCard into the board first and then power on to detect the SIM card. If the order is reversed, it will report that the SIMCard cannot be detected.

* **Can't upload any sketch，Please enter the upload mode manually.**
   1. Connect the board via the USB cable
   2. Press and hold the **BOOT** button , While still pressing the **BOOT** button
   3. Press **RST** button
   4. Release the **RST** button
   5. Release the **BOOT** button
   6. Upload sketch

* **What the onboard switch does**
  1. When using the internal battery pack, the switch will work normally to power/power down the board. However, if an external battery pack is used and connected to the VBAT pin, the switch will be bypassed, meaning the only way to shut down is to disconnect the battery.
  2. The switch is only for battery power and has no effect when plugged into USB

* **About VBUS Pin**
  1. VBUS Pin and USB-C are on the same line. Only when USB-C is connected, VBUS has voltage
  2. When only the battery is connected, VBUS has no voltage output
  3. If you want to connect an external power supply without connecting USB-C, VBUS Pin is the only voltage input pin. Please note that the maximum input of VBUS Pin is 5V, do not exceed 5V
