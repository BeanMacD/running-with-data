from flask import Flask, render_template, request
import pandas as pd
import numpy as np
from bokeh.charts import Histogram
from bokeh.embed import components
from bokeh.plotting import figure, output_file, show
from bokeh.models.widgets import Button, TextInput, Slider, Dropdown, Select
from bokeh.layouts import widgetbox ,row, column
from bokeh.plotting import curdoc
from bokeh.layouts import layout
import sqlite3


with sqlite3.connect('DublinMarathons0.db') as conn:
    cursor = conn.cursor()
    FinishTimes = cursor.execute('Select Race.RaceID, Race.RunnerID, FinishTime.Net_Time, Runner.Gender, Race.AgeCategory from Race Inner join Runner on Race.RunnerID=Runner.RunnerID Inner join FinishTime on Race.RunnerID=FinishTime.RunnerID;')
    Finishdf = pd.DataFrame(FinishTimes.fetchall(), columns=["RaceID", "RunnerID", "FinishTime", "Gender", "AgeCategory"])

p1 = figure(title="Finish Times for Runners", plot_width=800, plot_height=300, background_fill_color="#E8DDCB")
Finishdf['FinishTime'] = Finishdf['FinishTime'].replace("n/a","0:00:00")
Finishdf['FinishTime'] = pd.to_datetime(Finishdf['FinishTime'],format= '%H:%M:%S' ).dt.time
histogram, edges = np.histogram([t.hour for t in Finishdf.FinishTime], bins = 12)
print(histogram)
plot = p1.quad(top=histogram, bottom=0, left=edges[:-1], right=edges[1:],
        fill_color="#036564", line_color="#033649")

def updateFinish(attr, old, new):
    Gender = GenderSelect.value
    Age = AgeSelect.value
    Race = RaceSelect.value
    Finishtemp = Finishdf.copy()
    if Gender!='All':
        Finishtemp = Finishtemp[Finishtemp['Gender']==Gender]
    if Age!='All':
        Finishtemp = Finishtemp[Finishtemp['AgeCategory']==Age]
    if Race!='All':
        Finishtemp = Finishtemp[Finishtemp['RaceID']==Race]
    histogram, edges = np.histogram([t.hour for t in Finishtemp.FinishTime], bins = 12)
    plot.data_source.data['top']=histogram

Ages = ['All', 'U19', 'S', '35', '40', '45', '50', '55', '60', '65', '70', '75', '80', '85', '90', '95', '100']
AgeSelect = Select(title="Select Name:", options= Ages)
AgeSelect.on_change('value',updateFinish)
Genders = ['All', 'M', 'F']
GenderSelect = Select(title="Select Name:", options= Genders)
GenderSelect.on_change('value',updateFinish)
Races = Finishdf.RaceID.unique().tolist()
Races = ['All'] + Races
RaceSelect = Select(title="Select Race:", options=Races)
RaceSelect.on_change('value', updateFinish)
controls = column(AgeSelect, GenderSelect, RaceSelect)
curdoc().add_root(row(p1, controls))
