import pandas as pd


def DublinDataFrame():
    Dublinfields = ['RunnerID', 'Name', 'Age', 'Hometown', 'Gender']
    Dublindf = pd.read_csv('Dublin.csv', usecols=Dublinfields)
    Dublindf = Dublindf[Dublindf.Name!='None']
    data = []
    for index, row in Dublindf.iterrows():
        data.append((row['RunnerID'],  row['Name'], row['Hometown'], row['Gender'], 'Null'))
    NewDublindf = pd.DataFrame(data, columns=['RunnerID', 'Name', 'From', 'Gender', 'DateOfBirth'])
    return NewDublindf


Dublin = DublinDataFrame()
Dublin.to_csv('Runner.csv', index=False)
