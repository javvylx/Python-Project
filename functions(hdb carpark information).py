import os
import pandas as pd

import numpy as np
import matplotlib.pyplot as plt

#data processing into dataframe
raw_data = pd.read_csv("Datasets/Hdb Carpark Information.csv")
columns = raw_data.columns.tolist()
df = pd.DataFrame(raw_data, columns = columns)

#search for carpark address
def search_carparkaddress(string):
    '''returns all carpark names with 'string' inside'''
    array = []
    for carpark in range(len(df)):
        if string.upper() in df.loc[carpark, 'address']:
            array.append(df.loc[carpark, 'address'])
    return array

#search_carparkaddress('dover')

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
            carparks.append(df.loc[carpark][0])
    
    if carparks == []:
        return getTypes_shorttermparking()
    else:
        return carparks
    #return len(carparks) for number of carparks with 'type'
    
#getTypes_shorttermparking()
#find_shorttermparking('7AM-10.30PM')

#Free Parking
def has_freeparking(carpark_no):
    '''Returns True if carpark has free parking, else return False'''
    #get row for carpark_no
    row = df.loc[df['car_park_no'] == carpark_no].index[0]
    
    if df.loc[row, 'free_parking'] == 'NO':
        return False
    else:
        return True

def get_freeparking(carpark_no):
    '''get free parking hours for carpark'''
    row = df.loc[df['car_park_no'] == carpark_no].index[0]
    return df.loc[row, 'free_parking']

#get_freeparking('AH1')

#Night Parking
def has_nightparking(carpark_no):
    '''returns True if carpark has night parking, false otherwise'''
    row = df.loc[df['car_park_no'] == carpark_no].index[0]
    
    if df.loc[row, 'night_parking'] == 'NO':
        return False
    else:
        return True
    
#has_nightparking('AH1')

#gantry height
def get_gantryheight(carpark_no):
    '''returns gantry height of carpark, 0 means surface carpark'''
    row = df.loc[df['car_park_no'] == carpark_no].index[0]
    return df.loc[row, 'gantry_height']

#get_gantryheight('ACM')


#Basement carpark
def has_basement(carpark_no):
    '''returns True if carpark has basement, else False'''
    row = df.loc[df['car_park_no'] == carpark_no].index[0]
    return df.loc[row, 'car_park_basement'] == 'Y'

#has_basement('ACB')


def getTypes_carparkdecks():
    '''get all numbers of parking decks in carparks'''
    types = {}
    for item in df['car_park_decks'].tolist():
        if item not in types:
            types[int(item)] = 0
    return types

def sortby_carparkdecks(chart_type = 'bar'):
    '''show a chart. pie/bar'''
    types = getTypes_carparkdecks() 
    types_keys = sorted(types.keys())
    
    for row in range(len(df)):
        types[int(df.loc[row].car_park_decks)] += 1
    
    if chart_type == 'bar':
        objects = tuple(v for v in types_keys)
        y_pos = np.arange(len(objects))
        performance = [types[v] for v in types_keys]

        plt.bar(y_pos, performance, align='center', alpha=0.5)
        plt.xticks(y_pos, objects)
        plt.ylabel('Number of Carpark Decks')
        plt.title('Number of Carparks')

        plt.show()
    
    if chart_type == 'pie':
        labels = tuple(v for v in types_keys)
        sizes = [types[v] for v in types_keys]

        fig1, ax1 = plt.subplots()
        patches, texts = ax1.pie(sizes, labels=labels, shadow=True, startangle=90)
        
        ax1.axis('equal')
        ax1.legend(patches, labels, loc="best")
        
        plt.title("Carpark Decks")

        plt.show()

#sortby_carparkdecks('bar')
