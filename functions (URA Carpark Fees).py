import os
import pandas as pd

#data processing into dataframe
raw_data = pd.read_csv("Datasets/URA Carpark Fees.csv")
columns = raw_data.columns.tolist()
df = pd.DataFrame(raw_data, columns = columns)

#search for carpark
def search_carpark(string):
    '''returns all carpark names with 'input' inside'''
    array = []
    for carpark in range(len(df)):
        if string.upper() in df.loc[carpark, 'ppName']:
            if df.loc[carpark, 'ppName'] in array:
                continue
            array.append(df.loc[carpark, 'ppName'])
    return array

#search_carpark('Amoy')

def allows_vehicle(carpark_name, vehicle_type):
    '''Check if URA carpark allows for vehicle_type to park. Car, Motorcycle or Heavy Vechicle'''
    ppCode = df.loc[df.loc[df['ppName'].str.contains(carpark_name)].index[0], 'ppCode']
    for row in range(len(df)):
        if df.loc[row].ppCode == ppCode:
            if df.loc[row].vehCat == vehicle_type:
                return True
    return False

#allows_vehicle('AMOY STREET OFF STREET', 'Car')
