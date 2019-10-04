import os
import pandas as pd

data = pd.read_csv("Datasets/Hdb Carpark Information.csv")

#data.head()
print(data.columns.tolist())
print(data[['car_park_no', 'address', 'type_of_parking_system']])

# Please do not edit on skeleton.py! Skeleton.py is our baseline of the project. Create a .py file urself to try it
# out any functions instead 