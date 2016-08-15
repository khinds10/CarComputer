#! /usr/bin/python
# Kevin Hinds http://www.kevinhinds.com
# License: GPL 2.0
import time, json, string, cgi, subprocess, os
import includes.settings as settings

def getJSONFromDataFile(fileName):
    """get JSON contents from file in question"""
    with open(settings.logFilesLocation + fileName) as locationFile:    
        return json.load(locationFile)
		
def saveJSONObjToFile(fileName, JSONObj):
    """create or rewrite object to data file as JSON"""
    f = file(settings.logFilesLocation + fileName, "w")
    f.write(str(JSONObj.to_JSON()))
      
def getCurrentLatLong():
    """get the current lat/long from location data"""
    try:
        currentLocation = getJSONFromDataFile('location.data')
    except (Exception):
        # default to 0.0 if GPS is not ready
        currentLocation = {}
        currentLocation['latitude'] = '0.0'
        currentLocation['longitude'] = '0.0'
    
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
