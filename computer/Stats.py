#!/usr/bin/python
# Kevin Hinds http://www.kevinhinds.com
# License: GPL 2.0
import os, time, json
import includes.data as data
import includes.postgres as postgres

class DrivingStatistics:
    """Overall Driving Statistics to save as class to persist as JSON information to file"""
    drivingTimes = []
    inTrafficTimes = []
    averageSpeeds = []
    averageAltitude = []
    milesTravelled = []
    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,sort_keys=True, indent=4)
        
# get the beginning of the trip
thisTripStartID = postgres.getNewTripStartID()

# remove stats data and start calculating
data.removeJSONFile('stats.data')
while True:
    try:
        drivingStatistics = DrivingStatistics()
        drivingStatistics.drivingTimes = map(data.convertHumanReadable, postgres.getDrivingTimes(thisTripStartID))
        drivingStatistics.inTrafficTimes = map(data.convertHumanReadable, postgres.getInTrafficTimes(thisTripStartID))
        drivingStatistics.averageSpeeds = map(data.convertToString, map(data.convertToInt, postgres.getAverageSpeeds(thisTripStartID)))
        drivingStatistics.averageAltitude = map(data.convertToString, map(data.convertToInt, postgres.getAverageAlt(thisTripStartID)))

        # TODO, use map() and get this calculating from postgres.getDrivingTimes(thisTripStartID) not from the already formatted drivingTimes
        drivingStatistics.milesTravelled = 
        [
            drivingStatistics.drivingTimes[0] * (drivingStatistics.averageSpeeds[0]/60), 
            drivingStatistics.drivingTimes[1] * (drivingStatistics.averageSpeeds[1]/60), 
            drivingStatistics.drivingTimes[2] * (drivingStatistics.averageSpeeds[2]/60), 
            drivingStatistics.drivingTimes[3] * (drivingStatistics.averageSpeeds[3]/60)
        ]
        
        # create or rewrite data to stats data file as JSON, then wait 1 minute
        data.saveJSONObjToFile('stats.data', drivingStatistics)
        time.sleep(60)
    except (Exception):
        # data issue, wait 5 seconds
        data.saveJSONObjToFile('stats.data', drivingStatistics)
        time.sleep(5)
