#!/usr/bin/python
# CarComputer SSD1306 Display Driver
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
while True:
    try:
        with canvas(device) as draw:
        
            # location.data
            locationInfo = data.getJSONFromDataFile('location.data')
     
            if locationInfo != "":
                draw.text((70, 2), str(int(locationInfo['track'])) + "*", font=titleFont, fill=255)
                draw.text((70, 40), str(data.getHeadingByDegrees(locationInfo['track'])), font=bodyFont, fill=255)
                draw.ellipse((2, 2 , 60, 60), outline=255, fill=0)
                
                # calculate line angle from GPS degrees convert to radians
                degrees = locationInfo['track']
                r = radians(degrees)
                radius = 30
                px = round(32 + radius * sin(r))
                py = round(32 - radius * cos(r))
                draw.line((32, 32, px, py), fill=255)
            else:
                draw.text((10, 5), str('GPS'), font=titleFont, fill=255)
                draw.text((10, 30), str(' Starting'), font=titleFont, fill=255)
    except:
        pass   
    time.sleep(1)
