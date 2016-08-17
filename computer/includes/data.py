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
