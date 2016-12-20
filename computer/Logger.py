#!/usr/bin/python
# Kevin Hinds http://www.kevinhinds.com
# License: GPL 2.0
import os, time, json
import includes.data as data
import includes.postgres as postgres
import info.CurrentReadings as CurrentReadings
import info.WeatherDetails as WeatherDetails
import info.GPSInfo as GPSInfo
import info.DrivingStatistics as DrivingStatistics
import info.CurrentReadings as CurrentReadings
import info.LocaleDetails as LocaleDetails

# save full datasets to DB each second
while True:
    #try:
        locationInfo = data.getJSONFromDataFile('location.data')
        if locationInfo == "":
            locationInfo = GPSInfo.GPSInfo()
            locationInfo = json.loads(locationInfo.to_JSON())
        
        localeInfo = data.getJSONFromDataFile('locale.data')
        if localeInfo == "":
            localeInfo = LocaleDetails.LocaleDetails()
            localeInfo = json.loads(localeDetails.to_JSON())
        
        tempInfo = data.getJSONFromDataFile('temp.data')
        if tempInfo == "":
            tempInfo = CurrentReadings.CurrentReadings()
            tempInfo = json.loads(currentReadings.to_JSON())
        
        weatherInfo = data.getJSONFromDataFile('weather.data')
        if weatherInfo == "":
            weatherInfo = WeatherDetails.WeatherDetails()
            weatherInfo = json.loads(weatherDetails.to_JSON())
        
        print locationInfo
        print localeInfo
        print tempInfo
        print weatherInfo
        
        postgres.saveDrivingStats(locationInfo, localeInfo, tempInfo, weatherInfo)    
    #except (Exception):
    #    pass
        time.sleep(1)
