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
        Select Race.OverallPlace, Runner.Name, RaceDetails.Year
        from Race
        INNER JOIN Runner on Race.RunnerID = Runner.RunnerID
        INNER JOIN RaceDetails on Race.RaceID = RaceDetails.RaceID
        where Runner.Name="Barry,Smyth";
        """)

        data = []
        for row in cursor.fetchall():
            data.append(row)
        df = pd.DataFrame(data, columns=['Place', 'Name', 'Year'])
        output_file('Line.html')
        p = figure(plot_width=400, plot_height=400, tools=["hover"])
        p.line(df['Year'], df['Place'], line_width=2)
        p.circle(df['Year'], df['Place'], fill_color="white", size=8)
        show(p)

Test()
