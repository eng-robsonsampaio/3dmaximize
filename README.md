# 3dmaximize

# Basic libraries

## Update apt-get
    sudo apt-get update

## Install pip3 (case you already have it, skip this step)
    sudo apt-get install -y python3-pip

# Config bluetooth on raspiberry pi

## Install dependencies
    sudo apt-get install -y libusb-dev libdbus-1-dev libglib2.0-dev libudev-dev libical-dev libreadline-dev libbluetooth-dev

# Install the necessary additional packages
    sudo apt install -y bluetooth pi-bluetooth bluez

## Install pybluez
    sudo pip3 install pybluez

# Configuring the bluetooth service

## Configure the bluetooth service
    sudo nano /etc/systemd/system/dbus-org.bluez.service

## Edit the file with the following line
    ExecStart=/usr/lib/bluetooth/bluetoothd -C

## Insert the following line to register a serial port service
    ExecStartPost=/usr/bin/sdptool add SP

    Save the file and exit [ctrl+o] to save and [ctrl+x] to exit

## To reload the file run:
    systemctl daemon-reload

## Restart the bluetooth
    systemctl restart bluetooth

# Discoverable mode

## Run the following commands to able to pair and send/receive data
    sudo bluetoothctl

    [bluetooth]# 
    [bluetooth]# power on
    [bluetooth]# discoverable on
    [bluetooth]# pairable on
    [bluetooth]# quit

# Setting up Obex FTP to send files over bluetooth

## Install Obex FTP
    sudo apt-get install -y obexftp

## Check if the installation was sucessed
    sudo apt-cache show obexftp

# Extra commands

## Set up bluez service
    systemctl status bluetooth

## Command to start bluetooth
    sudo systemctl start bluetooth

## Commnad to stop bluetooth
    sudo systemctl stop bluetooth

## Command to enable bluetooth at boot
    sudo systemctl enable bluetooth

## Command to disable bluetooth at boot
    sudo systemctl disable bluetooth

## Command to config bluetooth
    sudo bluetoothctl

## Run help to see a list of all commands
    [bluetooth]# help

## Enable discovering by running
    [bluetooth]# discoverable on

# Configuring audio in raspberry pi

## Set USB Audio as Default Audio Device
    sudo nano /usr/share/alsa/alsa.conf

## Change the value of the following lines
    defaults.ctl.card 0
    defaults.pcm.card 0

    defaults.ctl.card 1
    defaults.pcm.card 1

Save the file and exit [ctrl+o] to save and [ctrl+x] to exit

## Also change the asound.conf with sudo (if not created then create it)
    sudo nano /etc/asound.conf
    
    pcm.!default {
        type hw
        card 1
    }

    ctl.!default {
        type hw
        card 1
    }


## Install pyaudio
    sudo apt-get install -y python3-pyaudio

## Check the alsamixer and rejust the mic and volume gain if you will
    alsamixer

## Do the same with sudo
    sudo alsamixer

## Install pulseaudio (this will take a while)
    sudo apt-get install -y pulseaudio
    sudo apt-get purge portaudio19-dev

# GPio Library

## Install RPi.GPio

    sudo apt-get install -y python3-dev python3-rpi.gpio
