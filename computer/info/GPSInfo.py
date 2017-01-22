#!/usr/bin/python
# Current GPS readings
# Kevin Hinds http://www.kevinhinds.com
# License: GPL 2.0
import json
class GPSInfo:
    '''GPS info as class to persist as JSON information to file'''
    latitude = -1
    longitude = -1
    altitude = -1
    speed = -1
    climb = -1
    track = -1
    mode = -1
    
    def __init__(self):
        self.latitude = -1
        self.longitude = -1
        self.altitude = -1
        self.speed = -1
        self.climb = -1
        self.track = -1
        self.mode = -1
        
    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,sort_keys=True, indent=4)
