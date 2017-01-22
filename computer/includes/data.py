#! /usr/bin/python
# Data helper functions to save and show human readable info
# Kevin Hinds http://www.kevinhinds.com
# License: GPL 2.0
import time, json, string, cgi, subprocess, os
import includes.settings as settings

def convertHumanReadable(seconds):
    """return days,hours,seconds for seconds in readable form"""
    return displayHumanReadableTime(seconds)

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

def displayHumanReadableTime(seconds, granularity=3):
    """display human readable units of time for given seconds"""
    intervals = (('d', 86400),('h', 3600),('m', 60),)
    result = []
    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            if value == 1:
                name = name.rstrip('s')
            result.append("{}{}".format(value, name))
    return ''.join(result[:granularity])

def getJSONFromDataFile(fileName):
    """get JSON contents from file in question"""
    try:
        with open(settings.logFilesLocation + fileName) as locationFile:    
            return json.load(locationFile)
    except (Exception):
        return ""

def saveJSONObjToFile(fileName, JSONObj):
    """create or rewrite object to data file as JSON"""
    f = file(settings.logFilesLocation + fileName, "w")
    f.write(str(JSONObj.to_JSON()))
      
def checkFileExists(fileName):
    """check if data file by name exists or not"""
    return os.path.exists(settings.logFilesLocation + fileName)
      
def getLastKnownLatLong():
    """get the last known lat/long from location data"""
    currentLocation = getJSONFromDataFile('last-location.data')
    
    # if we don't have
    if str(currentLocation['track']) == 'nan' or str(currentLocation['altitude']) == 'nan' or str(currentLocation['longitude']) == '0.0' or str(currentLocation['latitude']) == '0.0' or str(currentLocation['climb']) == 'nan' or str(currentLocation['speed']) == 'nan':
        raise ValueError('GPS is not fixed')
    
    # return lat/long as simple object
    currentLatLong = {}
    currentLatLong['latitude'] = currentLocation['latitude']
    currentLatLong['longitude'] = currentLocation['longitude']
    return currentLatLong
      
def getCurrentLatLong():
    """get the current lat/long from location data"""
    currentLocation = getJSONFromDataFile('location.data')
    
    # if we don't have
    if str(currentLocation['track']) == 'nan' or str(currentLocation['altitude']) == 'nan' or str(currentLocation['longitude']) == '0.0' or str(currentLocation['latitude']) == '0.0' or str(currentLocation['climb']) == 'nan' or str(currentLocation['speed']) == 'nan':
        raise ValueError('GPS is not fixed')
    
    # return lat/long as simple object
    currentLatLong = {}
    currentLatLong['latitude'] = currentLocation['latitude']
    currentLatLong['longitude'] = currentLocation['longitude']
    return currentLatLong
    
def removeJSONFile(fileName):
    """delete JSON file in question"""
    try:
        os.remove(settings.logFilesLocation + fileName)
    except (Exception):
        pass

def getHeadingByDegrees(heading):
    """get compass rose value from heading in degrees"""

    if heading <= 11.25:
        return 'N'
        
    if heading > 348.75:
        return 'N'
        
    if heading > 11.25 and heading <= 33.75:
        return 'NNE'
      
    if heading > 33.75 and heading <= 56.25:
        return 'NE'

    if heading > 56.25 and heading <= 78.75:
        return 'ENE'

    if heading > 78.75 and heading <= 101.25:
        return 'E'

    if heading > 101.25 and heading <= 123.75:
        return 'ESE'

    if heading > 123.75 and heading <= 146.25:
        return 'SE'

    if heading > 146.25 and heading <= 168.75:
        return 'SSE'

    if heading > 168.75 and heading <= 191.25:
        return 'S'

    if heading > 191.25 and heading <= 213.75:
        return 'SSW'

    if heading > 213.75 and heading <= 236.25:
        return 'SW'

    if heading > 236.25 and heading <= 258.75:
        return 'WSW'

    if heading > 258.75 and heading <= 281.25:
        return 'W'

    if heading > 281.25 and heading <= 303.75:
        return 'WNW'

    if heading > 303.75 and heading <= 326.25:
        return 'NW'

    if heading > 326.25 and heading <= 348.75:
        return 'NNW'
