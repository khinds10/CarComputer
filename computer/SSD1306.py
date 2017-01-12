#!/usr/bin/python
# CarComputer SSD1306 Display Driver
# @author khinds
# @license http://opensource.org/licenses/gpl-license.php GNU Public License

from oled.device import ssd1306, sh1106
from oled.render import canvas
from PIL import ImageFont
import psutil 
import time, commands, subprocess, re

# define fonts
font = ImageFont.load_default()
titleFont = ImageFont.truetype('/home/pi/CarComputer/computer/fonts/DroidSansMono.ttf', 20)
bodyFont = ImageFont.truetype('/home/pi/CarComputer/computer/fonts/DroidSansMono.ttf', 16)

# device and screen settings
device = ssd1306()
displayIterations = 3

def drawTextOnLine(line, text, font, draw):
    """for given line and text and font, draw the text on the screen"""
    xAxis = 0
    yAxis = 16 * (line-1)
    draw.text((xAxis, yAxis), str(text), font=font, fill=255)
    pass

iteration = 0
while True:
    try:
        with canvas(device) as draw:
            drawTextOnLine(1, str("CarComputer"), titleFont, draw)
            drawTextOnLine(2, str("CarComputer"), bodyFont, draw)
            drawTextOnLine(3, str("CarComputer"), bodyFont, draw)
            drawTextOnLine(4, str("CarComputer"), bodyFont, draw)
    except:
        pass   
    time.sleep(1)
