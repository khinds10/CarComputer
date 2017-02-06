#!/usr/bin/python
# Current GPS readings
# Kevin Hinds http://www.kevinhinds.com
# License: GPL 2.0
import json
class GPSInfo:
    '''GPS info as class to persist as JSON information to file'''
    latitude = 0
    longitude = 0
    altitude = 0
    speed = -1
    climb = 0
    track = 0
    mode = 0
    
    def __init__(self):
        self.latitude = 0
        self.longitude = 0
        self.altitude = 0
        self.speed = 0
        self.climb = 0
        self.track = 0
        self.mode = 0
        
    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,sort_keys=True, indent=4)
