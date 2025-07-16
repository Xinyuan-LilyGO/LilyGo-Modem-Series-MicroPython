'''
 * @file      SDCard.py
 * @license   MIT
 * @copyright Copyright (c) 2025  Shenzhen Xin Yuan Electronic Technology Co., Ltd
 * @date      2025-07-16
'''
import os
import machine
import uos
import time
import utilities

def listDir(fs, dirname, levels):
    print("Listing directory: %s" % dirname)
    try:
        entries = []
        for entry in fs.ilistdir(dirname):
            entries.append(entry)
        for entry in entries:
            name, type, inode, size = entry if len(entry) == 4 else (entry[0], entry[1], 0, 0)
            path = dirname + '/' + name if dirname != '/' else '/' + name
            if type == 0x4000: 
                print("  DIR : %s" % name)
                if levels:
                    listDir(fs, path, levels - 1)
        for entry in entries:
            name, type, inode, size = entry if len(entry) == 4 else (entry[0], entry[1], 0, 0)
            path = dirname + '/' + name if dirname != '/' else '/' + name
            if type != 0x4000:
                print("  FILE: %s  SIZE: %d" % (name, size)) 
    except:
        print("Failed to open directory")
        return

def createDir(fs, path):
    print("Creating Dir: %s" % path)
    try:
        fs.mkdir(path)
        print("Dir created")
    except:
        print("mkdir failed")

def removeDir(fs, path):
    print("Removing Dir: %s" % path)
    try:
        fs.rmdir(path)
        print("Dir removed")
    except:
        print("rmdir failed")

def readFile(fs, path):
    print("Reading file: %s" % path)
    try:
        with fs.open(path, 'r') as file:
            print("Read from file: ", end='')
            while True:
                data = file.read(128)
                if not data:
                    break
                print(data, end='')
            print()
    except:
        print("Failed to open file for reading")

def writeFile(fs, path, message):
    print("Writing file: %s" % path)
    try:
        with fs.open(path, 'w') as file:
            file.write(message)
            print("File written")
    except:
        print("Failed to open file for writing")

def appendFile(fs, path, message):
    print("Appending to file: %s" % path)
    try:
        with fs.open(path, 'a') as file:
            file.write(message)
            print("Message appended")
    except:
        print("Failed to open file for appending")

def renameFile(fs, path1, path2):
    print("Renaming file %s to %s" % (path1, path2))
    try:
        fs.rename(path1, path2)
        print("File renamed")
    except:
        print("Rename failed")

def deleteFile(fs, path):
    print("Deleting file: %s" % path)
    try:
        fs.remove(path)
        print("File deleted")
    except:
        print("Delete failed")

def testFileIO(fs, path):
    try:
        with fs.open(path, 'rb') as file:
            start = time.ticks_ms()
            size = 0
            buf = bytearray(512)
            while True:
                read = file.readinto(buf)
                if not read:
                    break
                size += read
            end = time.ticks_diff(time.ticks_ms(), start)
            print("%u bytes read for %u ms" % (size, end))
    except:
        print("Failed to open file for reading")
    try:
        with fs.open(path, 'wb') as file:
            start = time.ticks_ms()
            buf = bytearray(512)
            for i in range(2048):
                file.write(buf)
            end = time.ticks_diff(time.ticks_ms(), start)
            print("%u bytes written for %u ms" % (2048 * 512, end))
    except:
        print("Failed to open file for writing")

def setup():
    print("\nStarting SD Card Test\n")
    if 'utilities.BOARD_POWERON_PIN' in globals():
        power_pin = machine.Pin(utilities.BOARD_POWERON_PIN, machine.Pin.OUT)
        power_pin.value(1)
    try:
        sd = machine.SDCard(
            slot=2,
            width=1,
            sck=machine.Pin(utilities.BOARD_SCK_PIN),
            miso=machine.Pin(utilities.BOARD_MISO_PIN),
            mosi=machine.Pin(utilities.BOARD_MOSI_PIN),
            cs=machine.Pin(utilities.BOARD_SD_CS_PIN),
            freq=20000000)
        vfs = uos.VfsFat(sd)
        uos.mount(vfs, '/')
        print("Card Mounted")
    except:
        print("Card Mount Failed")
        return
    print("SD Card Type: ", end='')
    try:
        card_info = os.statvfs('/')
        total_size = (card_info[0] * card_info[2]) / (1024 * 1024)
        if total_size > 4096: 
            print("SDHC")
        else:
            print("SDSC")
    except:
        print("UNKNOWN")
    try:
        card_info = os.statvfs('/')
        total_size = (card_info[0] * card_info[2]) / (1024 * 1024)
        print("SD Card Size: %dMB" % total_size)
    except:
        print("Could not determine card size")
    listDir(vfs, "/", 0)
    createDir(vfs, "/mydir")
    listDir(vfs, "/", 0)
    removeDir(vfs, "/mydir")
    listDir(vfs, "/", 2)
    writeFile(vfs, "/hello.txt", "Hello ")
    appendFile(vfs, "/hello.txt", "World!\n")
    readFile(vfs, "/hello.txt")
    try:
        deleteFile(vfs, "/foo.txt")
    except:
        pass
    renameFile(vfs, "/hello.txt", "/foo.txt")
    readFile(vfs, "/foo.txt")
    testFileIO(vfs, "/test.txt")
    try:
        card_info = os.statvfs('/')
        total_size = (card_info[0] * card_info[2]) / (1024 * 1024)
        free_size = (card_info[0] * card_info[3]) / (1024 * 1024)
        print("Total space: %dMB" % total_size)
        print("Used space: %dMB" % (total_size - free_size))
    except:
        print("Could not determine space information")

def loop():
    pass

setup()

while True:
    loop()
    time.sleep(1)