import pandas as pd


def ScanMale():
    RaceIDS = []
    fields = ['Age', 'AgeCategory', 'Category', 'CategoryPlace', 'Clock_Time', 'Gender', 'Half_Split', 'Hometown', 'Name', 'Net_Time', 'OverallPlace', 'RaceID', 'RunnerID', 'Ten_Kilometer_Split', 'Thirty_Kilometer_Split']
    Maledf = pd.read_csv('Dublin.csv', usecols=fields)
    Maledf = Maledf[Maledf.Gender != 'F']
    for row in Maledf.iterrows():
        if row['RaceID'] not in RaceIDS:
            
    Maledf.sort_values(by=['Clock_Time'])
    Maledf['GenderPlace'] = Maledf.count()+1
    return Maledf



def ScanFemale():
    fields = ['Age', 'AgeCategory', 'Category', 'CategoryPlace', 'Clock_Time', 'Gender', 'Half_Split', 'Hometown', 'Name', 'Net_Time', 'OverallPlace', 'RaceID', 'RunnerID', 'Ten_Kilometer_Split', 'Thirty_Kilometer_Split']
    Femaledf = pd.read_csv('Dublin.csv', usecols=fields)
    Femaledf = Femaledf[Femaledf.Gender != 'F']
    Femaledf.sort_values(by=['Clock_Time'])
    Femaledf['GenderPlace'] = range(len(Femaledf))
    return Femaledf

Male = ScanMale()
Female = ScanFemale()
frames = [Male, Female]
Result = pd.concat(frames)
Result.to_csv('Data.csv', index=False)
