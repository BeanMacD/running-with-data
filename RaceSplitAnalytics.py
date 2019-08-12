from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import time
from bokeh.models import DatetimeTickFormatter
import datetime
from bokeh.charts import Histogram
from bokeh.embed import components
from bokeh.plotting import figure, output_file, show
from bokeh.models.widgets import Button, TextInput, Slider, Dropdown, Select
from bokeh.layouts import widgetbox ,row, column
from bokeh.plotting import curdoc
from bokeh.layouts import layout
import sqlite3

def get_sec(time_str):
    h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + int(s)

with sqlite3.connect('DublinMarathons0.db') as conn:
    cursor = conn.cursor()
    FinishTimes = cursor.execute('Select  Race.RaceID, Runner.RunnerID, Runner.Gender,  Splits.SplitEnd, Splits.Split_Duration, FinishTime.Net_Time from Splits Inner Join Race on Splits.RunnerID = Race.RunnerID Inner Join Runner on Splits.RunnerID = Runner.RunnerID Inner Join FinishTime on Splits.RunnerID=FinishTime.RunnerID where Splits.Split_Duration <> "n/a";')
    Initialdf = pd.DataFrame(FinishTimes.fetchall(), columns=["RaceID", "RunnerID", "Gender", "Split", "Duration", "FinishTime"])
Splits=Initialdf["Split"].unique().tolist()
avges = []
for split in Splits:
    df = Initialdf.copy()
    df = df[df['Split']==split]
    time = []
    for value in df['Duration']:
        if "-1 day" in value:
            value="00:00:00"
        time.append(get_sec(value))
    avg = sum(time)/len(time)
    avges.append(avg)
tempdf = pd.DataFrame({'splits':Splits, 'AvgDuration':avges})
tempdf['AvgDuration'] = pd.to_datetime(tempdf["AvgDuration"], unit='s' ).dt.time
print(tempdf)

p = figure(plot_width=800, plot_height=400)
p.toolbar.logo = None
p.toolbar_location = None
p.yaxis.formatter=DatetimeTickFormatter(formats=dict(
    seconds=["%H:%M:%S"],
    minsec=["%H:%M:%S"],
    minutes=["%H:%M:%S"],
    hourmin=["%H:%M:%S"],
    hours=["%H:%M:%S"],
    ))
plot = p.line(tempdf['splits'], tempdf['AvgDuration'])

def update(attr, old, new):
    Gender = GenderSelect.value
    Race = RaceSelect.value
    avges = []
    for split in Splits:
        df = Initialdf.copy()
        if Gender!='All':
            df = df[df['Gender']==Gender]
        elif Gender=='All':
            df = df
        if Race!='All':
            df = df[df['RaceID']==Race]
        elif Race=='All':
            df = df
        df = df[df['Split']==split]
        time = []
        for value in df['Duration']:
            if "-1 day" in value:
                value="00:00:00"
            time.append(get_sec(value))
        avg = sum(time)/len(time)
        avges.append(avg)
    newdf = pd.DataFrame({'splits':Splits, 'AvgDuration':avges})
    newdf['AvgDuration'] = pd.to_datetime(newdf["AvgDuration"], unit='s' ).dt.time
    print(newdf)
    plot.data_source.data['x']=newdf.splits
    plot.data_source.data['y']=newdf.AvgDuration

Racetypes = Initialdf["RaceID"].unique().tolist()
Genders = ['All', 'M', 'F']
RaceSelect = Select(title="Select Race:", options=Racetypes)
GenderSelect = Select(title="Select Name:", options= Genders)
GenderSelect.on_change('value',update)
RaceSelect.on_change('value', update)
controls = column(GenderSelect, RaceSelect)
curdoc().add_root(row(p, controls))
