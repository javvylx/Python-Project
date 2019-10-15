#!/usr/bin/env python
# coding: utf-8

import os
import pandas as pd

#data processing into dataframe
raw_data = pd.read_csv("Datasets/Carpark Rates.csv")
columns = raw_data.columns.tolist()
df = pd.DataFrame(raw_data, columns = columns)

#search for carpark
def search_carpark(input):
    '''returns all carpark names with 'input' inside'''
    array = []
    for carpark in range(len(df)):
        if input in df.loc[carpark, 'carpark']:
            array.append(df.loc[carpark, 'carpark'])
    return array

#search_carpark('Complex')

def get_rate(carpark_name, day = 'None'):
    '''returns carpark rate in string for carpark and day. 
    Day can only be weekday, saturday, sunday, holiday. 
    Returns rates for all days if day is not specified'''
    
    row = df.loc[df['carpark'] == carpark_name].index[0]
    
    if day == 'None':
        return df.loc[row, 'weekdays_rate_1':'sunday_publicholiday_rate']
    else:
        if day == 'weekday':
            return df.loc[row, 'weekdays_rate_1':'weekdays_rate_2']
        if day == 'saturday':
            return df.loc[row, 'saturday']
        if day == 'sunday' or day == 'holiday':
            return df.loc[row, 'sunday_publicholiday_rate']

rate = get_rate('Heartland Mall', 'weekday')
rate.weekdays_rate_1, rate.weekdays_rate_2


