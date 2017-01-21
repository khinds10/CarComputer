#!/usr/bin/python
# CarComputer SSD1306 Display Driver
# @author khinds
# @license http://opensource.org/licenses/gpl-license.php GNU Public License
import time
from math import cos, sin, pi, radians
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

# Raspberry Pi pin configuration:
RST = 24

# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

# 128x64 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing / Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# First define some constants to allow easy resizing of shapes.
padding = 2
shape_width = 55
top = padding
bottom = height-padding

# Move left to right keeping track of the current x position for drawing shapes.
x = padding

# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)

# Draw an ellipse.
draw.ellipse((x, top , x+60, bottom), outline=255, fill=0)
x += shape_width+padding

# calculate line angle from GPS degrees convert to radians
degrees = 200
r = radians(degrees)
radius = 30
px = round(32 + radius * sin(r))
py = round(32 - radius * cos(r))
draw.line((32, 32, px, py), fill=255)

# Load default font.
font = ImageFont.load_default()

# Alternatively load a TTF font.  Make sure the .ttf font file is in the same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
font = ImageFont.truetype('TheNextFont.ttf', 24)

# Write two lines of text.
draw.text((x+8, top+40),    'SSW',  font=font, fill=255)

# Display image.
disp.image(image)
disp.display()
