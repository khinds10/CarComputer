#!/usr/bin/python
# Show current travel direction as compass reading to ssd1306 display
# @author khinds
# @license http://opensource.org/licenses/gpl-license.php GNU Public License
from math import cos, sin, pi, radians
from oled.device import ssd1306, sh1106
from oled.render import canvas
from PIL import ImageFont
import time
import includes.data as data
 
# define fonts
font = ImageFont.load_default()
titleFont = ImageFont.truetype('/home/pi/CarComputer/computer/fonts/DroidSansMono.ttf', 20)
bodyFont = ImageFont.truetype('/home/pi/CarComputer/computer/fonts/TheNextFont.ttf', 24)

# device and screen settings
device = ssd1306()
displayIterations = 3
iteration = 0
currentDirection = 0
while True:
    try:
        with canvas(device) as draw:
        
            # location.data
            locationInfo = data.getJSONFromDataFile('location.data')
            if locationInfo != "":
                        
                # calculate line angle from GPS degrees convert to radians, but only if we're moving more than 5mph
                if (int(locationInfo['speed']) > 5):
                    currentDirection = locationInfo['track']
                draw.text((70, 2), str(int(currentDirection)) + "*", font=titleFont, fill=255)
                draw.text((70, 40), str(data.getHeadingByDegrees(currentDirection)), font=bodyFont, fill=255)
                draw.ellipse((2, 2 , 60, 60), outline=255, fill=0)       
                r = radians(currentDirection)
                radius = 30
                px = round(32 + radius * sin(r))
                py = round(32 - radius * cos(r))
                draw.line((32, 32, px, py), fill=255)
            else:
                draw.text((10, 5), str('GPS'), font=titleFont, fill=255)
                draw.text((10, 30), str(' Searching'), font=titleFont, fill=255)
    except:
        pass   
    time.sleep(1)
