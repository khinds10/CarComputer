#!/usr/bin/python
# Kevin Hinds http://www.kevinhinds.com
# License: GPL 2.0
import json
class DrivingStatistics:
    """Overall Driving Statistics to save as class to persist as JSON information to file"""
    drivingTimes = ['','','','']
    inTrafficTimes = ['','','','']
    averageSpeeds = [-1,-1,-1,-1]
    averageAltitude = [-1,-1,-1,-1]
    milesTravelled = [-1,-1,-1,-1]
    
    def __init__(self):
        self.drivingTimes = ['','','','']
        self.inTrafficTimes = ['','','','']
        self.milesTravelled = [-1,-1,-1,-1]
        self.averageSpeeds = [-1,-1,-1,-1]
        self.averageAltitude = [-1,-1,-1,-1]
            
    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,sort_keys=True, indent=4)
