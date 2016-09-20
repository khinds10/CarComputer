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
    milesTravelled = []
    averageSpeeds = []
    averageAltitude = []
    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,sort_keys=True, indent=4)
        
# get the beginning of the trip
thisTripStartID = postgres.getNewTripStartID()

def convertHumanReadable(seconds):
    """return days,hours,seconds for seconds in readable form"""
    return data.displayHumanReadableTime(seconds)

def convertNumberHumanReadable(miles):
    """get the number of miles with comma separation"""
    return ("{:,.0f} mi".format(miles))

def convertToInt(integer):
    """convert to integer catch for NoneTypes"""
    try:
        return int(integer)
    except (Exception):
        return 0

def convertToString(value):
    """convert to string catch for NoneTypes"""
    try:
        return str(value)
    except (Exception):
        return ""

# remove stats data and start calculating
data.removeJSONFile('stats.data')
while True:
    try:
        drivingStatistics = DrivingStatistics()
        drivingStatistics.drivingTimes = map(convertHumanReadable, postgres.getDrivingTimes(thisTripStartID))
        drivingStatistics.inTrafficTimes = map(convertHumanReadable, postgres.getInTrafficTimes(thisTripStartID))
        
        # todo, get the miles working as separate process, postgis is very expensive
        drivingStatistics.milesTravelled =  map(convertNumberHumanReadable, [0, 0, 0, 0])
        drivingStatistics.averageSpeeds = map(convertToString, map(convertToInt, postgres.getAverageSpeeds(thisTripStartID)))
        drivingStatistics.averageAltitude = map(convertToString, map(convertToInt, postgres.getAverageAlt(thisTripStartID)))

        # create or rewrite data to stats data file as JSON, then wait 1 minute
        data.saveJSONObjToFile('stats.data', drivingStatistics)
        time.sleep(60)
    except (Exception):
        # data issue, wait 5 seconds
        data.saveJSONObjToFile('stats.data', drivingStatistics)
        time.sleep(5)
