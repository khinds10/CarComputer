#!/usr/bin/env python
# postgres save driving stats from local data objects
import time, commands, subprocess, re, psycopg2

# postgresql connection
postgresConn = psycopg2.connect(database="driving_statistics", user="pi", password="password", host="127.0.0.1", port="5432")
dBCursor = postgresConn.cursor()

def startNewTrip():
    """start new trip entry in the DB"""
    dBCursor.execute("""INSERT INTO driving_stats (time, new_trip_start) VALUES (%s, %s)""", ("now()","now()",))
    postgresConn.commit()

def saveDrivingStats(locationInfo, localeInfo, tempInfo, weatherInfo):
    """save second worth of driving stats to the DB"""
    dBCursor.execute("""INSERT INTO driving_stats (time, gps_latitude, gps_longitude, gps_altitude, gps_speed, gps_climb, gps_track, locale_address, locale_area, locale_city, locale_county, locale_country, locale_zipcode, inside_temp, inside_hmidty, weather_time, weather_summary, weather_icon, weather_apparenttemperature, weather_humidity, weather_precipintensity, weather_precipprobability, weather_windspeed) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", ("now()", str(locationInfo["latitude"]), str(locationInfo["longitude"]), str(locationInfo["altitude"]), str(locationInfo["speed"]), str(locationInfo["climb"]), str(locationInfo["track"]), str(localeInfo["address"]), str(localeInfo["area"]), str(localeInfo["city"]), str(localeInfo["country"]), str(localeInfo["county"]), str(localeInfo["zipcode"]), str(tempInfo["temp"]), str(tempInfo["hmidty"]), str(weatherInfo["time"]), str(weatherInfo["summary"]), str(weatherInfo["icon"]), str(weatherInfo["apparentTemperature"]), str(weatherInfo["humidity"]), str(weatherInfo["precipIntensity"]), str(weatherInfo["precipProbability"]), str(weatherInfo["windSpeed"])))
    postgresConn.commit()
    
def getNewTripStartID():
    """get the highest DB row indentifier where a new trip starts"""
    dBCursor.execute("SELECT max(id) FROM driving_stats WHERE new_trip_start IS NOT NULL")
    return dBCursor.fetchone()
    
def calculateDrivingTimes(tripStartId):
    """get the driving times for current trip, day, week and month"""
    dBCursor.execute("SELECT count(id) FROM driving_stats WHERE id > %s", (tripStartId))
    currentDrivingSeconds = dBCursor.fetchone()
    currentDrivingSeconds = currentDrivingSeconds[0]
    
    dBCursor.execute("SELECT count(id) FROM driving_stats WHERE time >= (now() - interval '1 day')")
    dayDrivingSeconds = dBCursor.fetchone()
    dayDrivingSeconds = dayDrivingSeconds[0]
    
    dBCursor.execute("SELECT count(id) FROM driving_stats WHERE time >= (now() - interval '7 day')")
    weekDrivingSeconds = dBCursor.fetchone()
    weekDrivingSeconds = weekDrivingSeconds[0]
    
    dBCursor.execute("SELECT count(id) FROM driving_stats WHERE time >= (now() - interval '1 month')")
    monthDrivingSeconds = dBCursor.fetchone()
    monthDrivingSeconds = monthDrivingSeconds[0]
    
    return [currentDrivingSeconds, dayDrivingSeconds, weekDrivingSeconds, monthDrivingSeconds]


def getAverageSpeeds(tripStartId):
    """get the average speed in mph for current trip, day, week and month"""
    dBCursor.execute("SELECT AVG(gps_speed) FROM driving_stats WHERE id > %s  AND gps_speed != 'NaN'", (tripStartId))
    currentAvgMPH = dBCursor.fetchone()
    currentAvgMPH = currentAvgMPH[0]
    
    dBCursor.execute("SELECT AVG(gps_speed) FROM driving_stats WHERE time >= (now() - interval '1 day') AND gps_speed != 'NaN'")
    dayAvgMPH = dBCursor.fetchone()
    dayAvgMPH = dayAvgMPH[0]
    
    dBCursor.execute("SELECT AVG(gps_speed) FROM driving_stats WHERE time >= (now() - interval '7 day') AND gps_speed != 'NaN'")
    weekAvgMPH = dBCursor.fetchone()
    weekAvgMPH = weekAvgMPH[0]
    
    dBCursor.execute("SELECT AVG(gps_speed) FROM driving_stats WHERE time >= (now() - interval '1 month') AND gps_speed != 'NaN'")
    monthAvgMPH = dBCursor.fetchone()
    monthAvgMPH = monthAvgMPH[0]
    
    return [int(currentAvgMPH), int(dayAvgMPH), int(weekAvgMPH), int(monthAvgMPH)]




 
    #SELECT count(*)
    #FROM users
    #WHERE created_at >= (now() - interval '1 month');
        
     
     #id                          | integer                     | not null default nextval('driving_stats_id_seq'::regclass)
     #time                        | timestamp without time zone | not null
     #new_trip_start              | timestamp without time zone | 
     #gps_latitude                | double precision            | 
     #gps_longitude               | double precision            | 
     #gps_altitude                | real                        | 
     #gps_speed                   | real                        | 
     #gps_climb                   | real                        | 
     #gps_track                   | real                        | 
     #locale_address              | text                        | 
     #locale_area                 | text                        | 
     #locale_city                 | text                        | 
     #locale_county               | text                        | 
     #locale_country              | text                        | 
     #locale_zipcode              | text                        | 
     #inside_temp                 | real                        | 
     #inside_hmidty               | real                        | 
     #weather_time                | timestamp without time zone | 
     #weather_summary             | text                        | 
     #weather_icon                | text                        | 
     #weather_apparenttemperature | real                        | 
     #weather_humidity            | real                        | 
     #weather_precipintensity     | real                        | 
     #weather_precipprobability   | real                        | 
     #weather_windspeed           | real                        |  
        
    # dBCursor.execute("SELECT * FROM test;")
    # dBCursor.fetchone()
    # (1, 100, "abc'def")
    

    # Miles           10mi
    # Speed (avg.)    23mph


    # Stats               1 Day       7 days          30 days
    # ------------------------------------------------------------------------------------

    # Speed (avg.)        23mph       35mph           44mph
    # Miles               5.5mi       124mi           600mi
    # Alt (avg.)          551ft       553ft           556ft

