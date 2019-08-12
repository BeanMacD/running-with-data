def SplitData():
    with sqlite3.connect('DublinMarathons0.db') as conn:
        cursor = conn.cursor()
        FinishTimes = cursor.execute('Select  Race.RaceID, Runner.RunnerID, Runner.Gender,  Splits.SplitEnd, Splits.Split_Duration, FinishTime.Net_Time from Splits Inner Join Race on Splits.RunnerID = Race.RunnerID Inner Join Runner on Splits.RunnerID = Runner.RunnerID Inner Join FinishTime on Splits.RunnerID=FinishTime.RunnerID where Splits.Split_Duration <> "n/a";')
        Splitdf = pd.DataFrame(FinishTimes.fetchall(), columns=["RaceID", "RunnerID", "Gender", "Split", "Duration", "FinishTime"])
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
    #Gender = SplitGenderSelect.value
    Race = SplitRaceSelect.value
    Age = SplitAgeSelect.value
    avges = []
    for split in Splits:
        df = Splitdf.copy()
        #if Gender!='All':
        #    df = df[df['Gender']==Gender]
        #elif Gender=='All':
        #    df = df
        if Race!='All':
            df = df[df['RaceID']==Race]
        elif Race=='All':
            df = df
        if Age!='All':
            df = df[df['Age']==Age]
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
