import pandas as pd


RaceIDs = []

def FinishTimes():
    fields = ['RaceID', 'RunnerID', 'Net_Time', 'Clock_Time']
    df = pd.read_csv('Dublin.csv', usecols=fields)
    data = []
    for index, row in df.iterrows():
        data.append((row['RaceID'], row['RunnerID'], row['Net_Time'], row['Clock_Time']))
    DublinRacedf = pd.DataFrame(data, columns=['RaceID', 'RunnerID', 'Net_Time', 'Clock_Time'])
    return DublinRacedf

Dublin=FinishTimes()
Dublin.to_csv('FinishTimes.csv', index=False)
