#!/usr/bin/python
# Kevin Hinds http://www.kevinhinds.com
# License: GPL 2.0
import json
class WeatherDetails:
    '''Weather Information as class to persist as JSON information to file'''
    time = 0
    summary = ''
    nextHour = ''
    icon = ''
    apparentTemperature = -1
    humidity = -1
    precipIntensity = -1
    precipProbability = -1
    windSpeed = -1
    
    def __init__(self):
        self.time = 0
        self.summary = ''
        self.nextHour = ''
        self.icon = ''
        self.apparentTemperature = -1
        self.humidity = -1
        self.precipIntensity = -1
        self.precipProbability = -1
        self.windSpeed = -1
        
    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,sort_keys=True, indent=4)
