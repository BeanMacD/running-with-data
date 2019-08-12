import pandas as pd


RaceIDs = []

def FinishTimes():
    fields = ['RunnerID', 'RaceID', 'OverallPlace', 'GenderPlace', 'CategoryPlace']
    df = pd.read_csv('Dublin.csv', usecols=fields)
    data = []
    for index, row in df.iterrows():
        data.append((row['RaceID'], row['RunnerID'], row['OverallPlace'], row['GenderPlace'], row['CategoryPlace']))
    DublinRacedf = pd.DataFrame(data, columns=['RaceID', 'RunnerID', 'OverallPlace', 'GenderPlace', 'CategoryPlace'])
    return DublinRacedf

Dublin=FinishTimes()
Dublin.to_csv('Rank.csv', index=False)
