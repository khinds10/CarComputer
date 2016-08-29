#!/usr/bin/env python
import time, datetime, subprocess, json
import string, cgi, subprocess, json
import includes.data as data
import includes.settings as settings
print "Access-Control-Allow-Origin: *\n\n"

# adjust time in UTC to Eastern Standard Time
timezone=4*60*60

class TripStatistics:
    '''JSON Info to show on the HTML output of the display monitor'''
    time = ''
    outsideTemp = ''
    outsideHumidity = ''
    insideTemp = ''
    insideHumidity = ''
    tracking = ''
    altitude = ''
    speed = ''
    drivingTime = ''
    averageSpeed = ''
    inTrafficTime = ''
    weatherSummary = ''
    icon = ''
    windSpeed = ''
    precipProbability = ''
    precipIntensity = ''
    weatherNextHour = ''
    localeInfo = ''
    phoneMessage = ''
    drivingTimes = ''
    inTrafficTimes = ''
    averageSpeeds = ''
    averageAltitude = ''
    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,sort_keys=True, indent=4)

# get dashboard phone message
message = ""

# if a dashboard pi project is running, it will show a recent phone message on the screen
if settings.dashboardServer:
    try:
        phoneDashboardInfo = json.loads(unicode(subprocess.check_output(['curl', "http://" + settings.dashboardServer + "/message"]), errors='ignore'))
        message = str(phoneDashboardInfo["message"])
    except (Exception):
        pass
    
# get all available info and create HTML output for it
try: 
    tempInfo = data.getJSONFromDataFile('temp.data')
    drivingStats = data.getJSONFromDataFile('stats.data')
    locationInfo = data.getJSONFromDataFile('location.data')
    localeInfo = data.getJSONFromDataFile('locale.data')
    weatherInfo = data.getJSONFromDataFile('weather.data')
except (Exception):
        pass
        
# create JSON output of current trip stats
tripStatistics = TripStatistics()
try: 
    tripStatistics.time = datetime.datetime.fromtimestamp(time.time()-timezone).strftime('%I:%M%p').lstrip('0')
    tripStatistics.insideTemp = str(tempInfo['temp'])
    tripStatistics.insideHumidity = str(tempInfo['hmidty'])
    tripStatistics.drivingTime = str(drivingStats['drivingTimes'][0])
    tripStatistics.averageSpeed = str(drivingStats['averageSpeeds'][0])
    tripStatistics.inTrafficTime = str(drivingStats['inTrafficTimes'][0])
    tripStatistics.drivingTimes = drivingStats['drivingTimes']
    tripStatistics.inTrafficTimes = drivingStats['inTrafficTimes']
    tripStatistics.averageSpeeds = drivingStats['averageSpeeds']
    tripStatistics.averageAltitude = drivingStats['averageAltitude']
    tripStatistics.phoneMessage = str(message)
    tripStatistics.outsideTemp = str(int(weatherInfo['apparentTemperature']))
    tripStatistics.outsideHumidity = str(int(weatherInfo['humidity']*100))
    tripStatistics.tracking = str(data.getHeadingByDegrees(locationInfo['track']))
    tripStatistics.altitude = str(int(locationInfo['altitude']))
    tripStatistics.speed = str(int(locationInfo['speed']))
    tripStatistics.weatherSummary = str(weatherInfo['summary'])
    tripStatistics.icon = str(weatherInfo['icon'])
    tripStatistics.windSpeed = str(int(weatherInfo['windSpeed']))
    tripStatistics.precipProbability = str(int(weatherInfo['precipProbability']*100))
    tripStatistics.precipIntensity = str(int(weatherInfo['precipIntensity']*100))
    tripStatistics.weatherNextHour = str(weatherInfo['nextHour'])
    tripStatistics.localeInfo = str(localeInfo['zipcode'])
except (Exception):
        pass
        
# produce JSON/Output
print str(tripStatistics.to_JSON())
