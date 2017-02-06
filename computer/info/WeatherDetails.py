#!/usr/bin/python
# Current Weather conditions
# Kevin Hinds http://www.kevinhinds.com
# License: GPL 2.0
import json
class WeatherDetails:
    '''Weather Information as class to persist as JSON information to file'''
    time = 0
    summary = ''
    nextHour = ''
    icon = ''
    apparentTemperature = 0
    humidity = 0
    precipIntensity = 0
    precipProbability = 0
    windSpeed = 0
    
    def __init__(self):
        self.time = 0
        self.summary = ''
        self.nextHour = ''
        self.icon = ''
        self.apparentTemperature = 0
        self.humidity = 0
        self.precipIntensity = 0
        self.precipProbability = 0
        self.windSpeed = 0
        
    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,sort_keys=True, indent=4)
