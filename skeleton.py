import os
import pandas as pd

data = pd.read_csv("Datasets/Hdb Carpark Information.csv")

#data.head()
print(data.columns.tolist())
print(data[['car_park_no', 'address', 'type_of_parking_system']])

#Test