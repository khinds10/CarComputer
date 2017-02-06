#!/usr/bin/python
# Current Humidity and Tempurature from DHT11 sensor
# Kevin Hinds http://www.kevinhinds.com
# License: GPL 2.0
import json
class CurrentReadings:
    '''Current Humidity and Tempurature Readings from DHT11 Sensor'''
    temp = 0
    hmidty = 0

    def __init__(self):
        self.temp = 0
        self.hmidty = 0
        
    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,sort_keys=True, indent=4)
