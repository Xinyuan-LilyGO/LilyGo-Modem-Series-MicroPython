<div align="center" markdown="1">
  <img src="./images/LilyGo_logo.png" alt="LilyGo logo" width="100"/>
</div>
<h1 align = "center">🌟LilyGo-MicroPython🌟</h1>

# 1️⃣ **Windows subsystem for linux(WSL)**

1. Control Panel -> Programs and Features -> Enable or Disable windows Features. Open the Windows Features dialog box, select the "Windows Subsystem for Linux" TAB, and click "OK" to wait for the system configuration to complete.

   ![1](./images/1.png)

2. Open Microsoft Store.

   ![2](./images/2.png)

3. Search for "ubuntu 22.04.5" and install it as prompted.

   ![3](./images/3.png)

4. Open the downloaded "ubuntu 22.04.5" and display "Installing, this may take a few minutes..." .

   ![4](./images/4.png)

   Wait for a moment and then enter the username:

   ![5](./images/5.png)

   Then enter the password twice (remember the password you set here) :

   ![8](./images/8.png)

   After setting it up, you can successfully enter the WSL Ubuntu system.

   ![9](./images/9.png)



# 2️⃣ Download MobaXterm (terminal tool) and connect

1. Open the [MobaXterm](https://mobaxterm.mobatek.net/download-home-edition.html) website to download terminal tool.

   ![10](./images/10.png)

2. After the download is complete, extract it and open the "MobaXterm_installer_25.2.msi" installation package in the folder. Follow the prompts to complete the installation.

   ![10-1](./images/10-1.png)

3. After opening the software, select "Session" to connect.

   ![11](./images/11.png)

4. First, select WSL. Then, in Distribution, choose the corresponding Ubuntu version to download and click ok.

   ![12](./images/12.png)

5. Successfully entered the WSL Ubuntu system.

   ![13](./images/13.png)

   

# 3️⃣ Configure the python environment

1. Point `/usr/bin/python` to `/usr/bin/python3`.

   ```
   sudo ln -s /usr/bin/python3 /usr/bin/python
   ```

Enter the password you just set:

![14](./images/14.png)

2. Update the software package list.

   ```
   sudo apt-get update
   ```

   ![16](./images/16.png)

   Update completed:

   ![17](./images/17.png)

3. Installation environment:

   ```
   sudo apt-get install git wget libncurses-dev flex bison gperf python3 python3-pip python3-setuptools python3-serial python3-click python3-cryptography python3-future python3-pyparsing python3-pyelftools cmake ninja-build ccache libffi-dev libssl-dev python-is-python3
   ```

   ![18](./images/18.png)

   Installation completed:

   ![19](./images/19.png)

4. Install "python3.10-venv".

   ```
   sudo apt install python3.10-venv
   ```

   ![19-1](./images/19-1.png)

   Installation completed:

   ![19-3](./images/19-3.png)

   

# 4️⃣ **Esp-idf development environment**

1. Execute the following instructions in sequence in the command line mode of the linux subsystem:

   ```
   git clone https://gitee.com/EspressifSystems/esp-gitee-tools.git
   ```

   ![21](./images/21.png)

   ```
   git clone https://gitee.com/EspressifSystems/esp-idf.git
   ```

   ![23](./images/23.png)

2. Enter the "esp-idf" folder.

   ```
   cd esp-idf
   ```

   ![24](./images/24.png)

3. Switch branches.

   ```
   git checkout v5.2.2
   ```

   ![26](./images/26.png)

4. Enter the "esp-gitee-tools" folder.

   ```
   cd ../esp-gitee-tools
   ```

   ![27](./images/27.png)

5. Execute the script "submodule-update.sh".

   ```
   ./submodule-update.sh ~/esp-idf/
   ```

   ![28](./images/28.png)

   Run completed:

   ![29](./images/29.png)

6. Execute the "install.sh" script.

   ```
   ./install.sh ~/esp-idf/
   ```

   ![30](./images/30.png)

   Run completed:

   ![31](./images/31.png)

7. Configure environment variables.

   ```
   . /home/lilygo-micropython/esp-idf/export.sh
   ```

   ![32](./images/32.png)

   Configuration completed:

   ![33](./images/33.png)

   

# 5️⃣ **Make the MicroPython firmware**

1. Exit the current folder and download micropython.

   ```
   cd ~
   ```

   ```
   git clone https://github.com/Xinyuan-LilyGO/micropython.git
   ```

   ![34](./images/34.png)

   Download completed. (If the download fails, please try again):

   ![35](./images/35.png)

2. Enter the micropython folder and compile the "mpy-cross" tool.

   ```
   cd micropython
   ```

   ```
   make -C mpy-cross
   ```

   ![36](./images/36.png)

   Compilation completed:
   ![37](./images/37.png)

3. Enter the corresponding development board folder ("ports/xxx"), here taking "LILYGO_T_Connect_Pro_S3" as an example.

   ```
   cd ports/LILYGO_T_Connect_Pro_S3
   ```

   ![38](./images/38.png)

4. Initialize the sub-module.

   ```
   make submodules
   ```

   ![39](./images/39.png)

5. Make the firmware.

   ```
   make
   ```

   ![40](./images/40.png)

   Make completed：

   ![41](./images/41.png)

6. Download the compiled firmware and click the mouse to enter the "build-ESP32_GENERIC_S3" folder (if you are using ESP32, the folder name is "build-ESP32_GENERIC").

   ![41-1](./images/41-1.png)

7. In the file, find the "firmware.bin" file, right-click the mouse, and select "Download" to download it to your computer.

   ![42](./images/42.png)
