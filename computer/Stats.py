#!/usr/bin/python
# Kevin Hinds http://www.kevinhinds.com
# License: GPL 2.0
import os, time, json
import includes.data as data
import includes.postgres as postgres

# get the beginning of the trip
thisTripStartID = postgres.getNewTripStartID()

print thisTripStartID

# remove stats data and start calculating
data.removeJSONFile('stats.data')
while True:

    # check for Nones here
    # [0L, 3L, 3L, 3L]
    # [None, None, None, None]

    drivingTimes = postgres.getDrivingTimes(thisTripStartID)
    print drivingTimes

    averageSpeeds = postgres.getAverageSpeeds(thisTripStartID)
    print averageSpeeds
    
    averageAltitude = postgres.getAverageAlt(thisTripStartID)
    print averageAltitude

    time.sleep(1)
