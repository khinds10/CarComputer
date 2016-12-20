#!/usr/bin/python
# Kevin Hinds http://www.kevinhinds.com
# License: GPL 2.0
import datetime as dt
import time, json, string, cgi, subprocess, json

# clear and rotate screen
#subprocess.call(["/home/pi/CarComputer/computer/digole", "clear"])
subprocess.call(["/home/pi/CarComputer/computer/digole", "setRot90"])


subprocess.call(["/home/pi/CarComputer/computer/digole", "setColor", "0"])
subprocess.call(["/home/pi/CarComputer/computer/digole", "setFont", "123"])

subprocess.call(["/home/pi/CarComputer/computer/digole", "printxy_abs", "0", "0", "##############################################################################################"])

exit()

subprocess.call(["/home/pi/CarComputer/computer/digole", "setColor", "255"])


# make a function that doesn't have to clear the screen just writes empty spaces over the whole screen???




# show weather / phone summary
subprocess.call(["/home/pi/CarComputer/computer/digole", "setFont", "51"])
subprocess.call(["/home/pi/CarComputer/computer/digole", "printxy_abs", "5", "75", "Sunshine for the hour"])

# inside/outside tempurature
subprocess.call(["/home/pi/CarComputer/computer/digole", "setFont", "120"])
subprocess.call(["/home/pi/CarComputer/computer/digole", "setColor", "249"])
subprocess.call(["/home/pi/CarComputer/computer/digole", "printxy_abs", "5", "35", "131*F 18%"])
subprocess.call(["/home/pi/CarComputer/computer/digole", "setColor", "240"])
subprocess.call(["/home/pi/CarComputer/computer/digole", "printxy_abs", "150", "35", "[164*F 23%]"])

# driving times
subprocess.call(["/home/pi/CarComputer/computer/digole", "setColor", "28"])
subprocess.call(["/home/pi/CarComputer/computer/digole", "printxy_abs", "5", "125", "1h28m"])
subprocess.call(["/home/pi/CarComputer/computer/digole", "setColor", "252"])
subprocess.call(["/home/pi/CarComputer/computer/digole", "printxy_abs", "110", "125", "1h28m [Traffic]"])

# compass
subprocess.call(["/home/pi/CarComputer/computer/digole", "setColor", "255"])
subprocess.call(["/home/pi/CarComputer/computer/digole", "printxy_abs", "5", "175", "\ NW"])

# MPH and distance travelled
subprocess.call(["/home/pi/CarComputer/computer/digole", "setColor", "250"])
subprocess.call(["/home/pi/CarComputer/computer/digole", "printxy_abs", "105", "175", "22mph [Avg]"])
subprocess.call(["/home/pi/CarComputer/computer/digole", "setColor", "222"])
subprocess.call(["/home/pi/CarComputer/computer/digole", "printxy_abs", "150", "225", "65.4 mi [Est]"])
