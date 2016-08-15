#!/usr/bin/python
# Kevin Hinds http://www.kevinhinds.com
# License: GPL 2.0
import time, json, random
import Adafruit_CharLCD as LCD
from pprint import pprint
import includes.data as data
lcd = LCD.Adafruit_CharLCDPlate()

# map special HEX characters for advanced display information
# http://www.quinapalus.com/hd44780udg.html
lcd.create_char(1, [24,24,7,4,6,4,4,0])
lcd.create_char(2, [0,4,14,21,4,4,4,4])
lcd.create_char(3, [0,0,0,4,0,0,0,0])

while True:
    pprint(data.getJSONFromDataFile('location.data'))
    lcd.set_color(round(random.random()), round(random.random()), round(random.random()))
    lcd.clear()
    lcd.message(str(random.random()) + "\n" + str(random.random()))
    time.sleep(2)
