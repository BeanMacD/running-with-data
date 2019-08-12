from flask import Flask, render_template, request
import pandas as pd
from bokeh.charts import Histogram
from bokeh.embed import components
from bokeh.plotting import figure, output_file, show
from bokeh.models.widgets import Button, TextInput, Slider, Dropdown, Select
from bokeh.layouts import widgetbox ,row, column
from bokeh.plotting import curdoc
from bokeh.layouts import layout
import time
import datetime
from bokeh.models import DatetimeTickFormatter
import sqlite3

def get_sec(time_str):
    h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + int(s)


def FinishLineData():
    with sqlite3.connect('DisneyDB2.db') as conn:
        RunnerID='macdonagh1995'
        cursor = conn.cursor()
        FinishTimes = cursor.execute('Select FinishTime.RaceID, Net_Time, RaceDetails.Year, RaceDetails.RaceType from FinishTime Inner Join RaceDetails on FinishTime.RaceID = RaceDetails.RaceID where RunnerID=?;', [RunnerID])
        Finishdf = pd.DataFrame(FinishTimes.fetchall(), columns=["RaceID", "FinishTime", "Year", "RaceType"])
        return Finishdf

Finishdf = FinishLineData()
Finishdf['FinishTime'] = pd.to_datetime(Finishdf['FinishTime'],format= '%H:%M:%S' ).dt.time
Finishp = figure(plot_width=800, plot_height=300, title="Runner Finish Times vs Year")
Finishp.yaxis.formatter = DatetimeTickFormatter(formats=dict(hourmin = ['%H:%M:%S']))
Finishp.toolbar.logo = None
Finishp.toolbar_location = None
Finishp.background_fill_color = "whitesmoke"
Finishp.border_fill_color = "whitesmoke"
Finishplot = Finishp.line(x=Finishdf.Year, y=Finishdf.FinishTime)
Finishplot2 = Finishp.circle(Finishdf.Year, Finishdf.FinishTime)
Finishp.yaxis.axis_label="FinishTime"
Finishp.xaxis.axis_label="Year"

def updateFinish(attr, old, new):
    Rtype = Finishselect.value
    Finishtemp = Finishdf.copy()
    Finishtemp['FinishTime'] = pd.to_datetime(Finishtemp['FinishTime'],format= '%H:%M:%S' ).dt.time
    Finishtemp = Finishtemp[Finishtemp['RaceType']==Rtype]
    Finishplot.data_source.data['y']=Finishtemp['FinishTime']
    Finishplot2.data_source.data['y']=Finishtemp['FinishTime']
    Finishplot.data_source.data['x']=Finishtemp['Year']
    Finishplot2.data_source.data['x']=Finishtemp['Year']

def AvgPaceData():
    with sqlite3.connect('DisneyDB2.db') as connection:
        RunnerID='macdonagh1995'
        newcursor = connection.cursor()
        FinishTimes = newcursor.execute('Select Net_Time, RaceDetails.Year, RaceDetails.RaceType from FinishTime Inner Join RaceDetails on FinishTime.RaceID = RaceDetails.RaceID where RunnerID=?;', [RunnerID])
        temp = FinishTimes.fetchall()
        return temp
temp = AvgPaceData()
AvgPace = []
for row in temp:
    if row[2]=="Marathon":
        AvgPace.append(time.strftime('%M:%S', time.gmtime(get_sec(row[0])/42.2)))
    elif row[2]=="HalfMarathon":
        AvgPace.append(time.strftime('%M:%S', time.gmtime(get_sec(row[0])/21.1)))
    elif row[2]=="10K":
        AvgPace.append(time.strftime('%M:%S', time.gmtime(get_sec(row[0])/10)))
    elif row[2]=="5K":
        AvgPace.append(time.strftime('%M:%S', time.gmtime(get_sec(row[0])/5)))
    else:
        AvgPace.append(time.strftime('%M:%S', time.gmtime(0)))

TimeDf = pd.DataFrame(AvgPace, columns=["AvgPace"])
TimeDf.AvgPace = pd.to_datetime(TimeDf["AvgPace"], format='%M:%S').dt.time
print(TimeDf.AvgPace)
Avgdf = pd.DataFrame(temp, columns=["FinishTime", "Year", "RaceType"])
Avgdf['AvgPace'] = TimeDf.AvgPace
Racetypes = Avgdf["RaceType"].unique().tolist()
AvgPlot = figure(y_range=Racetypes, x_axis_type='datetime',  plot_width=300, plot_height=200, title="Average Pace per Km")
AvgPlot.border_fill_color = "whitesmoke"
AvgPlot.background_fill_color = "whitesmoke"
Bar = AvgPlot.hbar(y=Avgdf.RaceType, right=Avgdf.AvgPace, height=0.5, color="#3498DB")
AvgPlot.yaxis.axis_label="RaceType"
AvgPlot.xaxis.axis_label="AvgPace"
AvgPlot.toolbar.logo = None
AvgPlot.toolbar_location = None

def UpdateAvgPlot(attr, old, new):
    year =  Avgselect.value
    temp = Avgdf.copy()
    temp = temp[temp['Year'] == year]
    Bar.data_source.data['y']=temp.RaceType
    Bar.data_source.data['right']=temp.AvgPace
    print(temp.AvgPace)

def AmountData():
    with sqlite3.connect('DisneyDB2.db') as conn:
        RunnerID='macdonagh1995'
        cursor = conn.cursor()
        Years = cursor.execute('Select distinct(RaceDetails.Year) from Race Inner Join RaceDetails on Race.RaceID=RaceDetails.RaceID where RunnerID="macdonagh1995";')
        Yeardf = pd.DataFrame(Years.fetchall(), columns=["Year"])
        data=[]
        for year in Yeardf["Year"]:
            row = cursor.execute('select RaceDetails.RaceType, count(RaceDetails.RaceType) from Race Inner Join RaceDetails on Race.RaceID=RaceDetails.RaceID where RunnerID="macdonagh1995" and RaceDetails.Year=? Group by RaceDetails.RaceType;', [int(year)])
            for element in row:
                data.append([year, element[0], element[1]])
        Total = cursor.execute('select RaceDetails.RaceType, count(RaceDetails.RaceType) from Race Inner Join RaceDetails on Race.RaceID=RaceDetails.RaceID where RunnerID="macdonagh1995" Group by RaceDetails.RaceType;')
        res = Total.fetchall()
        totals = []
        for el in res:
            totals.append(["Total", el[0], el[1]])
        df1 = pd.DataFrame(totals, columns=["Year", "RaceType", "Amount"])
        df = pd.DataFrame(data, columns=["Year", "RaceType", "Amount"])
        frames = [df, df1]
        result = pd.concat(frames)
        return result

result = AmountData()
result.Year=result.Year.astype(str);
Races = ['Marathon', 'HalfMarathon', '10K', '5K']
AmountPlot = figure(x_range=Races, plot_width=300, plot_height=200, title="Races Ran")
AmountPlot.border_fill_color = "whitesmoke"
AmountPlot.background_fill_color = "whitesmoke"
AmountPlot.yaxis.axis_label="Amount"
AmountPlot.xaxis.axis_label="RaceType"
AmountPlot.toolbar.logo = None
AmountPlot.toolbar_location = None
VBar1 = AmountPlot.vbar(x=result['RaceType'], width=0.5, bottom=0, top=result['Amount'], color="#3498DB")

def update_VBarPlot(attr, old, new):
    year =  Amountselect.value
    temp = result.copy()
    temp = temp[temp['Year'] == year]
    print(temp)
    VBar1.data_source.data['x']=temp['RaceType']
    VBar1.data_source.data['top']=temp['Amount']



types = Finishdf["RaceType"].unique().tolist()
Finishselect = Select(options= types)
Finishselect.on_change('value',updateFinish)
Avgdf.Year=Avgdf.Year.astype(str);
years = Avgdf.Year.unique().tolist()
Avgselect = Select(options= years)
Avgselect.on_change('value',UpdateAvgPlot)
Amountselect = Select(options= years)
Amountselect.on_change('value',update_VBarPlot)
Avgcontrols = column(Avgselect)
Amountcontrols = column(Amountselect)
FinishControls = column(Finishselect)
l = layout([
[Finishp, FinishControls],
[AvgPlot, Avgcontrols, AmountPlot, Amountcontrols],
])
curdoc().add_root(l)
