#!/usr/bin/env python
import time, datetime, subprocess, json
import string, cgi, subprocess, json
import includes.data as data
import includes.settings as settings
print "Access-Control-Allow-Origin: *\n\n"

class TripStatistics:
    '''JSON Info to show on the HTML output of the display monitor'''
    time = ''
    outsideTemp = ''
    outsideHumidity = ''
    insideTemp = ''
    insideHumidity = ''
    tracking = ''
    track = ''
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
    zipcode = ''
    address = ''
    area = ''
    city = ''
    country = ''
    county = ''
    zipcode = ''
    phoneMessage = ''
    drivingTimes = ''
    inTrafficTimes = ''
    averageSpeeds = ''
    averageAltitude = ''
    climb = ''
    latitude = ''
    longitude = ''
    internetConnected = ''
    buttonPressed = 'Down'
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
except (Exception):
        pass
try:
    locationInfo = data.getJSONFromDataFile('location.data')
except (Exception):
        pass
try:
    localeInfo = data.getJSONFromDataFile('locale.data')
except (Exception):
        pass
try:
    weatherInfo = data.getJSONFromDataFile('weather.data')
except (Exception):
        pass
try:
    drivingStats = data.getJSONFromDataFile('stats.data')
except (Exception):
        pass
try:
    mileageStats = data.getJSONFromDataFile('miles.data')
except (Exception):
        pass
try:
    buttonPressed = data.getJSONFromDataFile('button.data')
except (Exception):
        pass

# create JSON output of current trip stats
tripStatistics = TripStatistics()

# get if the internet is connected or not "ok" / "error"
try:
    isConnected = subprocess.check_output(['bash', 'connection.sh'])
    isConnected = isConnected.strip()
    tripStatistics.internetConnected = isConnected
except (Exception):
        pass
try:
    tripStatistics.time = datetime.datetime.fromtimestamp(time.time()).strftime('%I:%M%p').lstrip('0')
except (Exception):
        pass
try: 
    tripStatistics.insideTemp = str(tempInfo['temp'])
except (Exception):
        pass
try: 
    tripStatistics.insideHumidity = str(tempInfo['hmidty'])
except (Exception):
        pass
try: 
    tripStatistics.drivingTime = str(drivingStats['drivingTimes'][0])
except (Exception):
        pass
try: 
    tripStatistics.averageSpeed = str(drivingStats['averageSpeeds'][0])
except (Exception):
        pass
try: 
    tripStatistics.inTrafficTime = str(drivingStats['inTrafficTimes'][0])
except (Exception):
        pass
try: 
    tripStatistics.drivingTimes = drivingStats['drivingTimes']
except (Exception):
        pass
try: 
    tripStatistics.inTrafficTimes = drivingStats['inTrafficTimes']
except (Exception):
        pass
try: 
    tripStatistics.averageSpeeds = drivingStats['averageSpeeds']
except (Exception):
        pass
try: 
    tripStatistics.averageAltitude = drivingStats['averageAltitude']
except (Exception):
        pass
try: 
    tripStatistics.tripMilesTravelled = str(mileageStats['milesTravelled'][0])
except (Exception):
        pass    
try: 
    tripStatistics.milesTravelled = mileageStats['milesTravelled']
except (Exception):
        pass
try: 
    tripStatistics.phoneMessage = str(message)
except (Exception):
        pass
try: 
    tripStatistics.outsideTemp = str(int(weatherInfo['apparentTemperature']))
except (Exception):
        pass
try: 
    tripStatistics.outsideHumidity = str(int(weatherInfo['humidity']*100))
except (Exception):
        pass
try: 
    tripStatistics.tracking = str(data.getHeadingByDegrees(locationInfo['track']))
except (Exception):
        pass
try: 
    tripStatistics.track = str(locationInfo['track'])
except (Exception):
        pass
try: 
    tripStatistics.altitude = str(int(locationInfo['altitude']))
except (Exception):
        pass
try: 
    tripStatistics.speed = str(int(locationInfo['speed']))
except (Exception):
        pass
try: 
    tripStatistics.climb = str(int(locationInfo['climb']))
except (Exception):
        pass
try: 
    tripStatistics.latitude = str(float(locationInfo['latitude']))
except (Exception):
        pass
try: 
    tripStatistics.longitude = str(float(locationInfo['longitude']))
except (Exception):
        pass        
try: 
    tripStatistics.weatherSummary = str(weatherInfo['summary'])
except (Exception):
        pass
try: 
    tripStatistics.icon = str(weatherInfo['icon'])
except (Exception):
        pass    
try: 
    tripStatistics.windSpeed = str(int(weatherInfo['windSpeed']))
except (Exception):
        pass
try: 
    tripStatistics.precipProbability = str(int(weatherInfo['precipProbability']*100))
except (Exception):
        pass
try: 
    tripStatistics.precipIntensity = str(int(weatherInfo['precipIntensity']*100))
except (Exception):
        pass
try: 
    tripStatistics.weatherNextHour = str(weatherInfo['nextHour'])
except (Exception):
        pass
try:
    tripStatistics.address = str(localeInfo['address'])
except (Exception):
        pass
try:
    tripStatistics.area = str(localeInfo['area'])
except (Exception):
        pass
try:
    tripStatistics.city = str(localeInfo['city'])
except (Exception):
        pass
try:
    tripStatistics.country = str(localeInfo['country'])
except (Exception):
        pass
try:
    tripStatistics.county = str(localeInfo['county'])
except (Exception):
        pass
try:
    tripStatistics.zipcode = str(localeInfo['zipcode'])
except (Exception):
        pass
try:
    tripStatistics.buttonPressed = buttonPressed['name']
except (Exception):
        tripStatistics.buttonPressed = 'Down'
        pass
        
# produce JSON/Output
print str(tripStatistics.to_JSON())
