
from flask import Flask,render_template, url_for, request,redirect,jsonify
import imgkit
import datetime
from dateutil.parser import parse
from dateutil import rrule
import math
import numpy as np
from datetime import timedelta
import pandas as pd
import os
from subprocess import call
from dateutil.parser import parse as date_parse
import pyrebase
import urllib
import re




"""
Create ngrok with following command:
    

./ngrok http <port-number of localhost the app is running on>
    
    
"""

#num_run_last_week = 2
#average_run_time_last_week = 60
#goal_run_km = 10
#goal_date = '2018-11-13'
#max_week_hours = 6
#ser_id = 'user_id'





def weeks_between(start_date, end_date):
    weeks = rrule.rrule(rrule.WEEKLY, dtstart=start_date, until=end_date)
    return weeks.count()


def get_tss_value(week_hours):
    return week_hours * 50


def hours_from_tss(tss_score):
    hours = tss_score / 50
    minutes = hours * 60
    return '%.2f' % (roundTo15(minutes) / 60.0)


def roundTo15(x, base=15):
    return int(base * math.ceil(float(x) / base))


def get_peak_tss_weekly(current_tss, ramp_rate_cycle, max_tss, cycles_remain):
    a = list(
        np.arange(current_tss + ramp_rate_cycle, max_tss, ramp_rate_cycle))
    extra = [max(a)] * (cycles_remain - len(a))
    a.extend(extra)
    max_values = np.array(a)
    return max_values


def get_timerange_weekly(start_time: datetime.datetime,
                         end_time: datetime.datetime):
    start = start_time + timedelta(days=(7 - start_time.weekday()))
    end = end_time - timedelta(days=end_time.weekday())
    return rrule.rrule(rrule.WEEKLY, dtstart=start.date(), until=end.date())

def save_as_table(df):
    import matplotlib.pyplot as plt
    import pandas as pd
    from pandas.tools.plotting import table

    ax = plt.subplot(111, frame_on=False)  # no visible frame
    ax.xaxis.set_visible(False)  # hide the x axis
    ax.yaxis.set_visible(False)  # hide the y axis

    table(ax, df)  # where df is your data frame

    plt.savefig('mytable.png')

def get_schedule(response_dict):
    num_run_last_week = response_dict["run_last_week"]
    average_run_time_last_week = response_dict["time_per_run"]
    goal_run_km = response_dict["distance_goal"]
    goal_date = response_dict["date_goal"]
    max_week_hours = response_dict["time_per_week"]
    user_id = response_dict["chatfuel+user+id"]
  
    if(num_run_last_week == 0):
        num_run_last_week = 1
    
    end_date = goal_date
    max_ramp_rate = 8
    weeks_in_cycle = 3
    current_week_hours = (num_run_last_week * average_run_time_last_week) / 60
    current_date = datetime.datetime.now()
#    end_date = parse(goal_date)
    current_tss = get_tss_value(current_week_hours)
    max_tss = get_tss_value(max_week_hours)
    weeks_remain = weeks_between(current_date, end_date)
    ramp_rate_needed = (max_tss - current_tss) / weeks_remain
    if ramp_rate_needed > max_ramp_rate:
        print('Warning, ramp rate too high')
    cycles_remain = int(math.floor(weeks_remain / weeks_in_cycle))
    ramp_rate_cycle = weeks_in_cycle * max_ramp_rate

    peak_values = get_peak_tss_weekly(current_tss, ramp_rate_cycle, max_tss,
                                      cycles_remain)
    print('cycles remain', cycles_remain)
    peak_values = peak_values[0:int(cycles_remain)]
    peak_phase = ['Build'] * len(peak_values)
    base_values = [current_tss] * int(len(peak_values))
    base_phase = ['Recover'] * len(base_values)
    mid_values = np.mean([peak_values, base_values], axis=0)
    mid_phase = ['Train'] * len(mid_values)

    cycle_names = list(zip(mid_phase, peak_phase, base_phase))
    cycle_values = list(zip(mid_values, peak_values, base_values))

    tss_values = [i for sub in cycle_values for i in sub]
    phases = [i for sub in cycle_names for i in sub]

    train_hours = [float(hours_from_tss(t)) for t in tss_values]

    week_range = list(get_timerange_weekly(current_date, end_date))
    week_range = week_range[0:len(tss_values)]

    overall_data = {
        'Week': week_range,
        'Phase': phases,
        'TSS': tss_values,
        'Train Hours': train_hours,
    }
    df = pd.DataFrame(overall_data)
    print(df)
    fname = os.path.join(os.getcwd(), '%s.html' % user_id)
    html_string = df.to_html(columns=['Week', 'Phase', 'TSS', 'Train Hours'], index=False, justify='center')
    style = """
    <style>
        table {
            border-collapse: collapse;
        }
        
        th, td {
            text-align: left;
            padding: 8px;
        }
        
        tr:nth-child(even){background-color: #d6edf9}
        
        th {
            background-color: #1fc0df;
            color: white;
        }
        </style>
    """
    html_string = html_string + style
    html_string = html_string.replace('border="1"',"")
    with open(fname, 'w') as f:
        f.write(html_string)
    options = {
        'format': 'jpg',
        'width': '350'
        #'encoding': "UTF-8",
    }
    imgfile = os.path.join(os.getcwd(), '%s.jpg' % user_id)
    imgkit.from_file(fname, imgfile,options=options)
    return(imgfile)






app = Flask(__name__)
#@app.route("/")
#def main():
#    return render_template('send_url.html')


def upload_image(path,name):
    config = {
        "apiKey": "AIzaSyBMCfKCPdUQNFMOMe5VnE7KH2dgqiHS5eo",
        "authDomain": "robocoach-5c23c.firebaseapp.com",
        "databaseURL": "https://robocoach-5c23c.firebaseio.com",
        "projectId": "robocoach-5c23c",
        "storageBucket": "robocoach-5c23c.appspot.com",
        "messagingSenderId": "557442657611"}
    image_name = path
    firebase = pyrebase.initialize_app(config)
    storage = firebase.storage()
    feed_back_data = storage.child("images/{}".format(name)).put("{}".format(image_name)   , "jLvU3HNT1iOChPvsKAA93iZxR902")
    url = storage.child("images/{}".format(name)).get_url(feed_back_data['downloadTokens'])
    # write url in an external file
    return(url)

def parse_res(s):
    response_string = s.split('&')
    response_dict = {}
    for ind,val_temp in enumerate(response_string):
        print(ind,val_temp)
        val = val_temp.split("=")
        if(val[0]=='gender' or val[0]=='chatfuel+user+id'):
            response_dict[val[0]] = val[1]
        elif(val[0]=='time_per_run'):
            response_dict[val[0]] = int(val[1].split("+")[0])
        elif(val[0]=='time_per_week'):
            response_dict[val[0]] = int(val[1].split("hours")[0].split('+')[-2])
        elif(val[0]=='date_goal'):
            response_dict[val[0]] = date_parse(urllib.parse.unquote(val[1]))          
        elif(val[0]=='distance_goal'):
            response_dict[val[0]] = int(val[1].split("+")[0])
        elif(val[0]=='run_last_week'):
            if("-" in val[1].split("+")[0]):                
                response_dict[val[0]] = int(val[1].split("+")[0].split('-')[1])                       
            else:
                response_dict[val[0]] = int(val[1].split("+")[0])                       
    return response_dict

#num_run_last_week = 2
#average_run_time_last_week = 60
#goal_run_km = 10
#goal_date = '2018-11-13'
#max_week_hours = 6
#user_id = 'user_id'



@app.route('/getData', methods = ['GET', 'POST', 'PATCH', 'PUT', 'DELETE'])
def getData():
    # here we want to get the value of user (i.e. ?url=some-value)
#    key_name = list(request.args)
#    print(request.args['data_1'])
#    print(url_address['URL'])
#    return('',204)
    
    if request.method == 'GET':
        print(request.args['time_per_week'])
        print(request.args['gender'])
        return(request.args['data_1'])

    elif request.method == 'POST':
        print(request.headers['Content-Type'])
#        if request.headers['Content-Type'] == 'text/plain':
#            print(request.data)
#            return "Text Message: " + request.data

#        elif request.headers['Content-Type'] == 'application/json':
#            print(json.dumps(request.json))
#            return "JSON Message: " + json.dumps(request.json)

#        elif request.headers['Content-Type'] == 'application/octet-stream':
#            f = open('./binary', 'wb')
#            f.write(request.data)
#            f.close()
#            print(request.data)
#            return "Binary message written!"
#        elif(request.headers['Content-Type'] == 'application/x-www-form-urlencoded'):
#            print(request.body)
#            print("here is the shit")
#           print(request.form.keys()[0])
        print(request.get_data().decode())
        value = parse_res(request.get_data().decode())
        path = get_schedule(value)
        print(path)
        name = path.split("/")[-1]
        print(name)
        url = upload_image(path,name)
        print(url)
        # if true send image
        message ={
                  "messages": [
                    {
                      "attachment": {
                        "type": "image",
                        "payload": {
                          "url":url
                        }
                      }
                    }
                  ]
                }
        
        return(jsonify(message))

 #       else:
 #           return "415 Unsupported Media Type ;)"
    




    
    
    
if __name__ == '__main__':
      app.run(host='0.0.0.0', port=2222,debug=True)
      
      
      