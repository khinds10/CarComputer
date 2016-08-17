#!/usr/bin/python
# Kevin Hinds http://www.kevinhinds.com
# License: GPL 2.0
import time, json, random
import Adafruit_CharLCD as LCD
import includes.data as data
lcd = LCD.Adafruit_CharLCDPlate()

# map special HEX characters for advanced display information
# http://www.quinapalus.com/hd44780udg.html
lcd.create_char(1, [24,24,7,4,6,4,4,0])
lcd.create_char(2, [0,4,14,21,4,4,4,4])
lcd.create_char(3, [0,0,0,4,0,0,0,0])

def setLCDText(text):
    """clear and set new text on LCD screen"""
    lcd.clear()
    lcd.message(text)

# show current GPS status on small screen
while True:
    try:

        # get current location from GPS
        currentLocationInfo = data.getCurrentLatLong()
        completeLocationInfo = data.getJSONFromDataFile('location.data')

        # show GPS fixed position info
        lcd.set_color(1, 0, 0)    
        setLCDText("<GPS FIX> WSW"+"\nSPD:" + str(int(completeLocationInfo['speed'])) +" ALT:" + str(int(completeLocationInfo['altitude'])))

    except (Exception):
    
        # GPS not fixed wait 5 seconds
        lcd.set_color(1, 1, 0) 
        setLCDText("Waiting for GPS Satellite")
    
    time.sleep(5)