#!/usr/bin/env python
# postgres save driving stats from local data objects
import time, commands, subprocess, re, psycopg2
from datetime import datetime

# postgresql connection
postgresConn = psycopg2.connect(database="driving_statistics", user="pi", password="password", host="127.0.0.1", port="5432")
dBCursor = postgresConn.cursor()

def startNewTrip():
    """start new trip entry in the DB"""
    dBCursor.execute("""INSERT INTO driving_stats (time, new_trip_start) VALUES (%s, %s)""", ("now()","now()",))
    postgresConn.commit()

def saveDrivingStats(locationInfo, localeInfo, tempInfo, weatherInfo):
    """save second worth of driving stats to the DB"""
    dBCursor.execute("""INSERT INTO driving_stats (time, gps_latitude, gps_longitude, gps_altitude, gps_speed, gps_climb, gps_track, locale_address, locale_area, locale_city, locale_county, locale_country, locale_zipcode, inside_temp, inside_hmidty, weather_time, weather_summary, weather_icon, weather_apparenttemperature, weather_humidity, weather_precipintensity, weather_precipprobability, weather_windspeed) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", ("now()", str(locationInfo["latitude"]), str(locationInfo["longitude"]), str(locationInfo["altitude"]), str(locationInfo["speed"]), str(locationInfo["climb"]), str(locationInfo["track"]), str(localeInfo["address"]), str(localeInfo["area"]), str(localeInfo["city"]), str(localeInfo["country"]), str(localeInfo["county"]), str(localeInfo["zipcode"]), str(tempInfo["temp"]), str(tempInfo["hmidty"]), "now()", str(weatherInfo["summary"]), str(weatherInfo["icon"]), str(weatherInfo["apparentTemperature"]), str(weatherInfo["humidity"]), str(weatherInfo["precipIntensity"]), str(weatherInfo["precipProbability"]), str(weatherInfo["windSpeed"])))
    postgresConn.commit()
    
def getNewTripStartID():
    """get the highest DB row indentifier where a new trip starts"""
    return getOneResult("SELECT max(id) FROM driving_stats WHERE new_trip_start IS NOT NULL")
    
def getDrivingTimes(tripStartId):
    """get the driving times for current trip, day, week and month"""
    return [getOneResult("SELECT count(id) FROM driving_stats WHERE id > " + str(tripStartId)), getDrivingTimeByInterval("count(id)", "1 day"), getDrivingTimeByInterval("count(id)", "7 day"), getDrivingTimeByInterval("count(id)", "1 month")]

def getInTrafficTimes(tripStartId):
    """get the driving times for current trip, day, week and month"""
    return [getOneResult("SELECT count(id) FROM driving_stats WHERE gps_speed < 2 AND gps_speed != 'NaN' AND id > " + str(tripStartId)), getTrafficTimeByInterval("count(id)", "1 day"), getTrafficTimeByInterval("count(id)", "7 day"), getTrafficTimeByInterval("count(id)", "1 month")]

def getTrafficTimeByInterval(value, interval):
    """for given column and date interval retrieve the calculated value"""
    # if one day is specified it means since 7am
    if (interval == '1 day'):
        morningTime = datetime.now().strftime('%Y-%m-%d 07:00:00')        
        result = getOneResult("SELECT " + str(value) + " FROM driving_stats WHERE gps_speed < 2 AND gps_speed != 'NaN' AND time >= '" + morningTime + "'") 
    else:
        result = getOneResult("SELECT " + str(value) + " FROM driving_stats WHERE gps_speed < 2 AND gps_speed != 'NaN' AND time >= (now() - interval '" + str(interval) + "')")
    return result

def getAverageSpeeds(tripStartId):
    """get the average speed in mph for current trip, day, week and month"""    
    return [getOneResult("SELECT AVG(gps_speed) FROM driving_stats WHERE id > " + str(tripStartId) + "  AND gps_speed != 'NaN'"), getDrivingAvgByInterval("gps_speed", "1 day"), getDrivingAvgByInterval("gps_speed", "7 day"), getDrivingAvgByInterval("gps_speed", "1 month")]

def getAverageAlt(tripStartId):
    """get the average speed in mph for current trip, day, week and month"""    
    return [getOneResult("SELECT AVG(gps_altitude) FROM driving_stats WHERE id > " + str(tripStartId) + "  AND gps_altitude != 'NaN'"), getDrivingAvgByInterval("gps_altitude", "1 day"), getDrivingAvgByInterval("gps_altitude", "7 day"), getDrivingAvgByInterval("gps_altitude", "1 month")]

def getDrivingTimeByInterval(value, interval):
    """"for given column and date interval retrieve the calculated value"""
    # if one day is specified it means since 7am, since we're in UTC add 4 hours to it to match EST
    if (interval == '1 day'):
        morningTime = datetime.now().strftime('%Y-%m-%d 11:00:00')
        result = getOneResult("SELECT " + str(value) + " FROM driving_stats WHERE time >= '" + morningTime + "'") 
    else:
        result = getOneResult("SELECT " + str(value) + " FROM driving_stats WHERE time >= (now() - interval '" + str(interval) + "')") 
    return result

def getDrivingAvgByInterval(value, interval):
    """for given column and date interval retrieve the avg value"""
    # if one day is specified it means since 7am, since we're in UTC add 4 hours to it to match EST
    if (interval == '1 day'):
        morningTime = datetime.now().strftime('%Y-%m-%d 11:00:00')
        return getOneResult("SELECT AVG(" + value + ") FROM driving_stats WHERE time >= '" + morningTime + "' AND " + value + " != 'NaN'")
    else:
        return getOneResult("SELECT AVG(" + value + ") FROM driving_stats WHERE time >= (now() - interval '" + interval + "') AND " + value + " != 'NaN'")

def getMilesForInterval(interval):
    """"for given interval get the amount of miles travelled"""
    # if one day is specified it means since 7am, since we're in UTC add 4 hours to it to match EST
    if (interval == '1 day'):
        morningTime = datetime.now().strftime('%Y-%m-%d 11:00:00')
        pointsInTrip = getAllResults("SELECT gps_latitude, gps_longitude FROM driving_stats WHERE gps_latitude IS NOT NULL AND gps_longitude IS NOT NULL AND time >= '" + morningTime + "'")
    else:
        pointsInTrip = getAllResults("SELECT gps_latitude, gps_longitude FROM driving_stats WHERE gps_latitude IS NOT NULL AND gps_longitude IS NOT NULL AND time >= (now() - interval '" + str(interval) + "');")
    return getMilesForPoints(pointsInTrip)

def getMileageAmounts(tripStartId):
    """get the driving milage amounts for current trip, day, week and month"""
    postgresConn.set_isolation_level(0)
    return [getMilesForPoints(getAllResults("SELECT gps_latitude, gps_longitude FROM driving_stats WHERE id > " + str(tripStartId))), getMilesForInterval('1 day'), getMilesForInterval('7 day'), getMilesForInterval('30 day')]

def getMilesForPoints(points):
    """add up all the miles along the points"""
    metersTravelled = 0
    pointPosition = 0
    for point in points:
        try:
            startingPoint = points[pointPosition]
            endingPoint = points[pointPosition+1]
            pointPosition = pointPosition + 1
            metersTravelled = metersTravelled + getDistanceBetweenPoints(startingPoint, endingPoint)
        except (Exception):
            pass
    milesTravelled = metersTravelled * 0.000621371
    return int(milesTravelled)

def getDistanceBetweenPoints(startPoint, endPoint):
    """for a set of 2 latitude/longitude points, get the distance in meters between them"""
    return getOneResult("SELECT ST_Distance(ST_Transform(ST_GeomFromText('POINT(" + str(startPoint[0]) + " " + str(startPoint[1]) + ")',4326),26986),ST_Transform(ST_GeomFromText('POINT(" + str(endPoint[0]) + " " + str(endPoint[1]) + ")',4326),26986))")

def getAllResults(query):
    """get results rows for query"""
    dBCursor.execute(query)
    results = dBCursor.fetchall()
    return results

def getOneResult(query):
    """get one result row for query"""
    dBCursor.execute(query)
    result = dBCursor.fetchone()
    return result[0]
