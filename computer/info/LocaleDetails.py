#!/usr/bin/python
# Current location specific information 
# Kevin Hinds http://www.kevinhinds.com
# License: GPL 2.0
import json
class LocaleDetails:
    '''Locale Information as class to persist as JSON information to file'''
    address = ''
    area = ''
    city = ''
    zipcode = ''
    county = ''
    country = ''
    
    def __init__(self):
        self.address = ''
        self.area = ''
        self.city = ''
        self.zipcode = ''
        self.county = ''
        self.country = ''
        
    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,sort_keys=True, indent=4)
