#!/usr/bin/python
# Kevin Hinds http://www.kevinhinds.com
# License: GPL 2.0
import Adafruit_DHT
import os, time, json
import includes.data as data

# set to use DHT11 sensor
sensor = Adafruit_DHT.DHT11
pin = 16

class CurrentReadings:
    '''Current Humidity and Tempurature Readings from DHT11 Sensor'''
    temp = 0
    hmidty = 0
    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,sort_keys=True, indent=4)

# reset temp data and start logging
currentReadings = CurrentReadings()
currentReadings.temp = 0
currentReadings.hmidty = 0
data.saveJSONObjToFile('temp.data', currentReadings)

# start logging temp
while True:
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    if humidity is not None and temperature is not None:
        # convert to imperial units, save to JSON file and wait one second
        temperature = 9.0/5.0 * temperature + 32
        currentReadings = CurrentReadings()
        currentReadings.temp = int(temperature)
        currentReadings.hmidty = int(humidity)
        data.saveJSONObjToFile('temp.data', currentReadings)
    time.sleep(1)
