#!/usr/bin/python
# Kevin Hinds http://www.kevinhinds.com
# License: GPL 2.0
import time, json, random
import Adafruit_CharLCD as LCD
import includes.data as data
lcd = LCD.Adafruit_CharLCDPlate()

# map special HEX characters for advanced display information
# http://www.quinapalus.com/hd44780udg.html

# FT symbol
lcd.create_char(1, [0,31,18,26,18,18,0,0])

# degrees F
lcd.create_char(2, [24,24,7,4,6,4,4,0]) 

# separator
lcd.create_char(3, [	0,0,0,4,0,0,0,0]) 

#N
lcd.create_char(5, [4,14,21,4,4,4,0,0])

#E
lcd.create_char(6, [0,4,2,31,2,4,0,0])

#S
lcd.create_char(7, [0,0,4,4,21,14,4,0])

#W
lcd.create_char(8, [0,0,4,8,31,8,4,0])

def setLCDText(text):
    """clear and set new text on LCD screen"""
    lcd.clear()
    lcd.message(text)

# show current GPS status on small screen
while True:
    try:

        # get temp data to display
        tempInfo = data.getJSONFromDataFile('temp.data')

        # get current location from GPS
        currentLocationInfo = data.getCurrentLatLong()
        completeLocationInfo = data.getJSONFromDataFile('location.data')
        
        # show GPS fixed position info
        lcd.set_color(1, 0, 0)    

        # get current heading by track
        tracking = str(data.getHeadingByDegrees(int(completeLocationInfo["track"])))
        
        tracking = 'NNE'
        
        # get tracking symbol from direction
        if tracking == 'N' or tracking == 'NNE' or tracking == 'NNW':
            trackingSymbol = '\x05'
        if tracking == 'E' or tracking == 'ENE' or tracking == 'ESE' or tracking == 'NE' or tracking == 'SE':
            trackingSymbol = '\x06'
        if tracking == 'S' or tracking == 'SSW' or tracking == 'SSE' or tracking == 'SW': 
            trackingSymbol = '\x07'
        if tracking == 'W' or tracking == 'WSW' or tracking == 'WNW' or tracking == 'NW':
            trackingSymbol = '\x08'
            
        setLCDText(str(tempInfo["temp"]) + "\x02 "+ str(tempInfo["hmidty"]) + "%"+ " " + trackingSymbol + " " + tracking + "\n" + str(int(completeLocationInfo['speed'])) +"mph " + str(int(completeLocationInfo['altitude'])) + "\x01")

    except (Exception):
    
        # GPS not fixed wait 5 seconds
        lcd.set_color(1, 1, 0)
    
        try:
            # get temp data to display
            tempInfo = data.getJSONFromDataFile('temp.data')
            setLCDText("Waiting for GPS Satellite\n" + str(tempInfo["temp"]) + "\x00  "+ str(tempInfo["hmidty"]) + "% hmdty")
        except (Exception):
            setLCDText("Waiting for GPS Satellite")

    time.sleep(5)
