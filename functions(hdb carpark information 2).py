import os
import pandas as pd

import numpy as np
import matplotlib.pyplot as plt

#data processing into dataframe
raw_data = pd.read_csv("Datasets/Hdb Carpark Information.csv")
columns = raw_data.columns.tolist()
df = pd.DataFrame(raw_data, columns = columns)

#short_term_parking
def getTypes_shorttermparking():
    '''get all types of short term parking in carparks'''
    types = []
    for item in df['short_term_parking'].tolist():
        if item not in types:
            types.append(item)
    return types

def find_shorttermparking(types):
    '''find all carparks with same short term parking types'''
    carparks = []
    for carpark in range(len(df)):
        if df.loc[carpark, 'short_term_parking'] == types.upper():
            carparks.append(df.loc[carpark][1])
    
    if carparks == []:
        return getTypes_shorttermparking()
    else:
        return carparks
    #return len(carparks) for number of carparks with 'type'
    
#getTypes_shorttermparking() #returns this ['WHOLE DAY', '7AM-7PM', 'NO', '7AM-10.30PM']
#find_shorttermparking('7AM-10.30PM')

def sortby_carparkdecks(chart_type = 'bar'):
    '''show a chart. pie/bar'''
    types = {}
    for item in df['car_park_decks'].tolist():
        if item not in types:
            types[int(item)] = 0
    types_keys = sorted(types.keys())
    
    for row in range(len(df)):
        types[int(df.loc[row].car_park_decks)] += 1
    
    objects = tuple(v for v in types_keys)
    y_pos = np.arange(len(objects))
    performance = [types[v] for v in types_keys]

    plt.bar(y_pos, performance, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    plt.ylabel('Number of Carpark Decks')
    plt.title('Number of Carparks')

    plt.show()

#sortby_carparkdecks()



