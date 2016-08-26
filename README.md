#CarComputer - GPS & Weather Module for you vehicle

####Flashing RaspberriPi Hard Disk / Install Required Software (Using Ubuntu Linux)

Download "RASPBIAN JESSIE FULL VERSION"
https://www.raspberrypi.org/downloads/raspbian/

**Create your new hard disk for DashboardPI**
>Insert the microSD to your computer via USB adapter and create the disk image using the `dd` command
>
> Locate your inserted microSD card via the `df -h` command, unmount it and create the disk image with the disk copy `dd` command
> 
> $ `df -h`
> */dev/sdb1       7.4G   32K  7.4G   1% /media/XXX/1234-5678*
> 
> $ `umount /dev/sdb1`
> 
> **Caution: be sure the command is completely accurate, you can damage other disks with this command**
> 
> *if=location of RASPBIAN JESSIE FULL VERSION image file*
> *of=location of your microSD card*
> 
> $ `sudo dd bs=4M if=/path/to/raspbian-jessie.img of=/dev/sdb`
> *(note: in this case, it's /dev/sdb, /dev/sdb1 was an existing factory partition on the microSD)*

**Setting up your RaspberriPi**

*Insert your new microSD card to the raspberrypi and power it on with a monitor connected to the HDMI port*

Login
> user: **pi**
> pass: **raspberry**

Change your account password for security (from terminal)
>`sudo passwd pi`

Enable RaspberriPi Advanced Options (from terminal)
>`sudo raspi-config`

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

**Enable the English/US Keyboard**

>`sudo nano /etc/default/keyboard`

> Change the following line:
>`XKBLAYOUT="us"`

**Reboot PI for Keyboard layout changes / file system resizing to take effect**
>$ `sudo shutdown -r now`

**Auto-Connect to your WiFi**

>`sudo nano /etc/wpa_supplicant/wpa_supplicant.conf`

Add the following lines to have your raspberrypi automatically connect to your home WiFi
*(if your wireless network is named "linksys" for example, in the following example)*

	network={
	   ssid="linksys"
	   psk="WIRELESS PASSWORD HERE"
	}

**Reboot PI to connect to WiFi network**

>$ `sudo shutdown -r now`
>
>Now that your PI is finally on the local network, you can login remotely to it via SSH.
>But first you need to get the IP address it currently has.
>
>$ `ifconfig`
>*Look for "inet addr: 192.168.XXX.XXX" in the following command's output for your PI's IP Address*

**Go to another machine and login to your raspberrypi via ssh**

> $ `ssh pi@192.168.XXX.XXX`

**Start Installing required packages**

>$ `sudo apt-get update && sudo apt-get upgrade`
>
>$ `sudo apt-get install build-essential git gpsd gpsd-clients i2c-tools python3 python3-pip python-dev python-gps python-imaging python-pip python-smbus rpi.gpio vim`
>
>$ `sudo pip install RPi.GPIO`

**Setup the simple directory `l` command [optional]**

>`vi ~/.bashrc`
>
>*add the following line:*
>
>`alias l='ls -lh'`
>
>`source ~/.bashrc`

**Fix VIM default syntax highlighting [optional]**

>`sudo vi  /etc/vim/vimrc`
>
>uncomment the following line:
>
>_syntax on_

####16x2 plate installation

`sudo i2cdetect -y 1`
> the 16x2 plate should be at address 20

`git clone https://github.com/adafruit/Adafruit_Python_CharLCD.git`

`cd Adafruit_Python_CharLCD`

`sudo python setup.py install`

`cd examples`

`python char_lcd_plate.py`

> the LCD display should be showing a random assortment of colors and symbols

####DHT11 Install

`cd ~`

`git clone https://github.com/adafruit/Adafruit_Python_DHT.git`

`cd Adafruit_Python_DHT/`

`sudo python setup.py install`

`sudo python ez_setup.py`

`cd examples/`

`vi simpletest.py`

Change the following line:

> sensor = Adafruit_DHT.DHT11

Comment the line out

> pin = 'P8_11'

Uncomment the line and change the pin number to 16

> pin = 16

Run the test

`python simpletest.py`

> You should see a metric reading of Temp and Humidity displayed on the command line.

####GPS Module Install

Make sure the command is working

`cgps -s`

Make sure the GPS unit is setup to connect via USB connection

`sudo gpsd /dev/ttyAMA0 -F /var/run/gpsd.sock`

`sudo gpsd /dev/ttyUSB0 -F /var/run/gpsd.sock`

`sudo systemctl stop gpsd.socket`

`sudo killall gpsd`

Verify all connected USB devices

`sudo lsusb`

####Setup and Run the scripts

`cd ~`

`git clone https://github.com/khinds10/CarComputer.git`

###Install driving monitoring tools & DB Logging

`sudo apt-get install ifstat memcached python-memcache postgresql postgresql-contrib python-psycopg2`

`sudo vi /etc/postgresql/9.4/main/pg_hba.conf`

> Add the following line to the end of the file:
>
>local all pi password

`sudo -i -u postgres`

`psql`

`create role pi password 'password here';`

`alter role pi login;`

`alter role pi superuser;`

`\du`

>(you should see your PI user with the permissions granted)

`create database driving_statistics;`

`\q`

`exit`

`psql -d driving_statistics`

Run the following queries:

>CREATE TABLE driving\_stats (
> id serial,
> time timestamp without time zone NOT NULL,
> new\_trip\_start timestamp without time zone NULL,
> gps\_latitude double precision	,
> gps\_longitude double precision,
> gps\_altitude real,
> gps\_speed real,
> gps\_climb real,
> gps\_track real,
> locale\_address text,
> locale\_area text,
> locale\_city text,
> locale\_county text,
> locale\_country text,
> locale\_zipcode text,
> inside\_temp real,
> inside\_hmidty real,
> weather\_time timestamp,
> weather\_summary text,
> weather\_icon text,
> weather\_apparentTemperature real,
> weather\_humidity real,
> weather\_precipIntensity real,
> weather\_precipProbability real,
> weather\_windSpeed real
>);
>CREATE UNIQUE INDEX time_idx ON driving\_stats (time);

###Setup the scripts to run at boot

`crontab -e`

Add the following lines 

`@reboot /bin/sleep 10; nohup python /home/pi/CarComputer/computer/GPS.py > /home/pi/CarComputer/computer/GPS.log 2>&1`
`@reboot /bin/sleep 30; nohup python /home/pi/CarComputer/computer/Display.py > /home/pi/CarComputer/computer/Display.log 2>&1`
`@reboot /bin/sleep 30; nohup python /home/pi/CarComputer/computer/Locale.py > /home/pi/CarComputer/computer/Locale.log 2>&1`
`@reboot /bin/sleep 30; nohup python /home/pi/CarComputer/computer/Logger.py > /home/pi/CarComputer/computer/Logger.log 2>&1`
`@reboot /bin/sleep 30; nohup python /home/pi/CarComputer/computer/Stats.py > /home/pi/CarComputer/computer/Stats.log 2>&1`
`@reboot /bin/sleep 30; nohup python /home/pi/CarComputer/computer/Temp.py > /home/pi/CarComputer/computer/Temp.log 2>&1`
`@reboot /bin/sleep 30; nohup python /home/pi/CarComputer/computer/Weather.py > /home/pi/CarComputer/computer/Weather.log 2>&1`


###Install the local driving statistics website [http://localhost]

`sudo apt-get update && sudo apt-get upgrade -y`

`sudo apt-get install apache2`

Enable Python CGI Scripting from our own project in http://localhost

`sudo vi /etc/apache2/sites-enabled/000-default.conf`

**Change to the following**

<VirtualHost *:80>
        ServerAdmin webmaster@localhost
        DocumentRoot /var/www/html
        ErrorLog ${APACHE_LOG_DIR}/error.log
        CustomLog ${APACHE_LOG_DIR}/access.log combined
    <Directory /var/www/html>
        Options +ExecCGI
        AddHandler cgi-script .py
    </Directory>
</VirtualHost>

### Add the symlink to the project in the Apache2 webroot

`cd /var/www/`
`sudo chmod 777 html`
`cd /var/www/html`
`ln -s /home/pi/CarComputer/computer/`
`cd /home/pi/CarComputer/computer/`
`chmod +x *.py`
`sudo a2enmod cgi`
`sudo service apache2 restart`

You can now visit the local HTTP site to get driving data [http://localhost/computer/TripStats.py]

### Get the small HDMI screen program working in desktop view

Disable Xsession from blanking

`sudo vi /etc/kbd/config`
BLANK_TIME=0

`sudo vi /etc/xdg/lxsession/LXDE/autostart`
remove
> @xscreensaver -no-splash
    
add: 
> @xset s noblank
> @xset s off
> @xset -dpms

Add the default browser to run in kiosk mode on system startup

`vi ~/.config/lxsession/LXDE-pi/autostart`

add the line
> @epiphany-browser -a --profile /home/pi/.config http://localhost/computer/trip-stats/

remove the screensave line
> @xscreensaver -no-splash

Update for HDMI to run in 800x480

`/boot/config.txt`

add the following line:
`hdmi_cvt=800 480 60 6 0 0 0`
