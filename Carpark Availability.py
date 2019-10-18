import requests
from Tkinter import *
from tkinter.ttk import Style
import Tkinter as tk
from PIL import Image, ImageTk
from ttk import *
import pandas as pd
from datetime import datetime, timedelta
from pprint import pprint

# pd.set_option('display.max_columns', 500)
url = "https://www.ura.gov.sg/uraDataService/insertNewToken.action"
header = {"AccessKey": "bbdbccd7-842d-4442-9485-e001137d4935"}
response = requests.get(url, headers=header)
token = response.json()['Result']

# Define parameters. If unsure, use Postman as guideline
params = {"service": "CarPark_Availability"}

# Define header. Header typically contains Accesskey and Token(re-generate every 24 hours)
header = {"AccessKey": "bbdbccd7-842d-4442-9485-e001137d4935",
          "Token": token}

# Indicate the desired URL to call API
url = "https://www.ura.gov.sg/uraDataService/invokeUraDS?service=Car_Park_Availability"

carparkavailability = requests.get(url, params=params, headers=header).json()['Result']

url1 = "https://www.ura.gov.sg/uraDataService/invokeUraDS?service=Car_Park_Details"
carparkRates = requests.get(url1, params={"service": "Car_Park_Details"}, headers=header).json()['Result']
carparknum = []
lotsAvailable = []
lotType = []
coordinates = []
weekDayRate = []
weekDayMin = []
satDayRate = []
satDayMin = []
sunPHRate = []
sunPHMin = []
carparkName = []
ppCode = []
vehCat = []
startTime = []
endTime = []
totalLots = []
parkingSystem = []

checkkey = 'geometries'
for key in carparkavailability:
    if checkkey not in key:
        coordinates.append("None")
        carparknum.append(key["carparkNo"])
        lotsAvailable.append(key["lotsAvailable"])
        lotType.append(key["lotType"])

    elif checkkey in key:
        carparknum.append(key["carparkNo"])
        lotsAvailable.append(key["lotsAvailable"])
        lotType.append(key["lotType"])
        coordinates.append(key["geometries"][0]["coordinates"])

for keys in carparkRates:
    carparkName.append(keys["ppName"])
    weekDayRate.append(keys["weekdayRate"])
    satDayRate.append(keys["satdayRate"])
    sunPHRate.append(keys["sunPHRate"])
    startTime.append(keys["startTime"])
    endTime.append(keys["endTime"])
    ppCode.append(keys["ppCode"])
    vehCat.append(keys["vehCat"])
    weekDayMin.append(keys["weekdayMin"])
    satDayMin.append(keys["satdayMin"])
    sunPHMin.append(keys["sunPHMin"])
    totalLots.append(keys["parkCapacity"])
    parkingSystem.append(keys["parkingSystem"])

carparkInfo = {"Carpark Number": carparknum,
               "Lot Type": lotType,
               "Lots Available": lotsAvailable,
               "Coordinates": coordinates
               }
carparkFees = {"ppCode": ppCode,
               "Carpark Name": carparkName,
               "WeekDay Rates": weekDayRate,
               "Saturday Rates": satDayRate,
               "Sunday & PH Rates": sunPHRate,
               "Start Time": startTime,
               "End Time": endTime,
               "Lot Type": vehCat,
               "WeekDay Minimum": weekDayMin,
               "Saturday Minimum": satDayMin,
               "Sunday & PH Minimum": sunPHMin,
               "Total Lots": totalLots,
               "Parking System": parkingSystem
               }

df = pd.DataFrame(carparkInfo)
df1 = pd.DataFrame(carparkFees)
df1 = df1[
    ['ppCode', 'Carpark Name', 'Total Lots', 'Lot Type', 'Parking System', 'WeekDay Rates', 'WeekDay Minimum', 'Saturday Rates', 'Saturday Minimum',
     'Sunday & PH Rates', 'Sunday & PH Minimum', 'Start Time', 'End Time']]

dfnamecode = df1[['ppCode', 'Carpark Name']]
dfnamecode = dfnamecode.rename(columns = {'ppCode':'Carpark Number'})
dfnamecode = dfnamecode.drop_duplicates(subset=['Carpark Number', 'Carpark Name'], keep="first")

df.loc[(df['Lot Type'] == 'C'), 'Lot Type'] = 'Car'
df.loc[(df['Lot Type'] == 'H'), 'Lot Type'] = 'Heavy Vehicles'
df.loc[(df['Lot Type'] == 'M'), 'Lot Type'] = 'Motorcycle'

df1.loc[(df1['Parking System'] == 'C'), 'Parking System'] = 'Coupon'
df1.loc[(df1['Parking System'] == 'B'), 'Parking System'] = 'Electronic'


df1['Start Time'] = (df1['Start Time'].str.replace('.', ':', regex=True))
df1['End Time'] = (df1['End Time'].str.replace('.', ':', regex=True))
x = 0
for n in df1['Start Time']:
    while x < len(df1['Start Time']):
        df1['Start Time'].iloc[x] = pd.to_datetime(df1['Start Time'].iloc[x]).strftime('%H:%M')
        df1['Start Time'].iloc[x] = pd.to_datetime(df1['Start Time'].iloc[x], format='%H%M', errors='ignore')
        x += 1

y = 0
for n in df1['End Time']:
    while y < len(df1['End Time']):
        df1['End Time'].iloc[y] = pd.to_datetime(df1['End Time'].iloc[y]).strftime('%H:%M')
        df1['End Time'].iloc[y] = pd.to_datetime(df1['End Time'].iloc[y], format='%H%M', errors='ignore')
        y += 1

dfnamecode.to_csv("CarparkNameCode.csv")
df = pd.merge(df, dfnamecode, how='inner', on=['Carpark Number'])
df = df[['Carpark Name', 'Carpark Number', 'Lot Type', 'Lots Available', 'Coordinates']]

df.to_csv("carparkAvailabilityAPI.csv")
df1.to_csv("carparkFees.csv")


# # pprint(df.loc[df['Carpark Name'] == 'CHOA CHU KANG WAY '])
# bb = (df.loc[lambda df: df['Carpark Name'] == 'CHOA CHU KANG WAY '])
# pprint(bb["Lots Available"])

readCsv = pd.read_csv("carparkAvailabilityAPI.csv")
saved_column = readCsv["Carpark Name"]

root = Tk()
root.title("Carpark Availabiity")

# Dictionary with options
choices = set()

for n in saved_column:
    choices.update([n])
choices = sorted(choices)
# tkvar.set('Choose Your Carpark')  # set the default option

canvas = tk.Canvas(root, height=500, width=600)
canvas.pack()

background_label = tk.Label(root)
background_label.place(relwidth=1, relheight=1)

frame = tk.Frame(root, bg='#006400', bd=5)
frame.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.1, anchor='n')

lower_frame = tk.Frame(root, bg='#006400', bd=10)
lower_frame.place(relx=0.5, rely=0.25, relwidth=0.75, relheight=0.6, anchor='n')

labelframe = tk.Label(lower_frame)
labelframe.place(relwidth=1, relheight=1)


# callback to print combobox value on change
def callback(eventObject):
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        pprint(df.loc[df['Carpark Name'] == (popupMenu.get())])
        userOutput = (df.loc[df['Carpark Name'] == (popupMenu.get())])
        userOutput = userOutput[['Lot Type', 'Lots Available']]
        userOutput = userOutput.to_string(index=False)
        labelframe["text"] = userOutput


# Combobox
popupMenu = Combobox(frame, state="readonly", values=choices)
popupMenu.bind("<<ComboboxSelected>>", callback)
popupMenu.place(relwidth=0.69, relheight=1)
popupMenu.style = Style()
# popupMenu.bind("<<ComboboxSelected>>", lambda e: frame.focus())  # Remove blue highlight on selection in combobox

w = Label(frame, text="Choose your carpark", anchor='center')
w.place(relx=0.7, relheight=1, relwidth=0.3)

root.mainloop()
