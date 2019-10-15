#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import pandas as pd


# In[2]:


#data processing into dataframe
raw_data = pd.read_csv("Datasets/Hdb Carpark Information.csv")
columns = raw_data.columns.tolist()
df = pd.DataFrame(raw_data, columns = columns)


# In[3]:


#search for carpark address
def search_carparkaddress(input):
    '''returns all carpark names with 'input' inside'''
    array = []
    for carpark in range(len(df)):
        if input.upper() in df.loc[carpark, 'address']:
            array.append(df.loc[carpark, 'address'])
    return array

search_carparkaddress('dover')


# In[4]:


#short_term_parking

def getTypes_shorttermparking():
    '''get all types of short term parking in carparks'''
    types = []
    for item in df['short_term_parking'].tolist():
        if item not in types:
            types.append(item)
    return types

def findTypes_shorttermparking(type):
    '''find all carparks with same short term parking types'''
    carparks = []
    for carpark in range(len(df)):
        if df.loc[carpark, 'short_term_parking'] == type.upper():
            carparks.append(df.loc[carpark][0])
    
    if carparks == []:
        return 
        return getTypes_shorttermparking()
    else:
        return carparks
    #return len(carparks) for number of carparks with 'type'


# In[5]:


#Free Parking

def has_freeparking(carpark_no):
    '''Check if carpark has free parking. Returns True if there is, else return False'''
    #get row for carpark_no
    row = df.loc[df['car_park_no'] == carpark_no].index[0]
    
    if df.loc[row, 'free_parking'] == 'NO':
        return False
    else:
        return True

def get_freeparking(carpark_no):
    row = df.loc[df['car_park_no'] == carpark_no].index[0]
    return df.loc[row, 'free_parking']

#get_freeparking('AH1')


# In[6]:


#Night Parking

def has_nightparking(carpark_no):
    #get row for carpark_no
    row = df.loc[df['car_park_no'] == carpark_no].index[0]
    
    if df.loc[row, 'night_parking'] == 'NO':
        return False
    else:
        return True
    
#has_nightparking('AH1')


# In[13]:


#gantry height
def get_gantryheight(carpark_no):
    '''returns gantry height of carpark, 0 means surface carpark'''
    row = df.loc[df['car_park_no'] == carpark_no].index[0]
    return df.loc[row, 'gantry_height']

get_gantryheight('AH1')


# In[10]:


#Basement carpark
def has_basement(carpark_no):
    '''returns True if carpark has basement, else False'''
    row = df.loc[df['car_park_no'] == carpark_no].index[0]
    return df.loc[row, 'car_park_basement'] == 'Y'


# In[12]:


has_basement('ACB')


# In[ ]:




