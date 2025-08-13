<div align="center" markdown="1">
  <img src="../../../../images/LilyGo_logo.png" alt="LilyGo logo" width="100"/>
</div>

<h1 align = "center">🌟LilyGo T-A7670X-S3-MicroPython-Standard🌟</h1>

## Overview

* This page introduces the hardware parameters related to `LilyGo T-A7670X-S3-Standard`

### Product

| Product                   | SOC              | Flash          | PSRAM         |
| ------------------------- | ---------------- | -------------- | ------------- |
| [T-A7670X-S3-Standard][1] | ESP32-S3-WROOM-1 | 16MB(Quad-SPI) | 2MB(Quad-SPI) |

[1]: https://www.lilygo.cc/products/

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
   python -m esptool --chip esp32s3 --port COMX --baud 460800 --before=default_reset --after=hard_reset write_flash -z 0x0 D:\LilyGO-T-A76XX-Micropython-main\firmware\LilyGO-T-SIM7670X-S3-Micropython-firmware.bin
   ```

   Note：

   1. COMX is the port number. Change it to the port number corresponding to your computer.
   2. D:\LilyGO-T-A76XX-Micropython-main\firmware\LilyGO-T-SIM7670X-S3-Micropython-firmware.bin is the firmware path. Change it to the corresponding storage path.
   3. **If you need to make your own MicroPython firmware, please refer to [Tutorial](../../../../make_firmware/README.md) for the operation.**

9. Click on "<kbd>[Device Connected/Disconnected](../../../../images/1.png)</kbd>" at the lower left corner, and then click on the pop-up window "<kbd>[COMX](../../../../images/2.png)</kbd>" at the top to connect the serial port. A pop-up pops up at the lower right corner saying "<kbd>[Connection successful](../../../../images/3.png)</kbd>" and the connection is complete.

10. After opening the code, click on“<kbd>[▶](../../../../images/4.png)</kbd>”at the lower left corner to run the program“<kbd>[Run this MicroPython file directly on the device](../../../../images/5.png)</kbd>”，Or use the<kbd>Alt</kbd>+<kbd>Q</kbd>），if you want to stop the program, click on the lower left corner of the“<kbd>[⏹](../../../../images/6.png)</kbd>”stop running the program.**(If you need to run the program automatically on the board, please copy the code to the "[main.py](../../../../examples/main.py)" file under the "exampels" folder and save it. Select the "main.py" file with the left mouse button. Right-click the mouse and select "[Download this file/folder to device](../../../../images/7.png)", then press the reset button on the board to run the program automatically.)**

> \[!IMPORTANT]
>
> 1. Unable to upload any code? Please see the FAQ below

### 📍 Pins Map

| Name              | GPIO NUM | Free |
| ----------------- | -------- | ---- |
| Modem TX          | 4        | ❌    |
| Modem RX          | 5        | ❌    |
| Modem RING        | 6        | ❌    |
| Modem DTR         | 7        | ❌    |
| Modem PWRKEY      | 46       | ❌    |
| GPS RX            | 48       | ❌    |
| GPS TX            | 45       | ❌    |
| Modem RTS*        | 48       | ❌    |
| Modem CTS*        | 45       | ❌    |
| GPS PPS           | 17       | ❌    |
| GPS Shield Wakeup | 0        | ❌    |
| Battery ADC Pin   | 8        | ❌    |
| Solar ADC Pin     | 18       | ❌    |
| SD SCK            | 12       | ❌    |
| SD MISO           | 13       | ❌    |
| SD MOSI           | 11       | ❌    |
| SD CS             | 10       | ❌    |
| Power Save Mode   | 42       | ❌    |
| Camera XCLK       | 21       | ❌    |
| Camera SIOD       | 1        | ❌    |
| Camera SIOC       | 41       | ❌    |
| Camera VSYNC      | 9        | ❌    |
| Camera HREF       | 14       | ❌    |
| Camera PCLK       | 37       | ❌    |
| Camera Y9         | 40       | ❌    |
| Camera Y8         | 39       | ❌    |
| Camera Y7         | 38       | ❌    |
| Camera Y6         | 36       | ❌    |
| Camera Y5         | 16       | ❌    |
| Camera Y4         | 47       | ❌    |
| Camera Y3         | 15       | ❌    |
| Camera Y2         | 35       | ❌    |
| Default SDA       | 3        | ✅️    |
| Default SCL       | 2        | ✅️    |

* The `Power Save Mode pin` is used to set the power capability of the power supply. Setting it to HIGH enables maximum power output. Setting it to LOW reduces current consumption.
* If a camera is connected externally, there will be no free GPIO. If the camera is not used, the camera's GPIO can be used for other purposes.
* `SDA`, `SCL` can only be used as I2C function, not as other functions
* `GPS Shield Wakeup Pin` is only used when an external GPS module is connected. Otherwise, it is idle. It is not recommended to use this GPIO. This IO is connected only when using `A7670G + L76K GPS`, otherwise it is not connected
* The camera must be powered on to be detected, otherwise the camera cannot be used. For how to turn it on, please refer to the Camera example.
* Modem RTS/Modem CTS are not connected by default. They are connected to the GPS RX/TX of the Modem by default. If you need to use them, you need to short-circuit the RTS/CTS short-circuit pads on the back of the PCB, and then separate the GPS TX and RX pads.

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

### ⚡Battery Protector Description

| Features                | Details  |
| ----------------------- | -------- |
| Over-Voltage Threshold  | 4.30V    |
| Under-Voltage Threshold | 2.4V     |
| Over-Charge Current     | 3.6A     |
| Over-Discharge Current  | 4.6A     |
| Short-Circuit Current   | 2 × 4.6A |

### Connector Description

| Button                     | Function                      | Location   |
| -------------------------- | ----------------------------- | ---------- |
| JST 1.0mm `SPEK`           | Connect speakers              | PCB Bottom |
| JST 1.0mm `MIC`            | Connect condenser microphone  | PCB Bottom |
| JST 1.0mm `RTC`            | Connect 3~3.3V button battery | PCB Bottom |
| JST 2.0mm Solar            | Connect to a 5~6V solar panel | PCB Top    |
| 24 Pin 0.5mm FPC Connector | Connect OV2640/OV5640 camera  | PCB Top    |

* Camera models support cameras supported by esp32 platform

### Button Description

| Button               | Function                            | Location   |
| -------------------- | ----------------------------------- | ---------- |
| BOOT  (ESP32S3 back) | Customizable function/Download mode | PCB Bottom |
| RST   (ESP32S3 back) | Reset devices button                | PCB Bottom |
| SBOOT(Near to modem) | Modem Upgrade mode                  | PCB Bottom |

* **RST** and **BOOT** Located on the bottom of the ESP32 module
* **SBOOT** is located on the back near the modem module
* Press and hold the `BOOT` button before powering on. The board is now in waiting mode for downloading.
* Before powering on, keep the `SBOOT` button pressed to put the modem into firmware update mode.
* The above naming method is subject to the board silk screen printing

### Antenna Description

| NAME | Function                     |
| ---- | ---------------------------- |
| LTE  | LTE Main antenna interface   |
| GNSS | GPS active antenna interface |

* When using, you only need to connect the LTE antenna you wear to the LTE IPEX first generation interface. The AUX antenna does not need to be connected.
* The above naming method is subject to the board silk screen printing

### LED Description

| FUNCTION        | COLOR                            | STATE                                                                  |
| --------------- | -------------------------------- | ---------------------------------------------------------------------- |
| MODEM STATE     | RED   (Near the modem)           | Startup:ON                                                             |
| MODEM NET       | RED   (Near the modem)           | Network status indicator                                               |
| GPS PPS LED     | RED  (Near the modem)            | Starting:ON,Startup completed:OFF,Position fix:Flashes once per second |
| CHARGE LED      | RED  (Near the battery switch)   | Charging:ON  Charging complete:OFF                                     |
| CHARGE DONE LED | GREEN  (Near the battery switch) | Charging:OFF  Charging complete:ON                                     |

* `CHARGE DONE LED` remains on if no battery is connected
* Modem Status light and network status led cannot be turned off

### Resource

* [GPS Antenna](../../../../datasheet/GPS%20Antenna%20Specifications.pdf)
* [LTE Antenna](../../../../datasheet/LTE%20Antenna%20Specifications.pdf)
* [T-A7670X-S3-Standard Schematic](../../../../schematic/standard/T-A7670X-S3-Standard_Rev1.0.pdf)
* [SIMCOM official A7670X All Datasheet](https://cn.simcom.com/product/A7670X.html)
* [For A7670X series documentation, please visit the datasheet directory.](../../../../datasheet/A7670X/)

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
* **Why is my board continuously failing to download the program?**
  1. Please hold down the "BOT" key, then press the "RST" key, and use the command again to burn the firmware.
