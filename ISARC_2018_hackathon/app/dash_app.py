# standard library
from collections import namedtuple
import io
import os
import numpy as np
import pandas as pd
from time import time
import pickle

# plot.ly modules
import dash
from dash.dependencies import Output, Event
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go




app = dash.Dash()

app.layout = html.Div(children = [
    dcc.Graph(
        id='live-graph', 
    ),
    dcc.Interval(
        id='interval-component',
        interval=1*1000  # in milliseconds
    )
])


@app.callback(Output('live-graph', 'figure'),
              events=[Event('interval-component', 'interval')])
def update_graph():
#    result = get_data('data/data.csv', nlines=200)
    model = pickle.load(open("speed_model.dat", "rb"))
    features_speed = ['lat','long','co','no2','o3','pm10','pm25','so2','co_normal','no2_normal','o3_normal','pm10_normal','pm25_normal','so2_normal']
    df = pd.read_csv('data/group_40.665790_73.757060_normalized.csv')
    t = time()
    i = int(t)%60
    x_axis = [t,t+1,t+2,t+3,t+4,t+5,t+6,t+7,t+8,t+9]
    results = df.iloc[i:i+10]
    pred = model.predict(results[features_speed].values)
    return {
        'data': [
                go.Scatter(
                    x=x_axis,
                    y=results.pm25,
                    xaxis = 'x2',
                    yaxis = 'y2',
                    name = 'Particulate Matter (pm25)'
                ),
                go.Scatter(
                    x=x_axis,
                    y=results.speed,
                    name = 'Actual Speed'
                ),
                go.Scatter(
                    x=x_axis,
                    y=pred,
                    name = 'Predicted Speed'
                )
                  
        ],
        'layout': go.Layout(#title = 'Actual and Predicted Traffic Speed in New York',
#              xaxis = dict(title = 'Time (s)'),
#              yaxis = dict(title = 'Speed (km/h)'),
                  xaxis=dict(
                        domain=[0.55, 1]
                    ),
                    yaxis=dict(
                        domain=[0, 0.45],
                        anchor = 'x2'
                    ),
                    xaxis2=dict(
                        domain=[0, 0.45]
                    ),
                    yaxis2=dict(
                        domain=[0, 0.45]
                    )
              )
        
    }


if __name__ == '__main__':
    app.run_server(host='0.0.0.0',debug=True)
