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
    global result
    result = pd.concat(frames)
    result.Year=result.Year.astype(str);
    Races = ['Marathon', 'HalfMarathon', '10K', '5K']
    plot = figure(x_range=Races, plot_width=300, plot_height=300)
    plot.background_fill_color = "#fafafa"
    plot.toolbar.logo = None
    plot.toolbar_location = None
    r1 = plot.vbar(x=result['RaceType'], width=0.5, bottom=0, top=result['Amount'], color="#3498DB")
def update_VBarPlot(attr, old, new):
    year =  select.value
    temp = result.copy()
    temp = temp[temp['Year'] == year]
    print(temp)
    r1.data_source.data['x']=temp['RaceType']
    r1.data_source.data['top']=temp['Amount']


result.Year=result.Year.astype(str);
years = result["Year"].unique().tolist()
select = Select(title="Select Name:", options= years)
select.on_change('value',update_VBarPlot)
controls = column(select)
curdoc().add_root(column(plot, controls))
curdoc().title = "Sliders"
