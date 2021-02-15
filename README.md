# Onboard Computer System

------

![ocs_screenshot_01](image_files/ocs_screenshot_01.png?raw=true "ocs_screenshot_01")

------

# Current Features #
* Chartplotter
* GRIB weather data visualization
* NMEA multiplexer
* Weather station (barometric pressure / temperature)
* Sunrise & sunset times for current position
* Automatic position logging
* Automatic weather logging
* Automatic data synchronization with a server
* Automatic time synchronization with GPS
* PDF reader
* And more..

# Parts List #
* 12v to 5v converter: LM2596 Buck Step-down Power Converter Module
* Computer: Raspberry Pi 3 Model B+
* Case: Raspberry Pi 3 B+ Case black
* SD: Sandisk microSDXC Ultra 128GB
* Screen: Chalkboard Electronics 15.6" Touchscreen
* GPS: GlobalSat MR-350 S4 + GlobalSat 11-BR305-USB2 (USB adapter)
* AIS: dAISy AIS Receiver
* Temperature sensors: (2x) DS18B20
* Barometric pressure sensor: BMP180
* Keyboard: Logitech K830
* Amplifier: PAM8403 + 3W 4ohm rectangle speaker pair (from ebay) + MPOW ground loop isolator
* Other stuff: USB hub, AIS antenna, junction box, GPIO cables

# UI - Right-click:
* Long-click on the touchscreen acts as a right-click
* Right-click on the desktop for a comprehensive menu

# UI - The main menu is at the top of the screen, with the following buttons:
* OCPN (CTRL+ALT+O) - OpenCPN chartplotter
* GRIB (CTRL+ALT+G) - zyGrib weather data visualization
* LOG (CTRL+ALT+L) - View location history
* WTHR (CTRL+ALT+W) - View weather history
* HDD (CTRL+ALT+H) - PCManFM file manager
* ALRM (CTRL+ALT+A) - Alarm system settings
* CONF (CTRL+ALT+C) - System settings
* OFF - Left click to power off, right-click to reboot

# UI - Under the main menu is the taskbar:
* Single click item to open/minimize
* Right-click item to close

# UI - At the bottom of the screen is the GPS info:
* The first (and last) item is GPS fix [ FX ] means there's a 3D fix, [ NO ] means there's no 3D fix
* TIME - Date and time
* SPD - Speed (in knots)
* COG - Course Above Ground (Shows course based on GPS data (only works when moving))
* LOG - Total distance travelled

# UI - If there's no active windows open:
* UPTIME - System uptime
* SUNRISE - The time of sunrise for current GPS position
* SUNSET - The time of sunset for current GPS position
* BARO - Barometric pressure (in millibar)
* INSIDE - Temperature inside (in celcius)
* OUTSIDE - Temperature outside (in celcius)
* TIME OFFSET - System time offset from UTC
* NAUTICAL TIMEZONE - Current nautical timzone (from GPS coordinates)
* LON - Longitude
* LON - Longitude
* AVG SPD - Total average speed (in knots)

# Usage - Commands:
* System settings: $ ocs-config-curses
* Alarm system settings: $ ocs-alarm-curses
* View data: $ ocs-info-curses
* View location history: $ ocs-location-history-curses
* View weather history: $ ocs-weather-history-curses
* Adjust volume: $ alsamixer
* Start cmus music player: $ cmus
* Start ranger file manager: $ ranger

# Usage - Configuration:
* General configuration: $ ocs-config-curses
* Edit desktop right-click menu: $ nano ~/.config/openbox/menu.xml
* Edit main menu: $ nano ~/.OnboardComputerSystem/OnboardComputerSystem
* Change kplex settings: $ nano .kplex.conf

# Usage - To recieve NMEA data on the local Wi-Fi from the Pi use these settings:
* Protocol: TCP
* IP: 192.168.1.99
* Port: 10110

# Usage - Location & weather history:
* A new entry is added to the location database once every hour if you have moved minimum 50 meters since last entry
* A new entry is added to the weather database once every hour

# Usage - PHP examples:
* Showing realtime data: https://github.com/LASER-WOLF/OnboardComputerSystem/blob/master/example_files/PHP/ocs.php
* Showing location history (requires a Google Maps API key): https://github.com/LASER-WOLF/OnboardComputerSystem/blob/master/example_files/PHP/location.php
* Showing weather history (requires Charts.js from http://www.chartjs.org/): https://github.com/LASER-WOLF/OnboardComputerSystem/blob/master/example_files/PHP/weather.php

# Hardware setup:
* BMP180 wiring diagram: https://github.com/LASER-WOLF/OnboardComputerSystem/blob/master/image_files/ocs_diagram_01_bmp180.png
* DS18B20 wiring diagram: https://github.com/LASER-WOLF/OnboardComputerSystem/blob/master/image_files/ocs_diagram_02_ds18b20.png

# Write the Raspbian image to the SD-card:
* Download the "Raspberry Pi OS Lite" image from https://www.raspberrypi.org/software/operating-systems/
* Download the "Raspberry Pi Imager" from https://www.raspberrypi.org/software/
* Install Raspberry Pi OS to microSD-card
* Insert the microSD-card into the Pi
* Power on the Pi
* Login with the default user "pi" and the password "raspberry"

# Configure raspi-config:
$ sudo raspi-config
* System Options -> S1 Wireless LAN
* System Options -> S2 Audio
* System Options -> S4 Hostname
* Localisation Options -> L3 Keyboard
$ ping google.com

# Perform update:
$ sudo apt-get update
$ sudo apt-get upgrade
$ sudo apt-get install rpi-update
$ sudo rpi-update
$ sudo reboot

# Setup Wi-Fi
$ sudo apt-get install wicd-curses
$ sudo systemctl disable dhcpcd
$ wicd-curses
* Set static IP: 192.168.1.99

# Enable SSH:
$ sudo systemctl enable ssh

# Set timezone to UTC:
$ sudo timedatectl set-timezone UTC

# Change username:
$ sudo adduser admin
$ sudo visudo
* Add the line: admin ALL=(ALL) NOPASSWD: ALL
$ sudo usermod -a -G adm,dialout,cdrom,sudo,audio,video,plugdev,games,users,input,netdev,spi,i2c,gpio admin
$ sudo reboot
* Login with the new user
$ sudo deluser -remove-home pi

# Edit config.txt:
$ sudo nano /boot/config.txt
* Add the line: disable_overscan=1
* Add the line: hdmi_force_hotplug=1
* Add the line: hdmi_group=2
* Add the line: hdmi_mode=81
* Add the line: gpu_mem=128
* Add the line: disable_splash=1
* Add the line: dtoverlay=w1-gpio
* Add the line: dtparam=i2c_arm=on
* Add the line: max_usb_current=1

# Remove Raspberry Pi logos at boot:
$ sudo nano /boot/cmdline.txt
* Add the following at the end of the line: logo.nologo

# Enable long-click on touchscreen as right-click ( from: https://fmirkes.github.io/articles/20190827.html )
$ sudo apt install libevdev2 libevdev-dev
$ git clone https://github.com/PeterCxy/evdev-right-click-emulation.git
$ cd evdev-right-click-emulation
$ make all
$ sudo cp out/evdev-rce /usr/local/bin/
$ sudo chmod +x /usr/local/bin/evdev-rce
$ echo uinput | sudo tee -a /etc/modules
$ sudo nano /etc/udev/rules.d/99-uinput.rules
* Add the line: KERNEL=="uinput", MODE="0660", GROUP="input"
$ sudo udevadm control --reload-rules
$ sudo udevadm trigger
$ cd
$ sudo rm -rf ~/evdev-right-click-emulation/

# Install bluetooth:
$ sudo apt-get install bluetooth bluez blueman pulseaudio-module-bluetooth

# Install GPSd
$ sudo apt-get install gpsd gpsd-clients
$ sudo nano /etc/default/gpsd
* Modify/add the line: START_DAEMON="true"
* Modify/add the line: USBAUTO="true"
* Modify/add the line: DEVICES="/dev/ttyUSB0"
* Modify/add the line: GPSD_OPTIONS="-n"
* Modify/add the line: GPSD_SOCKET="/var/run/gpsd.sock"

# Setup I2C:
$ sudo apt-get install i2c-tools
$ sudo nano /etc/modules
* Add the line: i2c-bcm2708
* Add the line: i2c-dev

# Install Python:
$ sudo apt-get install python3 python3-dev python3-pip python3-gst-1.0
$ pip3 install gps ephem geopy playsound

# Install SQLite3:
$ sudo apt-get install sqlite3

# Install ncurses:
$ sudo apt-get install libncurses5-dev libncursesw5-dev

# Setup the BMP180 barometric pressure sensor:
$ git clone https://github.com/adafruit/Adafruit_Python_BMP.git
$ cd Adafruit_Python_BMP
$ sudo python3 setup.py install
$ cd
$ sudo rm -rf ~/Adafruit_Python_BMP/

# Setup the DS18B20 temperature sensors:
$ sudo modprobe w1-gpio
$ sudo modprobe w1-therm

# Reboot
$ sudo reboot

# Clone the OnboardComputerSystem git repository:
$ sudo apt-get install build-essential git
$ git clone https://github.com/LASER-WOLF/OnboardComputerSystem
$ chmod -R 777 OnboardComputerSystem/
$ cp -r OnboardComputerSystem/ocs_files/.OnboardComputerSystem/ .OnboardComputerSystem/
$ mkdir .OnboardComputerSystem/databases
$ .OnboardComputerSystem/ocs-config-curses.py
* Set time offset (or enable nautical timezone)
* Set temperature sensor inside ID
* Set temperature sensor outside ID
* (get temp sensor ID with the command: "ls /sys/bus/w1/devices")

# Copy apps:
$ cp -r OnboardComputerSystem/ocs_files/Apps/ Apps/

# Copy scripts:
$ cp -r OnboardComputerSystem/ocs_files/Scripts/ Scripts/

# Copy documents:
$ cp -r OnboardComputerSystem/ocs_files/Documents/ Documents/

# Setup NTP to syncronize with GPSd:
$ sudo apt-get install ntp
$ sudo nano /etc/init.d/ntp
* Modify the line: "RUNASUSER=ntp" -> "RUNASUSER=root"
$ sudo nano /etc/ntp.conf
* Find the line: pool 3.debian.pool.ntp.org iburst
* Add the line (under the previous line): server 127.127.28.0
* Add the line (under the previous line): fudge 127.127.28.0 refid GPS
* Add the line (under the previous line): server 127.127.28.1 prefer
* Add the line (under the previous line): fudge 127.127.28.1 refid PPS

# Install Kplex (NMEA multiplexer):
$ cp OnboardComputerSystem/config_files/.kplex.conf .kplex.conf
$ git clone https://github.com/stripydog/kplex
$ cd kplex
$ make
$ sudo make install
$ cd
$ rm -rf kplex/

# Install urxvt (terminal emulator):
$ cp OnboardComputerSystem/config_files/.bash_aliases .bash_aliases
$ cp OnboardComputerSystem/config_files/.Xresources .Xresources
$ sudo apt-get install rxvt-unicode

# Install Xorg (display server):
$ sudo apt-get install xorg

# Install Openbox (window manager):
$ mkdir .config
$ cp -r OnboardComputerSystem/config_files/.config/openbox/ .config/openbox/
$ cp OnboardComputerSystem/config_files/.config/user-dirs.dirs .config/user-dirs.dirs
$ sudo apt-get install openbox

# Install LightDM (display manager):
$ sudo apt-get install lightdm
$ sudo nano /etc/lightdm/lightdm.conf
* Uncomment the following line (under "[Seat:*]"): autologin-user=
* Change it to: autologin-user=admin
$ sudo systemctl enable lightdm.service

# Install tint2 (taskbar):
$ cp -r OnboardComputerSystem/config_files/.config/tint2/ .config/tint2/
$ sudo apt-get install tint2

# Install lemonbar (statusbar):
# (lemonbar doesn't have xft font support so we'll be using a fork with xft support)
$ sudo apt-get install libxcb-xinerama0-dev libxcb-randr0-dev libxft-dev libx11-xcb-dev
$ git clone https://github.com/krypt-n/bar
$ cd bar
$ make
$ sudo make install
$ cd
$ sudo rm -rf ~/bar/

# Install Conky (system monitor):
$ sudo apt-get install conky
$ cp OnboardComputerSystem/config_files/.conkyrc .conkyrc
$ touch .datatext

# Install font, theme and icons:
$ cp -r OnboardComputerSystem/theme_files/.fonts/ .fonts/
$ cp -r OnboardComputerSystem/theme_files/.themes/ .themes/
$ cp -r OnboardComputerSystem/theme_files/.icons/ .icons/
$ cd .icons
$ tar xvzf Faenza.tar.gz
$ rm Faenza.tar.gz
$ cd
$ cp OnboardComputerSystem/config_files/.gtkrc-2.0 .gtkrc-2.0
$ cp -r OnboardComputerSystem/config_files/.config/gtk-3.0/ .config/gtk-3.0/

# Install unclutter (hides the mouse when idle):
$ sudo apt-get install unclutter

# Install x11vnc (vnc server):
$ sudo apt-get install x11vnc

# Reboot:
$ sudo reboot

# Install htop (process monitor):
$ sudo apt-get install htop

# Install slurm (network load monitor):
$ sudo apt-get install slurm

# Install ranger (console based file manager):
$ sudo apt-get install ranger

# Install cmus (music player):
$ mkdir Music
$ cp -r OnboardComputerSystem/config_files/.cmus/ .cmus/
$ cp -r OnboardComputerSystem/ocs_files/Radio/ Radio/
$ sudo apt-get install cmus

# (optional) Install cmusfm (last.fm scrobbler):
$ sudo apt-get install autoconf libssl-dev libcurl4-openssl-dev
$ git clone https://github.com/Arkq/cmusfm
$ cd cmusfm
$ autoreconf --install
$ mkdir build && cd build
$ ../configure
$ make
$ sudo make install
$ cd
$ rm -rf ~/cmusfm/
$ cmusfm init

# Install scrot (take screenshots):
$ sudo apt-get install scrot

# Install feh (image viewer):
$ sudo apt-get install feh

# Install PCManFM (file manager)
$ mkdir -p ~/.config/pcmanfm/default/
$ cp OnboardComputerSystem/config_files/.config/pcmanfm/default/pcmanfm.conf .config/pcmanfm/default/pcmanfm.conf
$ cp -r OnboardComputerSystem/config_files/.config/libfm/ .config/libfm/
$ sudo apt-get install pcmanfm

# Install Chromium (web browser):
$ sudo apt-get install chromium-browser

# Install FoxtrotGPS (non-maritime maps):
$ mkdir -p ~/.gconf/apps/foxtrotgps
$ sudo apt-get install foxtrotgps
$ cp OnboardComputerSystem/config_files/.gconf/apps/foxtrotgps/%gconf.xml .gconf/apps/foxtrotgps/%gconf.xml

# Install Okular (pdf reader):
$ mkdir -p ~/.kde/share/config
$ cp OnboardComputerSystem/config_files/.kde/share/config/okularrc .kde/share/config/okularrc
$ cp OnboardComputerSystem/config_files/.kde/share/config/okularpartrc .kde/share/config/okularpartrc
$ sudo apt-get install okular

# Setup JTides:
$ sudo apt-get install openjdk-8-jdk

# Install zyGrib (weather data visualization):
$ mkdir GRIB
$ sudo apt-get install build-essential g++ make libqt4-dev libbz2-dev zlib1g-dev libproj-dev libnova-dev nettle-dev
$ tar xvzf OnboardComputerSystem/other_files/zyGrib-7.0.0.tgz
$ cd zyGrib-7.0.0
$ make
$ sudo make install
$ cd
$ rm -rf ~/zyGrib-7.0.0/
$ mkdir -p ~/.zygrib/config/
$ cp OnboardComputerSystem/config_files/zygrib.ini .zygrib/config/zygrib.ini

# Install OpenCPN:
$ mkdir Charts
$ sudo apt-get install build-essential cmake gettext git-core gpsd gpsd-clients libgps-dev wx-common libwxgtk3.0-dev libglu1-mesa-dev libgtk2.0-dev libgtk-3-dev wx3.0-headers libbz2-dev libtinyxml-dev libportaudio2 portaudio19-dev libcurl4-openssl-dev libexpat1-dev libcairo2-dev libsqlite3-dev libarchive-dev libsndfile1-dev liblzma-dev libexif-dev libelf-dev libwxgtk-webview3.0-gtk3-dev
$ git clone git://github.com/OpenCPN/OpenCPN.git
$ cd OpenCPN
$ mkdir build
$ cd build
$ cmake ../
$ make
$ sudo make install
$ cd
$ rm -rf ~/OpenCPN/

# Setup PiSNES (SNES emulator):
$ sudo apt-get install libsdl1.2debian

# Install ScummVM (emulator):
$ sudo apt-get install scummvm
$ mkdir ScummVM

# Install Nethack (video game):
$ sudo apt-get install nethack-console
$ cp OnboardComputerSystem/config_files/.nethackrc .nethackrc

# (optional) If experiencing problems during git clone of Cataclysm DDA try the following:
$ nano .bashrc
* Add the line: export GIT_TRACE_PACKET=1
* Add the line: export GIT_TRACE=1
* Add the line: export GIT_CURL_VERBOSE=1

# Install Cataclysm DDA (video game):
$ sudo apt-get install libglib2.0-dev ccache clang liblua5.2-0 libncurses5-dev libncursesw5-dev build-essential astyle
$ git clone https://github.com/CleverRaven/Cataclysm-DDA.git
$ cd Cataclysm-DDA
$ make clean
$ make CLAN=1 CCACHE=1 RELEASE=1
$ cd
$ mv Cataclysm-DDA/ Apps/Cataclysm-DDA/

# Remove the OnboardComputerSystem folder (we have copied everything we need from it):
$ rm -rf ~/OnboardComputerSystem/

# Reboot:
$ sudo reboot

# Additional setup:
* Copy all your charts to the ~/Charts folder
* Copy all your documents to the "~/Documents" folder
* (check out https://www.reddit.com/r/sailing/comments/3hwagp/a_collection_of_free_useful_sailing_maritime/ for a collection of free maritime documents)
* Copy all your music to the "~/Music" folder
* Copy all your SNES roms to the ~/Apps/pisnes/roms/ folder
* Copy all your ScummVM games to the ~/ScummVM folder

------

![ocs_screenshot_02](image_files/ocs_screenshot_02.png?raw=true "ocs_screenshot_02")

------

![ocs_screenshot_03](image_files/ocs_screenshot_03.png?raw=true "ocs_screenshot_03")

------

![ocs_screenshot_04](image_files/ocs_screenshot_04.png?raw=true "ocs_screenshot_04")

------

![ocs_screenshot_05](image_files/ocs_screenshot_05.png?raw=true "ocs_screenshot_05")

------

![ocs_screenshot_06](image_files/ocs_screenshot_06.png?raw=true "ocs_screenshot_06")

------

![ocs_screenshot_07](image_files/ocs_screenshot_07.png?raw=true "ocs_screenshot_07")

------

![ocs_screenshot_08](image_files/ocs_screenshot_08.png?raw=true "ocs_screenshot_08")

------

![ocs_screenshot_09](image_files/ocs_screenshot_09.png?raw=true "ocs_screenshot_09")

------

![ocs_screenshot_10](image_files/ocs_screenshot_10.png?raw=true "ocs_screenshot_10")

------

![ocs_screenshot_11](image_files/ocs_screenshot_11.png?raw=true "ocs_screenshot_11")

------

![ocs_screenshot_12](image_files/ocs_screenshot_12.png?raw=true "ocs_screenshot_12")

------

![ocs_screenshot_13](image_files/ocs_screenshot_13.png?raw=true "ocs_screenshot_13")

------

![ocs_diagram_01_bmp180](image_files/ocs_diagram_01_bmp180.png?raw=true "ocs_diagram_01_bmp180")

------

![ocs_diagram_02_ds18b20](image_files/ocs_diagram_02_ds18b20.png?raw=true "ocs_diagram_02_ds18b20")
