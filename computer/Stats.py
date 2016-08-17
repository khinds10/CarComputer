#!/usr/bin/python
# Kevin Hinds http://www.kevinhinds.com
# License: GPL 2.0
import os, time, json
import includes.data as data

# remove stats data and start calculating
data.removeJSONFile('stats.data')
while True:
   

#
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
 # weather_time                | timestamp without time zone | 
 #weather_summary             | text                        | 
 #weather_icon                | text                        | 
 #weather_apparenttemperature | real                        | 
 #weather_humidity            | real                        | 
 #weather_precipintensity     | real                        | 
 #weather_precipprobability   | real                        | 
 #weather_windspeed           | real                        | 


    time.sleep(60)
