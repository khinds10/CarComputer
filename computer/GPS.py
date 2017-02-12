#! /usr/bin/python
# Get GPS readings and save to file
# Kevin Hinds http://www.kevinhinds.com / Dan Mandle http://dan.mandle.me
# License: GPL 2.0
import os, time, threading, pprint, json, math
import includes.postgres as postgres
from gps import *
import includes.data as data
import info.GPSInfo as GPSInfo
pp = pprint.PrettyPrinter(indent=4)

# setting the global variable
gpsd = None 

# start a new trip by inserting the new trip DB entry
postgres.startNewTrip()
data.removeJSONFile('location.data')

class GpsPoller(threading.Thread):
  '''create a threaded class for polling on the GPS sensor '''
  
  def __init__(self):
    threading.Thread.__init__(self)
    global gpsd
    
    # starting the stream of info
    gpsd = gps(mode=WATCH_ENABLE)
    self.current_value = None
    self.running = True

  def run(self):
    '''this will continue to loop and grab EACH set of gpsd info to clear the buffer'''
    global gpsd
    while gpsp.running:
      gpsd.next() 

if __name__ == '__main__':

    # create the thread & start it up
    gpsp = GpsPoller()
    try:
        gpsp.start()
        while True:
            try:
                # save JSON object of GPS info to file system
                gpsInfo = GPSInfo.GPSInfo()
                gpsInfo.latitude = float(gpsd.fix.latitude)
                gpsInfo.longitude = float(gpsd.fix.longitude)
                gpsInfo.track = float(gpsd.fix.track)

                # convert to imperial units
                gpsInfo.altitude = float(gpsd.fix.altitude * 3.2808)
                gpsInfo.climb = float(gpsd.fix.climb * 3.2808)
                
                # correct for bad speed value on the device
                #   also save to last location because it must be good with a valid speed present
                gpsInfo.speed = float(gpsd.fix.speed)
                if (gpsInfo.speed > 5):
                    gpsInfo.speed = gpsInfo.speed * 2.25
                    data.saveJSONObjToFile('last-location.data', gpsInfo)
                
                # create or rewrite data to GPS location data file as JSON
                data.saveJSONObjToFile('location.data', gpsInfo)
                time.sleep(1)
            
            except (Exception):
                pass
    except (KeyboardInterrupt, SystemExit):
        print "\nKilling Thread..."
        gpsp.running = False
        gpsp.join()
        print "Done.\nExiting."
