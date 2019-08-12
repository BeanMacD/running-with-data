import numpy as np
import pandas as pd
import sqlite3
import datetime as DT
from bokeh.plotting import ColumnDataSource, figure
from bokeh.charts import Scatter, output_file, show
from bokeh.models import HoverTool
def Test():
    with sqlite3.connect('DublinMarathons.db') as conn:
        cursor = conn.cursor()
        cursor.execute("""
        Select Splits.Split, Splits.Split_Start_Time, Splits.Split_Finish_Time, Splits.Split_Duration, RaceDetails.Year, Runner.Name
        from ((Splits
        INNER JOIN Runner ON Splits.RunnerID=Runner.RunnerID)
        INNER JOIN RaceDetails ON Splits.RaceID=RaceDetails.RaceID)
        where Runner.Name="Barry,Smyth";
        """)

        data = []
        for row in cursor.fetchall():
            data.append(row)
        df = pd.DataFrame(data, columns=['Split', 'Split_Start_Time', 'Split_Finish_Time', 'Split_Duration', 'Year', 'Name'])
        df.Split_Duration = df.Split_Duration.map(Convert)

        TOOLS = "hover"
        output_file('Scatter.html')
        source=ColumnDataSource(data=df)
        hover = HoverTool(tooltips=[
        ("Name", "$Name"),
        ("Split", "$Split"),
        ("StartTime", "$Split_Start_Time"),
        ("FinishTime", "$Split_Finish_Time")
        ])
        p = Scatter(df, x='Split_Duration', y='Year', tools=TOOLS)

        show(p)

def Convert(time):
    if not isinstance(time, str):
        return 0
    if time=='n/a':
        return 0
    Hours, Minutes, Sec = [int(x) for x in time.split(':')]
    Hours = Hours*60
    Sec = Sec/60
    return Hours+Minutes+Sec

Test()
