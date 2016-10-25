#!/usr/bin/python
# Kevin Hinds http://www.kevinhinds.com
# License: GPL 2.0
import os, time, json
import includes.data as data
import includes.postgres as postgres

class MileageStatistics:
    """Overall Mileage Statistics to save as class to persist as JSON information to file"""
    milesTravelled = []
    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,sort_keys=True, indent=4)

# get the beginning of the trip
thisTripStartID = postgres.getNewTripStartID()

# remove current miles data and start calculating
data.removeJSONFile('miles.data')
while True:
    try:
        mileageStatistics = MileageStatistics()
        mileageStatistics.milesTravelled =  map(data.convertNumberHumanReadable, postgres.getMileageAmounts(thisTripStartID))
        
        # create or rewrite data to miles data file as JSON, then wait 1 minute
        data.saveJSONObjToFile('miles.data', mileageStatistics)
        time.sleep(60)
    except (Exception):
        # data issue, wait 5 seconds
        data.saveJSONObjToFile('miles.data', mileageStatistics)
        time.sleep(5)