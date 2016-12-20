#!/usr/bin/python
# Kevin Hinds http://www.kevinhinds.com
# License: GPL 2.0
import json
class CurrentReadings:
    '''Current Humidity and Tempurature Readings from DHT11 Sensor'''
    temp = -1
    hmidty = -1

    def __init__(self):
        self.temp = -1
        self.hmidty = -1
        
    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,sort_keys=True, indent=4)
