#!/usr/bin/python
# Kevin Hinds http://www.kevinhinds.com
# License: GPL 2.0
import os, time, json
import includes.data as data
import includes.postgres as postgres

# get the beginning of the trip
thisTripStartID = postgres.getNewTripStartID()

# remove stats data and start calculating
data.removeJSONFile('stats.data')
while True:

    
    drivingTimes = postgres.calculateDrivingTimes(thisTripStartID)
    currentTime = data.displayHumanReadableTime(drivingTimes[0])
    dayTime = data.displayHumanReadableTime(drivingTimes[1])
    weekTime = data.displayHumanReadableTime(drivingTimes[2])
    monthTime = data.displayHumanReadableTime(drivingTimes[3])


    print postgres.getAverageSpeeds(thisTripStartID)

    time.sleep(1)
