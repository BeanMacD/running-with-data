from flask import Flask, render_template, request
import pandas as pd
from bokeh.charts import Histogram
from bokeh.embed import components
from bokeh.plotting import figure, output_file, show
from bokeh.models.widgets import Button, TextInput, Slider, Dropdown, Select
from bokeh.layouts import widgetbox ,row, column
from bokeh.plotting import curdoc
import sqlite3

app = Flask(__name__)

def get_sec(time_str):
    h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + int(s)


with sqlite3.connect('DisneyDB2.db') as conn:
    RunnerID='macdonagh1995'
    cursor = conn.cursor()
    FinishTimes = cursor.execute('Select Net_Time, RaceDetails.Year, RaceDetails.RaceType from FinishTime Inner Join RaceDetails on FinishTime.RaceID = RaceDetails.RaceID where RunnerID=?;', [RunnerID])
    temp = FinishTimes.fetchall()
AvgPace = []
for row in temp:
    if row[2]=="Marathon":
        AvgPace.append(get_sec(row[0])/42.2)
    elif row[2]=="HalfMarathon":
        AvgPace.append(get_sec(row[0])/21.1)
    elif row[2]=="10K":
        AvgPace.append(get_sec(row[0])/10)
    elif row[2]=="5K":
        AvgPace.append(get_sec(row[0])/5)
    else:
        AvgPace.append(0)


TimeDf = pd.DataFrame(AvgPace, columns=["AvgPace"])
TimeDf.AvgPace = pd.to_datetime(TimeDf["AvgPace"], unit='s').dt.time
df = pd.DataFrame(temp, columns=["FinishTime", "Year", "RaceType"])
df['AvgPace'] = TimeDf.AvgPace
Racetypes = df["RaceType"].unique().tolist()
plot = figure(y_range=Racetypes, plot_width=300, plot_height=300)
Bar = plot.hbar(y=df.RaceType, right=df.AvgPace, height=0.5, color="#3498DB")
plot.yaxis.axis_label="AvgPace"
plot.xaxis.axis_label="RaceType"

def update(attr, old, new):
    year =  select.value
    temp = df.copy()
    temp = temp[temp['Year'] == year]
    Bar.data_source.data['y']=temp.RaceType
    Bar.data_source.data['right']=temp.AvgPace

df.Year=df.Year.astype(str);
years = df.Year.unique().tolist()
select = Select(title="Select Name:", options= years)
select.on_change('value',update)
controls = column(select)
curdoc().add_root(column(plot, controls))
