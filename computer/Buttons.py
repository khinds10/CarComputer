#!/usr/bin/python
# Read in any button presses from LCD plate
import Adafruit_CharLCD as LCD
import includes.postgres as postgres
import includes.data as data

# Initialize the LCD using the pins and the mapped buttons you can press
lcd = LCD.Adafruit_CharLCDPlate()
buttons = ((LCD.SELECT, 'Select'), (LCD.LEFT, 'Left'), (LCD.UP, 'Up'), (LCD.DOWN, 'Down'),(LCD.RIGHT, 'Right'))

class Button:
    '''Button pressed as a class to persist to data file'''
    name = 'Down'
    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,sort_keys=True, indent=4)

# reset what button was pressed and start waiting for button press
myButton = Button()
saveButtonClick('Down')

def saveButtonClick(buttonPressed):
    '''save which button was pressed to file'''
    myButton.name = buttonPressed
    data.saveJSONObjToFile('button.data', myButton)

# Loop through each button and save to file if any of them are pressed
while True:
    for button in buttons:
        if lcd.is_pressed(button[0]):
        
            # 'Select' button pressed, reset the trip meter by inserting the new trip DB entry
            if button[1] == 'Select':
                postgres.startNewTrip()
            else:
                # 'Left', show locale info, 'Up', show weather info, 'Down', show default driving status view, 'Right', show full stats view
                saveButtonClick(button[1])
