#!/usr/bin/python
# Kevin Hinds http://www.kevinhinds.com
# License: GPL 2.0
import Adafruit_DHT
import os, time, json
import includes.data as data
import info.CurrentReadings as CurrentReadings

# set to use DHT11 sensor
sensor = Adafruit_DHT.DHT11
pin = 16

# start logging temp
data.removeJSONFile('temp.data')
while True:
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    if humidity is not None and temperature is not None:
        # convert to imperial units, save to JSON file and wait one second
        temperature = 9.0/5.0 * temperature + 32
        currentReadings = CurrentReadings.CurrentReadings()
        currentReadings.temp = int(temperature)
        currentReadings.hmidty = int(humidity)
        data.saveJSONObjToFile('temp.data', currentReadings)
    time.sleep(1)
