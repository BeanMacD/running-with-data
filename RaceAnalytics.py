from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import time
from bokeh.charts import Histogram
from bokeh.embed import components
from bokeh.plotting import figure, output_file, show
from bokeh.models.widgets import Button, TextInput, Slider, Dropdown, Select
from bokeh.layouts import widgetbox ,row, column
from bokeh.models import DatetimeTickFormatter
from bokeh.plotting import curdoc
from bokeh.layouts import layout
import sqlite3

def HistogramData():
    with sqlite3.connect('DublinMarathons0.db') as conn:
        cursor = conn.cursor()
        FinishTimes = cursor.execute('Select Race.RaceID, Race.RunnerID, FinishTime.Net_Time, Runner.Gender, Race.AgeCategory from Race Inner join Runner on Race.RunnerID=Runner.RunnerID Inner join FinishTime on Race.RunnerID=FinishTime.RunnerID;')
        Finishdf = pd.DataFrame(FinishTimes.fetchall(), columns=["RaceID", "RunnerID", "FinishTime", "Gender", "AgeCategory"])
        return Finishdf

Histdf = HistogramData()
Hist = figure(title="Finish Times For Runners", plot_width=800, plot_height=300, background_fill_color='#E8DDCB')
Hist.yaxis.axis_label="Number of Runners"
Hist.xaxis.axis_label="Finish Times (Hours)"
Histdf['FinishTime'] = Histdf['FinishTime'].replace("n/a","00:00:00")
Histdf['FinishTime'] = pd.to_datetime(Histdf['FinishTime'], format= '%H:%M:%S').dt.time
histogram, edges = np.histogram([t.hour for t in Histdf.FinishTime], bins=12)
HistPlot = Hist.quad(top=histogram, bottom=0, left=edges[:-1], right=edges[1:], fill_color="#036564", line_color="#033649")

def UpdateHist(attr, old, new):
    Gender = HistGenderSelect.value
    Age = HistAgeSelect.value
    Race = HistRaceSelect.value
    HistTemp = Histdf.copy()
    if Gender!='All':
        HistTemp = HistTemp[HistTemp['Gender']==Gender]
    HistTemp = HistTemp[HistTemp['AgeCategory']==Age]
    HistTemp = HistTemp[HistTemp['RaceID']==Race]
    histogram, edges = np.histogram([t.hour for t in HistTemp.FinishTime], bins=12)
    HistPlot.data_source.data['top']=histogram

def get_sec(time_str):
    h, m, s = time_str.split(':')
    return int(h)*3600 + int(m) * 60 + int(s)

def SplitData():
    with sqlite3.connect('DublinMarathons0.db') as conn:
        cursor = conn.cursor()
        FinishTimes = cursor.execute('Select  Race.RaceID, Runner.RunnerID, Runner.Gender,  Splits.SplitEnd, Splits.Split_Duration, FinishTime.Net_Time, Race.AgeCategory from Splits Inner Join Race on Splits.RunnerID = Race.RunnerID Inner Join Runner on Splits.RunnerID = Runner.RunnerID Inner Join FinishTime on Splits.RunnerID=FinishTime.RunnerID where Splits.Split_Duration <> "n/a";')
        Splitdf = pd.DataFrame(FinishTimes.fetchall(), columns=["RaceID", "RunnerID", "Gender", "Split", "Duration", "FinishTime", "AgeCategory"])
        return Splitdf


Splitdf = SplitData()
Splits=Splitdf["Split"].unique().tolist()
avges = []
for split in Splits:
    df = Splitdf.copy()
    df = df[df['Split']==split]
    time = []
    for value in df['Duration']:
        if "-1 day" in value:
            value="00:00:00"
        time.append(get_sec(value))
    avg = sum(time)/len(time)
    avges.append(avg)
TempSplitdf = pd.DataFrame({'splits':Splits, 'AvgDuration':avges})
TempSplitdf['AvgDuration'] = pd.to_datetime(TempSplitdf["AvgDuration"], unit='s' ).dt.time

SplitFigure = figure(title="Finish Times For Runners", plot_width=800, plot_height=400, background_fill_color='#E8DDCB')
SplitFigure.yaxis.axis_label="Split Time"
SplitFigure.xaxis.axis_label="Km"
SplitFigure.toolbar.logo = None
SplitFigure.toolbar_location = None
SplitFigure.yaxis.formatter=DatetimeTickFormatter(formats=dict(
    seconds=["%H:%M:%S"],
    minsec=["%H:%M:%S"],
    minutes=["%H:%M:%S"],
    hourmin=["%H:%M:%S"],
    hours=["%H:%M:%S"],
    ))
SplitPlot = SplitFigure.line(TempSplitdf['splits'], TempSplitdf['AvgDuration'])

def SplitUpdate(attr, old, new):
    Gender = SplitGenderSelect.value
    Race = SplitRaceSelect.value
    Age = SplitAgeSelect.value
    avges = []
    for split in Splits:
        df = Splitdf.copy()
        if Gender!='All':
            df = df[df['Gender']==Gender]
        elif Gender=='All':
            df = df
        if Race!='All':
            df = df[df['RaceID']==Race]
        elif Race=='All':
            df = df
        if Age!='All':
            df = df[df['AgeCategory']==Age]
        elif Age=='All':
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
    SplitPlot.data_source.data['x']=newdf.splits
    SplitPlot.data_source.data['y']=newdf.AvgDuration
    print(SplitPlot.data_source.data['y'])

Racetypes = Histdf["RaceID"].unique().tolist()
Genders = ['All', 'M', 'F']
Ages = ['All', 'U19', 'S', '35', '40', '45', '50', '55', '60', '65', '70', '75', '80', '85', '90', '95', '100']
SplitRaceSelect = Select(title="Select Race:", options=Racetypes)
SplitGenderSelect = Select(title="Select Gender:", options= Genders)
SplitAgeSelect = Select(title="Select Age: ", options=Ages)
SplitGenderSelect.on_change('value', SplitUpdate)
SplitRaceSelect.on_change('value', SplitUpdate)
SplitAgeSelect = Select(title="Select Age:", options= Ages)
SplitAgeSelect.on_change('value', SplitUpdate)
HistAgeSelect = Select(title="Select Age:", options= Ages)
HistAgeSelect.on_change('value', UpdateHist)
HistRaceSelect = Select(title="Select Race:", options=Racetypes)
HistGenderSelect = Select(title="Select Gender:", options= Genders)
HistGenderSelect.on_change('value',UpdateHist)
HistRaceSelect.on_change('value', UpdateHist)
HistControls = column(HistRaceSelect, HistGenderSelect, HistAgeSelect)
SplitControls = column(SplitRaceSelect, SplitGenderSelect, SplitAgeSelect)
l = layout([
[Hist, HistControls],
[SplitFigure, SplitControls]
])
curdoc().add_root(l)
