#!/usr/bin/python
# Current summarized driving statistics
# Kevin Hinds http://www.kevinhinds.com
# License: GPL 2.0
import json
class DrivingStatistics:
    """Overall Driving Statistics to save as class to persist as JSON information to file"""
    drivingTimes = ['','','','']
    inTrafficTimes = ['','','','']
    averageSpeeds = [0,0,0,0]
    averageAltitude = [0,0,0,0]
    milesTravelled = [0,0,0,0]
    
    def __init__(self):
        self.drivingTimes = ['','','','']
        self.inTrafficTimes = ['','','','']
        self.milesTravelled = [0,0,0,0]
        self.averageSpeeds = [0,0,0,0]
        self.averageAltitude = [0,0,0,0]
            
    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,sort_keys=True, indent=4)
