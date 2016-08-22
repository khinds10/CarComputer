import time, datetime, subprocess, json
import string, cgi, subprocess, json
try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk
from tkinterhtml import HtmlFrame
import includes.data as data
import includes.settings as settings

root = tk.Tk()
frame = HtmlFrame(root, horizontal_scrollbar="auto")
frame.grid(sticky=tk.NSEW)

# adjust time in UTC to Eastern Standard Time
timezone=4*60*60

def update_window():

    # get dashboard phone message
    message = ""
    
    # if a dashboard pi project is running, it will show a recent phone message on the screen
    if dashboardServer:
        try:
            phoneDashboardInfo = json.loads(unicode(subprocess.check_output(['curl', "http://" + settings.dashboardServer + "/message"]), errors='ignore'))
            message = str(phoneDashboardInfo["message"])
        except (Exception):
            pass
        
    # get all available info and create HTML output for it    
    try:
        locationInfo = data.getJSONFromDataFile('location.data')
        localeInfo = data.getJSONFromDataFile('locale.data')
        tempInfo = data.getJSONFromDataFile('temp.data')
        weatherInfo = data.getJSONFromDataFile('weather.data')
        drivingStats = data.getJSONFromDataFile('stats.data')
        
        # build frame content with HTML to show driving stats        
        frame.set_content("""
        <!DOCTYPE html>
        <html>
            <head>
                <title>Trip Computer</title>
            </head>
            <body style="background-color: black; color: white; font-family: 'Courier New', Courier, monospace; font-size: 24px; font-weight: bold;">
                <div id="wrap" style="width:800px;margin:0 auto;">
                    <div id="left_col" style="height: 300px;float:left;width:400px;">
                        <h1 style="margin: 0; padding: 0; display:inline;">"""+datetime.datetime.fromtimestamp(time.time()-timezone).strftime('%I:%M%p').lstrip('0')+"""</h1> <h2 style="margin: 0; padding: 0; display:inline;">[""" 
                        + str(int(weatherInfo['apparentTemperature'])) + """&deg;F / """ 
                        + str(int(weatherInfo['humidity']*100)) + """%]</h2>
                        <h2 style="margin: 0; padding: 0; color: #999;">In: """ + str(tempInfo['temp']) + """&deg;F / """ + str(tempInfo['hmidty']) + """%</h2> 
                        <h3>Heading: <span style="color: #FFF4AD;">""" + str(data.getHeadingByDegrees(locationInfo['track'])) + """</span> <br/><span style="color: #999;">&nbsp;&nbsp;&nbsp;&nbsp;Alt. """ + str(int(locationInfo['altitude'])) + """ ft</span></h3>
                        <div style="font-size: 30px;">
                            Driving&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#FFF4AD; font-weight: bolder;">""" + str(drivingStats['drivingTimes'][0]) + """</span> 
                            <br/>Miles&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#BBEDFF;">-- mi</span>
                            <br/>Speed (avg.)&nbsp;&nbsp;&nbsp;<span style="color:#D6FFBB;">""" + str(drivingStats['averageSpeeds'][0]) + """ mph</span>
                            <br/>In Traffic: &nbsp;&nbsp;&nbsp;<span style="color:#FFD5BB;">""" + str(drivingStats['inTrafficTimes'][0]) + """</span>
                        </div>
                    </div>
                    <div id="right_col" style="float:right;height:300px;width:400px; font-style:italic;">
                        <br/>
                        """ + str(weatherInfo['summary']) + """ / """ + str(int(weatherInfo['windSpeed'])) + """ mph<br/>
                        Precip: """ + str(int(weatherInfo['precipProbability']*100)) + """% / Intensity: """ + str(int(weatherInfo['precipIntensity']*100)) + """<br/><br/>
                        """ + str(weatherInfo['nextHour']) + """<br/><br/>
                        """ + str(localeInfo['zipcode']) + """<br/>
                        <br/><br/><span style="color: #999">""" + str(message) + """</span><br/>
                    </div>   
                    <table style="width:100%;">
                      <tr>
                        <th></th>
                        <th style="text-align: left; color: #999;">1 Day</th>
                        <th style="text-align: left; color: #999;">7 Days</th>
                        <th style="text-align: left; color: #999;">30 Days</th>
                      </tr>
                      <tr>
                        <td>Driving</td>
                        <td>""" + str(drivingStats['drivingTimes'][1]) + """</td>
                        <td>""" + str(drivingStats['drivingTimes'][2]) + """</td>
                        <td>""" + str(drivingStats['drivingTimes'][3]) + """</td>
                      </tr>
                      <tr>
                        <td>Traffic</td>
                        <td>""" + str(drivingStats['inTrafficTimes'][1]) + """</td>
                        <td>""" + str(drivingStats['inTrafficTimes'][2]) + """</td>
                        <td>""" + str(drivingStats['inTrafficTimes'][3]) + """</td>
                      </tr>
                      <tr>
                        <td>Speed (avg.)</td>
                        <td>""" + str(drivingStats['averageSpeeds'][1]) + """ mph</td>
                        <td>""" + str(drivingStats['averageSpeeds'][2]) + """ mph</td>
                        <td>""" + str(drivingStats['averageSpeeds'][3]) + """ mph</td>
                      </tr>
                      <tr>
                        <td>Miles</td>
                        <td>-- mi</td>
                        <td>-- mi</td>
                        <td>-- mi</td>
                      </tr>
                      <tr>
                        <td>Alt (avg.)</td>
                        <td>""" + str(drivingStats['averageAltitude'][1]) + """ ft</td>
                        <td>""" + str(drivingStats['averageAltitude'][2]) + """ ft</td>
                        <td>""" + str(drivingStats['averageAltitude'][3]) + """ ft</td>
                      </tr>
                    </table>
                </div>
            </body>
        </html>
        """)
    except (Exception):
        frame.set_content("""<!DOCTYPE html><html><head><title>Trip Computer</title></head><body style="background-color: black; color: white; font-family: 'Courier New', Courier, monospace; font-size: 24px; font-weight: bold;">Waiting for data...</body></html>""")
    root.after(1000, update_window)

root.title("Trip Computer")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
root.after(1000, update_window)
root.mainloop()
