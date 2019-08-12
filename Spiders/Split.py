import pandas as pd
from datetime import datetime


def DublinScan():
    fields = ['RaceID', 'RunnerID', 'Ten_Kilometer_Split', 'Half_Split', 'Thirty_Kilometer_Split', 'Net_Time']
    df = pd.read_csv('Dublin.csv', usecols=fields)
    DublinData = []
    for index, row in df.iterrows():
        Splits = ['0', '10', '21', '30', '42']
        StartTimes = ['00:00:00', row['Ten_Kilometer_Split'], row['Half_Split'], row['Thirty_Kilometer_Split']]
        SplitFinish = [row['Ten_Kilometer_Split'], row['Half_Split'], row['Thirty_Kilometer_Split'], row['Net_Time']]
        for i in range(0, 4):
            SplitStart = Splits[i]
            SplitEnd = Splits[i+1]
            StartTime = str(StartTimes[i])
            FinishTime = str(SplitFinish[i])
            SplitUnit = 'K'
            print(StartTime + ' and ' +FinishTime)
            if(FinishTime[:1]=='-'):
                FinishTime = FinishTime.replace("-", "", 1)
            if(StartTime[:1]=='-'):
                StartTime = StartTime.replace("-", "", 1)
            if(StartTime == 'n/a' or FinishTime == 'n/a' or StartTime=='nan' or FinishTime=='nan'):
                Duration = 'n/a'
            else:
                FMT = '%H:%M:%S'
                Duration = datetime.strptime(FinishTime, FMT) - datetime.strptime(StartTime, FMT)
            DublinData.append((row['RaceID'], row['RunnerID'], SplitStart, SplitEnd, SplitUnit, StartTime, FinishTime, Duration))
    Dublindf = pd.DataFrame(DublinData, columns=['RaceID', 'RunnerID', 'SplitStart', 'SplitEnd', 'SplitUnit', 'Split_Start_Time', 'Split_Finish_Time', 'Split_Duration'])
    Dublindf.to_csv('Split.csv', index=False)

DublinScan()
