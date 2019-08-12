import pandas as pd


RaceIDs = []

def DublinRace():
    fields = ['RaceID']
    global RaceIDs
    df = pd.read_csv('Dublin.csv', usecols=fields)
    data = []
    for index, row in df.iterrows():
        if row['RaceID'] not in RaceIDs:
            RaceIDs.append(row['RaceID'])
            temp = row['RaceID']
            data.append((row['RaceID'], 'SSE Dublin Marathon', 'Dublin, Ireland', temp[-4:], 'Marathon'))
    DublinRacedf = pd.DataFrame(data, columns=['RaceID', 'Race_Name', 'Location', 'Year', 'RaceType'])
    return DublinRacedf

Dublin = DublinRace()
Dublin.to_csv('Race.csv', index=False)
