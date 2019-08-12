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


with sqlite3.connect('DisneyDB2.db') as conn:
    RunnerID='macdonagh1995'
    cursor = conn.cursor()
    FinishTimes = cursor.execute('Select FinishTime.RaceID, Net_Time, RaceDetails.Year, RaceDetails.RaceType from FinishTime Inner Join RaceDetails on FinishTime.RaceID = RaceDetails.RaceID where RunnerID=?;', [RunnerID])
    df = pd.DataFrame(FinishTimes.fetchall(), columns=["RaceID", "FinishTime", "Year", "RaceType"])
    print(df)




df['FinishTime'] = pd.to_datetime(df['FinishTime'],format= '%H:%M:%S' ).dt.time
print(df['FinishTime'])
p = figure(y_axis_type='datetime', plot_width=1000, plot_height=300)
plot = p.line(x=df.Year, y=df.FinishTime)
p.yaxis.axis_label="FinishTime"
p.xaxis.axis_label="Year"

def update(attr, old, new):
    Rtype = select.value
    temp = df.copy()
    temp = temp[temp['RaceType']==Rtype]
    plot.data_source.data['x']=temp['FinishTime']
    plot.data_source.data['y']=temp['Year']

types = df["RaceType"].unique().tolist()
select = Select(title="Select Name:", options= types)
select.on_change('value',update)
controls = column(select)
curdoc().add_root(column(p, controls))
