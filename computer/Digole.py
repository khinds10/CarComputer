#!/usr/bin/python
# Kevin Hinds http://www.kevinhinds.com
# License: GPL 2.0
import datetime as dt
import time, json, string, cgi, subprocess, json
import includes.data as data
import info.CurrentReadings as CurrentReadings
import info.WeatherDetails as WeatherDetails
import info.GPSInfo as GPSInfo
import info.DrivingStatistics as DrivingStatistics
import info.CurrentReadings as CurrentReadings
import info.LocaleDetails as LocaleDetails

def resetScreen():
    """clear and rotate screen"""
    subprocess.call([digoleDriveLocation, "clear"])
    subprocess.call([digoleDriveLocation, "setRot90"])
    pass

def defaultScreen():
    """show default screen"""
    resetScreen()

def statisticsScreen():
    """show statistics screen"""
    resetScreen()

def setFont(fontSize):
    """set font size for screen"""
    subprocess.call([digoleDriveLocation, "setFont", fontSize])
    
def setColor(fontColor):
    """set font color for screen"""
    subprocess.call([digoleDriveLocation, "setColor", fontColor])

def printByFontColorPosition(fontSize, fontColor, x, y, text, previousText):
    """erase existing text and print at x,y """
    setFont(fontSize)
    
    # print the previous text in black to then print the new text
    setColor("0")
    subprocess.call([digoleDriveLocation, "printxy_abs", x, y, previousText])
    
    # print the new text at the desired color, x, y and font size
    setColor(fontColor)
    subprocess.call([digoleDriveLocation, "printxy_abs", x, y, text])
    
    print fontSize, fontColor, x, y, text, previousText

def showStatisticsScreen():
    """show statistics screen by button press"""
    resetScreen()
    
    # stats.data
    drivingStatistics = data.getJSONFromDataFile('stats.data')
    if drivingStatistics == "":
        drivingStatistics = DrivingStatistics.DrivingStatistics()
        drivingStatistics = json.loads(tempInfo.to_JSON())
    
    printByFontColorPosition("120", "249", "5", "35", "Today: " + str(drivingStatistics['drivingTimes'][1]) + "/" + str(drivingStatistics['inTrafficTimes'][1]), "")
    printByFontColorPosition("120", "249", "5", "70", "       " + str(drivingStatistics['milesTravelled'][1]) + " mi / " + drivingStatistics['averageSpeeds'][1] + " mph", "")
    
    printByFontColorPosition("120", "249", "5", "35", "Week: " + str(drivingStatistics['drivingTimes'][2]) + "/" + str(drivingStatistics['inTrafficTimes'][2]), "")
    printByFontColorPosition("120", "249", "5", "70", "       " + str(drivingStatistics['milesTravelled'][2]) + " mi / " + drivingStatistics['averageSpeeds'][2] + " mph", "")
    
    printByFontColorPosition("120", "249", "5", "35", "Month: " + str(drivingStatistics['drivingTimes'][3]) + "/" + str(drivingStatistics['inTrafficTimes'][3]), "")
    printByFontColorPosition("120", "249", "5", "70", "       " + str(drivingStatistics['milesTravelled'][3]) + " mi / " + drivingStatistics['averageSpeeds'][3] + " mph", "")
    
    time.sleep(5)
    # set the button press back to zero
    resetScreen()
    
    # reset the current driving condition values
    weatherNextHour = ''
    weatherOutside = ''
    tempHmidty = ''
    locationTrack = ''
    statsDrivingTimes = ''
    statsInTrafficTimes = ''
    statsAverageSpeeds = ''
    statsMilesTravelled = ''

# weather.data
weatherNextHour = ''
weatherOutside = ''

# temp.data
tempHmidty = ''

# location.data  (use equation)
locationTrack = ''
currentTime = ''

# stats.data (get the first of each)
statsDrivingTimes = ''
statsInTrafficTimes = ''
statsAverageSpeeds = ''
statsMilesTravelled = ''

# reset screen and load beginning driving statistics using the configured digole driver
digoleDriveLocation = "/home/pi/CarComputer/computer/digole"
resetScreen()

########################
# default screen
########################

# begin loop through main default screen
while True:

    # weather.data
    weatherInfo = data.getJSONFromDataFile('weather.data')
    if weatherInfo == "":
        weatherInfo = WeatherDetails.WeatherDetails()
        weatherInfo = json.loads(weatherInfo.to_JSON())

    # next hour weather
    if weatherNextHour != weatherInfo['nextHour']:
        printByFontColorPosition("51", "255", "5", "75", weatherInfo['nextHour'][:25], weatherNextHour)
        weatherNextHour = weatherInfo['nextHour']

    # outside temp/humidity
    weatherOutsideUpdated = '[' + str(int(weatherInfo['apparentTemperature'])) + '*F ' + str(int(weatherInfo['humidity']*100)) + '%]'
    if weatherOutside != weatherOutsideUpdated:
        printByFontColorPosition("120", "240", "150", "35", weatherOutsideUpdated, weatherOutside)
        weatherOutside = weatherOutsideUpdated
    
    # temp.data
    tempInfo = data.getJSONFromDataFile('temp.data')
    if tempInfo == "":
        tempInfo = CurrentReadings.CurrentReadings()
        tempInfo = json.loads(tempInfo.to_JSON())
    
    # inside temp / humidity
    tempHmidtyUpdated =  str(tempInfo['temp']) + "*F " + str(tempInfo['hmidty']) + "%"
    if tempHmidty != tempHmidtyUpdated:
        printByFontColorPosition("120", "249", "5", "35", tempHmidtyUpdated, tempHmidty)        
        tempHmidty = tempHmidtyUpdated

    # stats.data
    drivingStatistics = data.getJSONFromDataFile('stats.data')
    if drivingStatistics == "":
        drivingStatistics = DrivingStatistics.DrivingStatistics()
        drivingStatistics = json.loads(tempInfo.to_JSON())
    
    # current driving time
    statsDrivingTimesUpdated = str(drivingStatistics['drivingTimes'][0])
    if statsDrivingTimes != statsDrivingTimesUpdated:
        printByFontColorPosition("120", "28", "5", "125", statsDrivingTimesUpdated, statsDrivingTimes)
        statsDrivingTimes = statsDrivingTimesUpdated
        
    # current in-traffic time
    statsInTrafficTimesUpdated = str(drivingStatistics['inTrafficTimes'][0]) + ' [Traffic]'
    if statsInTrafficTimes != statsInTrafficTimesUpdated:
        printByFontColorPosition("120", "252", "120", "125", statsInTrafficTimesUpdated, statsInTrafficTimes)
        statsInTrafficTimes = statsInTrafficTimesUpdated
    
    # average speed
    statsAverageSpeedsUpdated = str(drivingStatistics['averageSpeeds'][0]) + 'mph [Avg]'
    if statsAverageSpeeds != statsAverageSpeedsUpdated:
        printByFontColorPosition("120", "250", "5", "175", statsAverageSpeedsUpdated, statsAverageSpeeds)
        statsAverageSpeeds = statsAverageSpeedsUpdated

    # miles travelled
    statsMilesTravelledUpdated = str(drivingStatistics['milesTravelled'][0]) + ' mi Est.'
    if statsMilesTravelled != statsMilesTravelledUpdated:
        printByFontColorPosition("120", "222", "190", "175", statsMilesTravelledUpdated[:10], statsMilesTravelled)
        statsMilesTravelled = statsMilesTravelledUpdated
    
    # location.data
    locationInfo = data.getJSONFromDataFile('location.data')
    if locationInfo == "":
        locationInfo = GPSInfo.GPSInfo()
        locationInfo = json.loads(locationInfo.to_JSON())
    
    currentTimeUpdated = ''
    printByFontColorPosition("120", "249", "150", "225", " - 11:09pm - ", '')
    
    # if button pressed go to the 2nd screen for 5 seconds
    # showStatisticsScreen()
    
    time.sleep(1)
