# CarComputer - GPS & Weather Module for your vehicle

![Car Computer](https://raw.githubusercontent.com/khinds10/CarComputer/master/construction/CarComputer.png "Car Computer")

## Flashing Raspberry Pi Hard Disk / Install required software (using Ubuntu Linux)

Download "RASPBIAN JESSIE LITE VERSION" from https://www.raspberrypi.org/downloads/raspbian/

### Create your new hard disk for DashboardPI

Insert the microSD to your computer via USB adapter and create the disk image using the `dd` command:

Locate your inserted microSD card via the `df -h` command, unmount it and create the disk image with the disk copy `dd` command

```
$ df -h
/dev/sdb1       7.4G   32K  7.4G   1% /media/XXX/1234-5678*
$ umount /dev/sdb1
```

**Caution: be sure the command is completely accurate, you can damage other disks with this command**

* `if` = location of RASPBIAN JESSIE FULL VERSION image file
* `of` = location of your microSD card

```
$ sudo dd bs=4M if=/path/to/raspbian-jessie-lite.img of=/dev/sdX
```

*(note: in this case, it's /dev/sdb, /dev/sdb1 was an existing factory partition on the microSD)*

### Setting up your Raspberry Pi

Insert your new microSD card to the Raspberry Pi and power it on with a monitor connected to the HDMI port.

First login: user: **pi**, password: **raspberry**.

Change your account password for security (from terminal):

```shell
sudo passwd pi
```

Enable Raspberry Pi Advanced Options (from terminal):

```shell
sudo raspi-config
```

Choose:
`1 Expand File System`

`9 Advanced Options`
>`A2 Hostname`
>*change it to "CarComputer"*
>
>`A4 SSH`
>*Enable SSH Server*
>
>`A7 I2C`
>*Enable i2c interface*

### Enable the English/US Keyboard

```shell
sudo nano /etc/default/keyboard
```

Change the following line:
```
XKBLAYOUT="us"
```

### Reboot PI for Keyboard layout changes / file system resizing to take effect

```
$ sudo shutdown -r now
```

### Auto-Connect to your Wi-Fi

```shell
sudo nano /etc/wpa_supplicant/wpa_supplicant.conf
```

Add the following lines to have your Raspberry Pi automatically connect to your home Wi-Fi:
*(if your wireless network is named "linksys" for example, in the following example)*

```
	network={
	   ssid="linksys"
	   psk="WIRELESS PASSWORD HERE"
	}
```

### Reboot Raspberry Pi to connect to WiFi network

```
sudo shutdown -r now
```

Now that your PI is finally on the local network, you can login remotely to it via SSH.
But first you need to get the IP address it currently has.

```shell
ifconfig
```

*Look for "inet addr: 192.168.XXX.XXX" in the following command's output for your PI's IP Address*

#### Go to another machine and login to your Raspberry Pi via ssh

```shell
ssh pi@192.168.XXX.XXX
```

#### Install required packages

```shell
sudo apt-get update && sudo apt-get upgrade
sudo apt-get install build-essential git gpsd gpsd-clients i2c-tools libi2c-dev python3 python3-pip python-dev python-gps python-imaging python-pip python-smbus rpi.gpio vim python-psutil
sudo pip install RPi.GPIO
```

#### Update local timezone settings

```shell
sudo dpkg-reconfigure tzdata
```

select your timezone using the interface.

#### Setup the simple directory `l` command [optional]

```shell
vi ~/.bashrc
```

add the following line:

```shell
alias l='ls -lh'
```

Apply now:

```shell
source ~/.bashrc
```

#### Fix VIM default syntax highlighting [optional]

```shell
sudo vi  /etc/vim/vimrc
```

uncomment the following line:

```ini
syntax on
```

### Supplies needed

2" 320x240 TFT LCD Digole Display

![Digole Display](https://raw.githubusercontent.com/khinds10/CarComputer/master/construction/Digole-Display.png "Digole Display")

SSD1306 Display

![SSD1306](https://raw.githubusercontent.com/khinds10/CarComputer/master/construction/SSD1306-Display.jpg "SSD1306")

DHT11 Humidistat

![DHT11](https://raw.githubusercontent.com/khinds10/CarComputer/master/construction/DHT11.jpg "DHT11")

Raspberry Pi Zero

![Raspberry Pi Zero](https://raw.githubusercontent.com/khinds10/CarComputer/master/construction/PiZero.jpg "Raspberry Pi Zero")

Momentary Push Button (x2)

![Push Button Switch](https://raw.githubusercontent.com/khinds10/CarComputer/master/construction/PushButton.jpg "Push Button Switch")

LEDs (RED / Blue / Orange / Yellow)

![LED](https://raw.githubusercontent.com/khinds10/CarComputer/master/construction/LED.jpg "LED")

## Print the Enclosure

Using the provided STL files in the enclosure/ folder print the front and back panels as well as the enclosure.

Hot glue the push button switches, the LEDs and both displays as shown:

![Assemble1](https://raw.githubusercontent.com/khinds10/CarComputer/master/construction/Assemble1.jpg "Assemble1")

![Assemble2](https://raw.githubusercontent.com/khinds10/CarComputer/master/construction/Assemble2.jpg "Assemble2")


## Building the CarComputer

This is the wiring for the unit

![Schematic](https://raw.githubusercontent.com/khinds10/CarComputer/master/construction/schematic.png "Schematic")

#### Connect the following Devices the pins on the  Pi Zero

```
Digole:         3v / GND / SDA / SCL
SSD1306:        3v / GND / SDA / SCL
DHT11:          5v / GPIO 16 (36) / GND
Push Button 1:  GND / GPIO 18 (24)
Push Button 2:  GND / GPIO 11 (17)
Power LED:      330ohm resistor - 3v / GND
```

LEDs:

* LED Blue:       330ohm resistor - GPIO 27 (13) / GND (the Blue LED, for pin 13 will be for if the internet is connected or not)
* LED Orange:     330ohm resistor - GPIO 22 (15) / GND
* LED Yellow:     330ohm resistor - GPIO 23 (16) / GND (Yellow LED, pin 15 will be for if the GPS is currently tracking your location or not)

### Connect the USB module to Raspberry Pi HW UART

Using HW UART for the GPS module requires the following to free the UART connection up on your Pi.

* "Cross"-Connect the TX and RX pins from the GPS module to the RPi TX (GPIO 14/8 pin) and RX (GPIO 15/10 pin) -- [TX goes to RX on the device and vice versa.]
* Connect RPi 5V to the VIN pin and the GPS module GND pin to an available RPi GND pin.

### Final assembly

The following shows the internal devices wired before the enclosure is screwed shut on each corner front and back with small screws.

I've used very long speaker wire to allow for the humidistat to sit in the car away from the direct sun for an accurate reading.

![Assemble3](https://raw.githubusercontent.com/khinds10/CarComputer/master/construction/Assemble3.jpg "Assemble3")

Note: I've wrapped the wireless USB adapter in felt tape to have it avoid rattling while driving inside the enclosure.

![Assemble4](https://raw.githubusercontent.com/khinds10/CarComputer/master/construction/Assemble4.jpg "Assemble4")


#### Configure your Pi to use the GPS Module on UART

```shell
sudo vi /boot/cmdline.txt
```

Change:

```
dwc_otg.lpm_enable=0 console=ttyAMA0,115200 kgdboc=ttyAMA0,115200 console=tty1 root=/dev/mmcblk0p2 rootfstype=ext4 elevator=deadline rootwait
```
to:
```
dwc_otg.lpm_enable=0 console=tty1 root=/dev/mmcblk0p2 rootfstype=ext4 elevator=deadline rootwait
```
(e.g., remove console=ttyAMA0,115200 and if there, kgdboc=ttyAMA0,115200)

Note: you might see `console=serial0,115200` or `console=ttyS0,115200` and should remove those parts of the line if present.

Run the following commands:

```shell
sudo systemctl stop serial-getty@ttyAMA0.service
sudo systemctl disable serial-getty@ttyAMA0.service
```

#### GPS module install

For testing force your USB device to connect to gpsd

```shell
sudo gpsd /dev/ttyAMA0 -F /var/run/gpsd.sock
sudo systemctl stop gpsd.socket
sudo killall gpsd
sudo dpkg-reconfigure gpsd
sudo vi /etc/default/gpsd
```

Default settings for gpsd:

```shell
START_DAEMON="true"
GPSD_OPTIONS="-n"
DEVICES="/dev/ttyAMA0"
USBAUTO="false"
GPSD_SOCKET="/var/run/gpsd.sock"
```

Make sure the command is working

`cgps -s`

#### DHT11 Install

```shell
cd ~
git clone https://github.com/adafruit/Adafruit_Python_DHT.git
cd Adafruit_Python_DHT/
sudo python setup.py install
sudo python ez_setup.py
cd examples/
vi simpletest.py
```

Change the following line:

```shell
sensor = Adafruit_DHT.DHT11
```

Comment the line out

```shell
pin = 'P8_11'
```

Uncomment the line and change the pin number to 16

```shell
pin = 16
```

Run the test:

```shell
python simpletest.py
```

You should see a metric reading of Temp and Humidity displayed on the command line.

### SSD1306 Display Driver

Download and install drivers for ssd1306 display:

```shell
sudo apt-get install i2c-tools python-smbus python-pip ifstat git python-imaging
git clone https://github.com/rm-hull/ssd1306.git
cd ssd1306
sudo python setup.py install
sudo pip install pillow
```

#### Setup and Run the scripts

```shell
cd ~
git clone https://github.com/khinds10/CarComputer.git
```

### Install driving monitoring tools & DB Logging

```shell
sudo apt-get install ifstat memcached python-memcache postgresql postgresql-contrib python-psycopg2
sudo vi /etc/postgresql/9.4/main/pg_hba.conf
```

Add the following line to the end of the file:

```
local all pi password
```

```shell
sudo -i -u postgres
psql
```

```sql
create role pi password 'password here';
alter role pi login;
alter role pi superuser;
\du
```

(you should see your PI user with the permissions granted)

```sql
create database driving_statistics;
\q
exit
psql -d driving_statistics
```

Run the following queries:

```sql
CREATE TABLE driving_stats (
 id serial,
 time timestamp without time zone NOT NULL,
 new_trip_start timestamp without time zone NULL,
 gps_latitude double precision,
 gps_longitude double precision,
 gps_altitude real,
 gps_speed real,
 gps_climb real,
 gps_track real,
 locale_address text,
 locale_area text,
 locale_city text,
 locale_county text,
 locale_country text,
 locale_zipcode text,
 inside_temp real,
 inside_hmidty real,
 weather_time timestamp,
 weather_summary text,
 weather_icon text,
 weather_apparentTemperature real,
 weather_humidity real,
 weather_precipIntensity real,
 weather_precipProbability real,
 weather_windSpeed real
);
CREATE UNIQUE INDEX time_idx ON driving_stats (time);
```

### Hack required to get GPSD working with UART connection on reboot

```shell
sudo su
crontab -e
```

```cron
# m h  dom mon dow   command
@reboot /bin/sleep 5; killall gpsd
@reboot /bin/sleep 10; /usr/sbin/gpsd /dev/ttyAMA0 -F /var/run/gpsd.sock
```

### Create the logs folder for the data to be saved

```shell
mkdir /home/pi/CarComputer/computer/logs
```

### Setup the scripts to run at boot

```shell
crontab -e
```

Add the following lines:

```cron
@reboot /bin/sleep 15; nohup python /home/pi/CarComputer/computer/GPS.py > /home/pi/CarComputer/computer/GPS.log 2>&1
@reboot /bin/sleep 15; nohup python /home/pi/CarComputer/computer/Indicators.py > /home/pi/CarComputer/computer/Indicators.log 2>&1
@reboot /bin/sleep 20; nohup python /home/pi/CarComputer/computer/Button.py > /home/pi/CarComputer/computer/Button.log 2>&1
@reboot /bin/sleep 20; nohup python /home/pi/CarComputer/computer/Compass.py > /home/pi/CarComputer/computer/Compass.log 2>&1
@reboot /bin/sleep 20; nohup python /home/pi/CarComputer/computer/Locale.py > /home/pi/CarComputer/computer/Locale.log 2>&1
@reboot /bin/sleep 20; nohup python /home/pi/CarComputer/computer/Temp.py > /home/pi/CarComputer/computer/Temp.log 2>&1
@reboot /bin/sleep 20; nohup python /home/pi/CarComputer/computer/Weather.py > /home/pi/CarComputer/computer/Weather.log 2>&1
@reboot /bin/sleep 20; nohup python /home/pi/CarComputer/computer/Stats.py > /home/pi/CarComputer/computer/Stats.log 2>&1
@reboot /bin/sleep 20; nohup python /home/pi/CarComputer/computer/Logger.py > /home/pi/CarComputer/computer/Logger.log 2>&1
@reboot /bin/sleep 20; nohup python /home/pi/CarComputer/computer/Digole.py > /home/pi/CarComputer/computer/Digole.log 2>&1
```

### Finished and powered on!

![Assembly Powered](https://raw.githubusercontent.com/khinds10/CarComputer/master/construction/Assemble-Powered.jpg "Assembly Powered")

### Mounting inside your vehicle

* Mount on Dash

![Car Mount](https://raw.githubusercontent.com/khinds10/CarComputer/master/construction/Car-Mount.jpg "Car Mount")

* Mount Humidistat away from direct Sun

![Humidistat Mount](https://raw.githubusercontent.com/khinds10/CarComputer/master/construction/Humidistat-Mount.jpg "Humidistat Mount")

* Reboot your Raspberry Pi and you should be ready for driving!
