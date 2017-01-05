#!/usr/bin/python
# Kevin Hinds http://www.kevinhinds.com
# License: GPL 2.0
import json
class ButtonPressed:
    '''save to file which button was pressed for other processes to read'''
    buttonName = ''
    
    def __init__(self):
        self.buttonName = ''
        
    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,sort_keys=True, indent=4)
