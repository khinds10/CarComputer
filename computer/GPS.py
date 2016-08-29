#! /usr/bin/python
# Kevin Hinds http://www.kevinhinds.com / Dan Mandle http://dan.mandle.me
# License: GPL 2.0
import os, time, threading, pprint, json
import includes.postgres as postgres
from gps import *
import includes.data as data
pp = pprint.PrettyPrinter(indent=4)

# setting the global variable
gpsd = None 

# start a new trip by inserting the new trip DB entry
postgres.startNewTrip()

# remove data and start logging GPS
data.removeJSONFile('location.data')

class GPSInfo:
    '''GPS info as class to persist as JSON information to file'''
    latitude = 0
    longitude = 0
    altitude = 0
    speed = 0
    climb = 0
    track = 0
    mode = 0
    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,sort_keys=True, indent=4)

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
        
            # save JSON object of GPS info to file system
            gpsInfo = GPSInfo()
            gpsInfo.latitude = float(gpsd.fix.latitude)
            gpsInfo.longitude = float(gpsd.fix.longitude)
            gpsInfo.track = float(gpsd.fix.track)

            # convert to imperial units
            gpsInfo.altitude = float(gpsd.fix.altitude * 3.2808)
            
            # correct for bad speed value on the device?
            gpsInfo.speed = float(gpsd.fix.speed)
            if (gpsInfo.speed > 5):
                gpsInfo.speed = gpsInfo.speed * 2.25
            gpsInfo.climb = float(gpsd.fix.climb * 3.2808)

            # create or rewrite data to GPS location data file as JSON
            data.saveJSONObjToFile('location.data', gpsInfo)
            time.sleep(1)

    except (KeyboardInterrupt, SystemExit):
        print "\nKilling Thread..."
        gpsp.running = False
        gpsp.join()
        print "Done.\nExiting."
