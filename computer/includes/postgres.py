#!/usr/bin/env python
# postgres save driving stats from local data objects
import time, commands, subprocess, re, psycopg2

# postgresql connection
postgresConn = psycopg2.connect(database="driving_statistics", user="pi", password="password", host="127.0.0.1", port="5432")

def startNewTrip():
    """start new trip entry in the DB"""
    dBCursor = postgresConn.cursor()
    dBCursor.execute("""INSERT INTO driving_stats (time, new_trip_start) VALUES (%s, %s)""", ("now()","now()",))
    postgresConn.commit()

def saveDrivingStats(locationInfo, localeInfo, tempInfo, weatherInfo):
    """save second worth of driving stats to the DB"""
    dBCursor = postgresConn.cursor()
    dBCursor.execute("""INSERT INTO driving_stats (time, gps_latitude, gps_longitude, gps_altitude, gps_speed, gps_climb, gps_track, locale_address, locale_area, locale_city, locale_county, locale_country, locale_zipcode, inside_temp, inside_hmidty, weather_time, weather_summary, weather_icon, weather_apparenttemperature, weather_humidity, weather_precipintensity, weather_precipprobability, weather_windspeed) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", ("now()", str(locationInfo["latitude"]), str(locationInfo["longitude"]), str(locationInfo["altitude"]), str(locationInfo["speed"]), str(locationInfo["climb"]), str(locationInfo["track"]), str(localeInfo["address"]), str(localeInfo["area"]), str(localeInfo["city"]), str(localeInfo["country"]), str(localeInfo["county"]), str(localeInfo["zipcode"]), str(tempInfo["temp"]), str(tempInfo["hmidty"]), str(weatherInfo["time"]), str(weatherInfo["summary"]), str(weatherInfo["icon"]), str(weatherInfo["apparentTemperature"]), str(weatherInfo["humidity"]), str(weatherInfo["precipIntensity"]), str(weatherInfo["precipProbability"]), str(weatherInfo["windSpeed"])))
    postgresConn.commit()
