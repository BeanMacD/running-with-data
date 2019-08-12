import csv
import pandas as pd

Names = []
id = 1
IDS = []

def DublinScan():
    fields = ['RunnerID', 'RaceID', 'AgeCategory', 'Category']
    Dubdf = pd.read_csv('Dublin.csv', usecols=fields)
    data = []
    for index, row in Dubdf.iterrows():
        data.append((row['RaceID'], row['RunnerID'], 'n/a', row['AgeCategory'], row['Category']))
    Dublin_df = pd.DataFrame(data, columns=['RaceID', 'RunnerID', 'Bib', 'AgeCategory', 'Category'])
    return Dublin_df


Dublin = DublinScan()
Dublin.to_csv('RaceScan.csv', index=False)
