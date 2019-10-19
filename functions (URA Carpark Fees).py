import os
import pandas as pd

#data processing into dataframe
raw_data = pd.read_csv("Datasets/carparkFees.csv")
columns = raw_data.columns.tolist()
df = pd.DataFrame(raw_data, columns = columns)

def allows_vehicle(carpark_name, vehicle_type):
    '''Check if URA carpark allows for vehicle_type to park. Car, Motorcycle or Heavy Vechicle'''
    ppCode = df.loc[df.loc[df['Carpark Name'].str.contains(carpark_name)].index[0], 'ppCode']
    for row in range(len(df)):
        if df.loc[row].ppCode == ppCode:
            if df.loc[row]['Lot Type'] == vehicle_type:
                return True
    return False

allows_vehicle('AMOY STREET OFF STREET', 'Car')
