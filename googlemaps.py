import os
import pandas as pd
import webbrowser

#data processing into dataframe
raw_data = pd.read_csv("Datasets/Carpark Rates.csv")
columns = raw_data.columns.tolist()
df = pd.DataFrame(raw_data, columns = columns)

def googlemaps(address):
    '''Turn address into google maps search link'''
    link = 'https://www.google.com/maps/search/'
    link += address.replace(' ','+').replace('/', '%2F')
    
    webbrowser.open(link)

googlemaps('BLK 260 ANG MO KIO ST 21')

