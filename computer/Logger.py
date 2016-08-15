#!/usr/bin/python
# Kevin Hinds http://www.kevinhinds.com
# License: GPL 2.0
import os, time, json
import includes.data as data
import includes.postgres as postgres

while True:
    locationInfo = data.getJSONFromDataFile('location.data')
    localeInfo = data.getJSONFromDataFile('locale.data')
    tempInfo = data.getJSONFromDataFile('temp.data')
    weatherInfo = data.getJSONFromDataFile('weather.data')
    postgres.saveDrivingStats(locationInfo, localeInfo, tempInfo, weatherInfo)
    time.sleep(1)