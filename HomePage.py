from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import json
import os
import subprocess
import time
from werkzeug import secure_filename
from bokeh.models.widgets import Select
from bokeh.layouts import widgetbox ,row, column
from bokeh.plotting import figure, output_file, show
from bokeh.embed import components
from bokeh.plotting import curdoc
import collections
import datetime
from bokeh.client import push_session
from bokeh.embed import autoload_server
from bokeh.client import pull_session
from bokeh.models.formatters import DatetimeTickFormatter
import pandas as pd
app = Flask(__name__)

@app.route("/")
def main():
    return render_template('Index.html')



@app.route("/NewIndex", methods=['GET', 'POST'])
def search():
    if request.method == "POST":
        with sqlite3.connect('DisneyDB2.db') as conn:
            cursor = conn.cursor()
            Result = cursor.execute('Select * from Runner where Name=?;', [str(request.form['search'])])
            rows = Result.fetchone()
            ID = rows[0]
            Name = rows[1]
            return render_template('search.html', RunnerName=Name, RunnerID=ID)
    return render_template('FinalIndex.html')

@app.route('/Runner/RunnerProfile/<Runner>')
def RunnerProfile(Runner):
    Name = ""
    print(Runner)
    RunnerID = Runner
    with sqlite3.connect('DisneyDB2.db') as conn:
        cursor = conn.cursor()
        Result = cursor.execute('Select * from Runner where RunnerID=?;', [RunnerID])
        rows = Result.fetchone()
        Name=rows[1]
        From=rows[2]
        Gender=rows[3]
        Date=rows[4]
    return render_template('RunnerProfile.html', RunnerName=Name, RunnerID=RunnerID, RunnerGender=Gender, RunnerFrom=From, RunnerDOB=Date)

@app.route('/Race/RaceResults/<Location>')
def Races(Location):
    print(Location)
    with sqlite3.connect('DublinMarathons0.db') as conn:
        cursor = conn.cursor()
        Races = cursor.execute("select RaceDetails.RaceID, RaceDetails.RaceName from RaceDetails where RaceDetails.Location=?;", [Location])
        Races = Races.fetchall()
    return render_template('Races.html', Races=Races, Location=Location)



@app.route('/Race/RaceResults/<Location>/<RaceID>/Results/<Max>')
def RaceTables(Location, RaceID, Max):
    Min = 10
    print(RaceID)
    if((int(Max))/10>=Min):
        Min=int(Max)/10+10
    with sqlite3.connect('DublinMarathons0.db') as conn:
        cursor = conn.cursor()
        Runners = cursor.execute('select Race.RunnerID from Race where Race.RaceID=?;', [RaceID])
        Runners = Runners.fetchall()
        print(Runners)
        RaceInfo = cursor.execute('select Runner.Name, Race.RunnerID, Race.RaceID, FinishTime.Clock_Time ,Rank.OverallPlace, Rank.CategoryPlace, Rank.GenderPlace from Race Inner Join FinishTime on FinishTime.RunnerID=Race.RunnerID and FinishTime.RaceID=Race.RaceID Inner Join Runner on Runner.RunnerID = Race.RunnerID Inner Join Rank on Rank.RunnerID=FinishTime.RunnerID and Rank.RaceID=FinishTime.RaceID Where Race.RaceID=? Limit ?, ?', [RaceID, Max, 10])
        RaceInfos = RaceInfo.fetchall()
        print(RaceInfos)
        Prev = str(int(Max)-10)
        Next = str(int(Max)+10)
        HyperLinks = len(Runners)/10
    return render_template('RaceResults.html', RaceInfos=RaceInfos, RaceID=RaceID, Prev=Prev, Next=Next, HyperLinks=HyperLinks, Current=int(Max)/10, Min=int(Min))

@app.route('/Race/RaceDetails/<Location>')
def RaceDetails(Location):
    with sqlite3.connect('DublinMarathons0.db') as conn:
        cursor = conn.cursor()
        RaceDetails = cursor.execute("select RaceDetails.RaceID, RaceDetails.RaceName, RaceDetails.Year, RaceDetails.Location, RaceDetails.RaceType from RaceDetails where RaceDetails.Location=?;", [Location])
        Results = RaceDetails.fetchall()
    return render_template('RaceDetails.html', RaceDets=Results, Location=Location)


@app.route('/Runner/RunnerTables/<Runner>')
def RunnerTable(Runner):
    test="";
    with sqlite3.connect('DisneyDB2.db') as conn:
        cursor = conn.cursor()
        RaceInfo = cursor.execute('select Race.RaceID, FinishTime.Clock_Time ,Rank.OverallPlace, Rank.CategoryPlace, Rank.GenderPlace from Race Inner Join FinishTime on FinishTime.RunnerID=Race.RunnerID and FinishTime.RaceID=Race.RaceID Inner Join Rank on Rank.RunnerID=FinishTime.RunnerID and Rank.RaceID=FinishTime.RaceID Where Race.RunnerID=?;', [Runner])
        RaceIDS = RaceInfo.fetchall()
        Result = cursor.execute('Select * from Splits where RunnerID=?;', [Runner])
        Splits = Result.fetchall()
        Names = cursor.execute('select Name from Runner where RunnerID=?;', [Runner])
        Name = Names.fetchone()
    return render_template('RunnerTables.html', RunnerID=Runner, RunnerName=Name, RaceIDS=RaceIDS, Splits=Splits)


@app.route('/Runner/Dashboard/<Runner>')
def Analytics(Runner):
    Name = ""
    From=""
    Gender=""
    Date=""
    with sqlite3.connect('DisneyDB2.db') as conn:
        cursor = conn.cursor()
        Result = cursor.execute("Select * from Runner where RunnerID=?", [Runner])
        rows = Result.fetchall()
        for row in rows:
            Name=row[1]
            From=row[2]
            Gender=row[3]
            Date=row[4]
        print(Name)
        print(From)
    Script=autoload_server(model=None,app_path="/RunnerAnalytics",url="http://localhost:5007")
    return render_template('RaceAnalytics.html', Script=Script, RunnerID=Runner, RunnerName=Name, From=From, Gender=Gender, Date=Date)

@app.route('/Race/Dashboard/<Location>')
def MarathonAnalytics(Location):
    Script=autoload_server(model=None, app_path="/RaceAnalytics", url="http://localhost:5006")
    return render_template('MarathonAnalytics.html', Script=Script, Location=Location)

@app.route('/Runner/Upload/<Runner>')
def upload_file(Runner):
   return render_template('upload.html', RunnerID=Runner)

UPLOAD_FOLDER = '/Users/noellemacdonagh/Downloads/WebsiteDesignJan/WebsiteDesignJan/Uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/Runner/upload/<Runner>/uploaded', methods = ['GET', 'POST'])
def temp(Runner):
   if request.method == 'POST':
      file = request.files['file']
      filename = secure_filename(file.filename)
      data = json.loads(file.read())
      print(data)
      Splits, SplitStarts, SplitEnds = GetSplits(data)
      print(data)
      print(Splits)
      print(SplitStarts)
      print(SplitEnds)
      with sqlite3.connect('DisneyDB2.db') as conn:
          cursor = conn.cursor()
          count = Splits.SplitDuration.size
          for x in range(0, count):
              IntervalQuery = "Insert into Splits(RaceID, RunnerID, SplitStart, SplitEnd, SplitUnit, SplitStartTime, SplitEndTime, SplitDuration) Values(?, ?, ?, ?, ?, ?, ?, ?)"
              cursor.execute(IntervalQuery, [data['RaceID'], data['RunnerID'], SplitStarts[x], SplitEnds[x], data['RaceUnits'], str(Splits.SplitStartTimes.iloc[x]), str(Splits.SplitEndTimes.iloc[x]), str(Splits.SplitDuration.iloc[x])])
          RunnerQuery = "Insert into Runner(RunnerID) Values (?);"
          cursor.execute(RunnerQuery, [data['RunnerID']])
          RaceQuery = "Insert into Race(RaceID, RunnerID) Values (?, ?);"
          cursor.execute(RaceQuery, [data['RaceID'], data['RunnerID']])
          FinishQuery = "Insert into FinishTime(RaceID, RunnerID, Net_Time) Values(?, ?, ?);"
          cursor.execute(FinishQuery, [data['RaceID'], data['RunnerID'], data['FinishTime']])
          RaceDetailsQuery = "Insert into RaceDetails(RaceID) Values (?);"
          cursor.execute(RaceDetailsQuery, [data['RaceID']])
          RankQuery = "Insert into Rank(RunnerID, RaceID) Values(?, ?)"
          cursor.execute(RankQuery, [data['RunnerID'], data['RaceID']])
      return render_template('Uploaded.html', RunnerID=Runner)



def GetSplits(data):
    SplitStarts = [0]
    SplitEnds = []
    Splits = pd.DataFrame(columns=['SplitStartTimes', 'SplitEndTimes'])
    SplitDurations = pd.DataFrame(columns=['SplitDur'])
    for key, value in data['Intervals'].items():
        SplitEnds.append(key)
        SplitDurations = SplitDurations.append({'SplitDur': value}, ignore_index=True)
    for end in SplitEnds[:-1]:
      SplitStarts.append(end)
    count = SplitDurations.SplitDur.size
    InitialStart = datetime.time(0, 0, 0)
    for x in range(0, count):
        if x==0:
            Splits = Splits.append({'SplitStartTimes': InitialStart, 'SplitEndTimes': SplitDurations.SplitDur.iloc[x]}, ignore_index=True)
        else:
            Splits = Splits.append({'SplitStartTimes': Splits.SplitEndTimes.iloc[x-1], 'SplitEndTimes': add_time(Splits.SplitEndTimes.iloc[x-1], SplitDurations.SplitDur.iloc[x])}, ignore_index=True)
    Splits['SplitDuration'] = SplitDurations['SplitDur']
    return (Splits, SplitStarts, SplitEnds)


def get_sec(time_str):
    h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + int(s)

def add_time(t1, t2):
    seconds = get_sec(t1)+get_sec(t2)
    return(time.strftime('%H:%M:%S', time.gmtime(seconds)))

if __name__ == "__main__":
    app.run(debug=True)
