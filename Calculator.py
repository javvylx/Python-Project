import datetime
import pandas as pd
import requests
from pprint import pprint

# Read CSV
# df = pd.read_csv("carparkFees.csv")

url = "https://www.ura.gov.sg/uraDataService/insertNewToken.action"
header = {"AccessKey": "bbdbccd7-842d-4442-9485-e001137d4935"}
response = requests.get(url, headers=header)
token = response.json()['Result']

header1 = {"AccessKey": "bbdbccd7-842d-4442-9485-e001137d4935",
           "Token": token}

url1 = "https://www.ura.gov.sg/uraDataService/invokeUraDS?service=Car_Park_Details"
carparkRates = requests.get(url1, params={"service": "Car_Park_Details"}, headers=header1).json()['Result']
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


df = pd.DataFrame(carparkFees)

df['Start Time'] = (df['Start Time'].str.replace('.', ':', regex=True))
df['End Time'] = (df['End Time'].str.replace('.', ':', regex=True))

x = 0
for n in df['Start Time']:
    while x < len(df['Start Time']):
        df['Start Time'].iloc[x] = pd.to_datetime(df['Start Time'].iloc[x]).strftime('%H:%M')
        df['Start Time'].iloc[x] = pd.to_datetime(df['Start Time'].iloc[x], format='%H%M', errors='ignore')
        x += 1

y = 0
for n in df['End Time']:
    while y < len(df['End Time']):
        df['End Time'].iloc[y] = pd.to_datetime(df['End Time'].iloc[y]).strftime('%H:%M')
        df['End Time'].iloc[y] = pd.to_datetime(df['End Time'].iloc[y], format='%H%M', errors='ignore')
        y += 1

# Input Text = Carpark Name, can use callback function , User has to input the desired lot type
# output dataframe based on carpark name
inputText = "ALLENBY ROAD "
inputLotType = "Car"
output = (df.loc[df['Carpark Name'] == inputText])
userOutput = output[
    ['Lot Type', 'WeekDay Rates', 'WeekDay Minimum', 'Saturday Rates', 'Saturday Minimum', 'Sunday & PH Rates',
     'Sunday & PH Minimum', 'Start Time', 'End Time']]

# User has to input the year, month, day, start time
startYear = '2019'
startMonth = '10'
startDay = '14'
startTime = '09:00'  # time must be based on this format HH:MM

# This block of lines are to format the datatype of the time into datetime for calculation
timeStart = startYear + ' ' + startMonth + ' ' + startDay + ' ' + startTime
timeStart = pd.to_datetime(timeStart).strftime('%Y/%m/%d %H:%M')
timeStart = datetime.datetime.strptime(timeStart, '%Y/%m/%d %H:%M')
startingTime = pd.to_datetime(timeStart, format='%H:%M').time()  # Get Only the time, removing dates
dayofweek = timeStart.weekday()  # Get the day of week (e.g. Monday-Friday/Saturday/Sunday)

# This block of lines are to format the datatype of the time into datetime for calculation
endYear = '2019'
endMonth = '10'
endDay = '15'
endTime = '09:00'
timeEnd = endYear + ' ' + endMonth + ' ' + endDay + ' ' + endTime
timeEnd = pd.to_datetime(timeEnd).strftime('%Y/%m/%d %H:%M')
timeEnd = datetime.datetime.strptime(timeEnd, '%Y/%m/%d %H:%M')
endTime = pd.to_datetime(endTime).strftime('%H:%M')


def countCarPrice(timeStart, timeEnd, startingTime):
    # Input lot type is Car
    if inputLotType == "Car":
        count = 0  # Variable for cost
        a = 0  # Variable for looping
        # Loop not more than the total length of the dataframe
        while a < len(userOutput):
            if userOutput['Lot Type'].iloc[a] == 'Car':
                # Weekday parking rates
                if 0 <= timeStart.weekday() <= 4:
                    # For parking times between 00:00 and 22:30
                    if pd.to_datetime('00:00', format='%H:%M').time() <= startingTime < pd.to_datetime('22:30',
                                                                                                       format='%H:%M').time():
                        # Break if timeStart is more than or equal to timeEnd
                        if timeStart >= timeEnd:
                            count += 0
                            return count
                        # Get the row for when starting time is between two times
                        elif pd.to_datetime(userOutput['Start Time'].iloc[a],
                                            format='%H:%M').time() <= startingTime < pd.to_datetime(
                                userOutput['End Time'].iloc[a], format='%H:%M').time():
                            minMins = int(userOutput['WeekDay Minimum'].iloc[a].replace('mins', ""))
                            timeStart += datetime.timedelta(minutes=minMins)
                            startingTime = pd.to_datetime(timeStart, format='%H:%M').time()
                            count += float(userOutput['WeekDay Rates'].iloc[a].replace('$', ""))
                            return count + countCarPrice(timeStart, timeEnd, startingTime)
                        # Return 30 mins parking for overnight parking, aka pass 00:00
                        elif pd.to_datetime(userOutput['Start Time'].iloc[a], format='%H:%M').time() > pd.to_datetime(
                                userOutput['End Time'].iloc[a], format='%H:%M').time() >= startingTime:
                            # If there is 30 mins parking for overnight parking, add the parking fees
                            if userOutput['WeekDay Minimum'].iloc[a] == '30 mins':
                                timeStart += datetime.timedelta(minutes=30)
                                startingTime = pd.to_datetime(timeStart, format='%H:%M').time()
                                count += float(userOutput['WeekDay Rates'].iloc[a].replace('$', ""))
                                return count + countCarPrice(timeStart, timeEnd, startingTime)
                            # If there are no 30 mins based overnight parking, free parking until next time slot
                            else:
                                count += 0
                                timeStart += datetime.timedelta(minutes=30)
                                startingTime = pd.to_datetime(timeStart, format='%H:%M').time()
                                return count + countCarPrice(timeStart, timeEnd, startingTime)
                        # Free parking if no rows found between timings
                        else:
                            count += 0
                            timeStart += datetime.timedelta(minutes=30)
                            startingTime = pd.to_datetime(timeStart, format='%H:%M').time()
                            return count + countCarPrice(timeStart, timeEnd, startingTime)
                    # Get rows of parking fees for starting time pass or equals to 22:30
                    elif startingTime >= pd.to_datetime('22:30', format='%H:%M').time():
                        # Break if timeStart is more than or equal to timeEnd
                        if timeStart >= timeEnd:
                            count += 0
                            return count
                        # Check if duration of overnight parking is less than 510 minutes
                        elif timeEnd - timeStart < datetime.timedelta(minutes=510):
                            # Check for 30 minutes parking for overnight parking is less than 510 minutes
                            if userOutput['WeekDay Minimum'].iloc[a] == '30 mins':
                                timeStart += datetime.timedelta(minutes=30)
                                startingTime = pd.to_datetime(timeStart, format='%H:%M').time()
                                count += float(userOutput['WeekDay Rates'].iloc[a].replace('$', ""))
                                return count + countCarPrice(timeStart, timeEnd, startingTime)
                            # Free parking if there are no 30 minutes parking charge
                            else:
                                count += 0
                                timeStart += datetime.timedelta(minutes=30)
                                startingTime = pd.to_datetime(timeStart, format='%H:%M').time()
                                return count + countCarPrice(timeStart, timeEnd, startingTime)
                        # Check if duration of parking is full 510mins overnight parking and parking time not exceed
                        # 07:00, which is the cut off for midnight parking
                        elif timeEnd - timeStart >= datetime.timedelta(minutes=510) and pd.to_datetime(
                                timeStart + datetime.timedelta(minutes=510), format='%H:%M').time() <= pd.to_datetime(
                                '07:00', format='%H:%M').time():
                            if userOutput['WeekDay Minimum'].iloc[a] == '510 mins':
                                timeStart += datetime.timedelta(minutes=510)
                                startingTime = pd.to_datetime(timeStart, format='%H:%M').time()
                                count += float(userOutput['WeekDay Rates'].iloc[a].replace('$', ""))
                                return count + countCarPrice(timeStart, timeEnd, startingTime)
                            # Free parking for rows not found until next timing slot
                            else:
                                count += 0
                                timeStart += datetime.timedelta(minutes=30)
                                startingTime = pd.to_datetime(timeStart, format='%H:%M').time()
                                return count + countCarPrice(timeStart, timeEnd, startingTime)
                        # Free parking for rows not found until next timing slot
                        else:
                            count += 0
                            timeStart += datetime.timedelta(minutes=30)
                            startingTime = pd.to_datetime(timeStart, format='%H:%M').time()
                            return count + countCarPrice(timeStart, timeEnd, startingTime)
                    # Free parking for rows not found until next timing slot
                    else:
                        count += 0
                        timeStart += datetime.timedelta(minutes=30)
                        startingTime = pd.to_datetime(timeStart, format='%H:%M').time()
                        return count + countCarPrice(timeStart, timeEnd, startingTime)
                # Saturday parking rates
                elif timeStart.weekday() == 5:
                    # For parking times between 00:00 and 22:30
                    if pd.to_datetime('00:00', format='%H:%M').time() <= startingTime < pd.to_datetime('22:30',
                                                                                                       format='%H:%M').time():
                        # Break if timeStart is more than or equal to timeEnd
                        if timeStart >= timeEnd:
                            count += 0
                            return count
                        # Get the row for when starting time is between two times
                        elif pd.to_datetime(userOutput['Start Time'].iloc[a],
                                            format='%H:%M').time() <= startingTime < pd.to_datetime(
                                userOutput['End Time'].iloc[a], format='%H:%M').time():
                            minMins = int(userOutput['Saturday Minimum'].iloc[a].replace('mins', ""))
                            timeStart += datetime.timedelta(minutes=minMins)
                            startingTime = pd.to_datetime(timeStart, format='%H:%M').time()
                            count += float(userOutput['Saturday Rates'].iloc[a].replace('$', ""))
                            return count + countCarPrice(timeStart, timeEnd, startingTime)
                        # Return 30 mins parking for overnight parking, aka pass 00:00
                        elif pd.to_datetime(userOutput['Start Time'].iloc[a], format='%H:%M').time() > pd.to_datetime(
                                userOutput['End Time'].iloc[a], format='%H:%M').time() >= startingTime:
                            # If there is 30 mins parking for overnight parking, add the parking fees
                            if userOutput['Saturday Minimum'].iloc[a] == '30 mins':
                                timeStart += datetime.timedelta(minutes=30)
                                startingTime = pd.to_datetime(timeStart, format='%H:%M').time()
                                count += float(userOutput['Saturday Rates'].iloc[a].replace('$', ""))
                                return count + countCarPrice(timeStart, timeEnd, startingTime)
                            # If there are no 30 mins based overnight parking, free parking until next time slot
                            else:
                                count += 0
                                timeStart += datetime.timedelta(minutes=30)
                                startingTime = pd.to_datetime(timeStart, format='%H:%M').time()
                                return count + countCarPrice(timeStart, timeEnd, startingTime)
                        # Free parking if no rows found between timings
                        else:
                            count += 0
                            timeStart += datetime.timedelta(minutes=30)
                            startingTime = pd.to_datetime(timeStart, format='%H:%M').time()
                            return count + countCarPrice(timeStart, timeEnd, startingTime)
                    # Get rows of parking fees for starting time pass or equals to 22:30
                    elif startingTime >= pd.to_datetime('22:30', format='%H:%M').time():
                        # Break if timeStart is more than or equal to timeEnd
                        if timeStart >= timeEnd:
                            count += 0
                            return count
                        # Check if duration of overnight parking is less than 510 minutes
                        elif timeEnd - timeStart < datetime.timedelta(minutes=510):
                            # Check for 30 minutes parking for overnight parking is less than 510 minutes
                            if userOutput['Saturday Minimum'].iloc[a] == '30 mins':
                                timeStart += datetime.timedelta(minutes=30)
                                startingTime = pd.to_datetime(timeStart, format='%H:%M').time()
                                count += float(userOutput['Saturday Rates'].iloc[a].replace('$', ""))
                                return count + countCarPrice(timeStart, timeEnd, startingTime)
                            # Free parking if there are no 30 minutes parking charge
                            else:
                                count += 0
                                timeStart += datetime.timedelta(minutes=30)
                                startingTime = pd.to_datetime(timeStart, format='%H:%M').time()
                                return count + countCarPrice(timeStart, timeEnd, startingTime)
                        # Check if duration of parking is full 510mins overnight parking and parking time not exceed
                        # 07:00, which is the cut off for midnight parking
                        elif timeEnd - timeStart >= datetime.timedelta(minutes=510) and pd.to_datetime(
                                timeStart + datetime.timedelta(minutes=510), format='%H:%M').time() <= pd.to_datetime(
                                '07:00', format='%H:%M').time():
                            if userOutput['Saturday Minimum'].iloc[a] == '510 mins':
                                timeStart += datetime.timedelta(minutes=510)
                                startingTime = pd.to_datetime(timeStart, format='%H:%M').time()
                                count += float(userOutput['Saturday Rates'].iloc[a].replace('$', ""))
                                return count + countCarPrice(timeStart, timeEnd, startingTime)
                            # Free parking for rows not found until next timing slot
                            else:
                                count += 0
                                timeStart += datetime.timedelta(minutes=30)
                                startingTime = pd.to_datetime(timeStart, format='%H:%M').time()
                                return count + countCarPrice(timeStart, timeEnd, startingTime)
                        # Free parking for rows not found until next timing slot
                        else:
                            count += 0
                            timeStart += datetime.timedelta(minutes=30)
                            startingTime = pd.to_datetime(timeStart, format='%H:%M').time()
                            return count + countCarPrice(timeStart, timeEnd, startingTime)
                    # Free parking for rows not found until next timing slot
                    else:
                        count += 0
                        timeStart += datetime.timedelta(minutes=30)
                        startingTime = pd.to_datetime(timeStart, format='%H:%M').time()
                        return count + countCarPrice(timeStart, timeEnd, startingTime)
                # Sunday Parking Rates
                elif timeStart.weekday() == 6:
                    # For parking times between 00:00 and 22:30
                    if pd.to_datetime('00:00', format='%H:%M').time() <= startingTime < pd.to_datetime('22:30',
                                                                                                       format='%H:%M').time():
                        # Break if timeStart is more than or equal to timeEnd
                        if timeStart >= timeEnd:
                            count += 0
                            return count
                        # Get the row for when starting time is between two times
                        elif pd.to_datetime(userOutput['Start Time'].iloc[a],
                                            format='%H:%M').time() <= startingTime < pd.to_datetime(
                                userOutput['End Time'].iloc[a], format='%H:%M').time():
                            minMins = int(userOutput['Sunday Minimum'].iloc[a].replace('mins', ""))
                            timeStart += datetime.timedelta(minutes=minMins)
                            startingTime = pd.to_datetime(timeStart, format='%H:%M').time()
                            count += float(userOutput['Sunday Rates'].iloc[a].replace('$', ""))
                            return count + countCarPrice(timeStart, timeEnd, startingTime)
                        # Return 30 mins parking for overnight parking, aka pass 00:00
                        elif pd.to_datetime(userOutput['Start Time'].iloc[a], format='%H:%M').time() > pd.to_datetime(
                                userOutput['End Time'].iloc[a], format='%H:%M').time() >= startingTime:
                            # If there is 30 mins parking for overnight parking, add the parking fees
                            if userOutput['Sunday Minimum'].iloc[a] == '30 mins':
                                timeStart += datetime.timedelta(minutes=30)
                                startingTime = pd.to_datetime(timeStart, format='%H:%M').time()
                                count += float(userOutput['Sunday Rates'].iloc[a].replace('$', ""))
                                return count + countCarPrice(timeStart, timeEnd, startingTime)
                            # If there are no 30 mins based overnight parking, free parking until next time slot
                            else:
                                count += 0
                                timeStart += datetime.timedelta(minutes=30)
                                startingTime = pd.to_datetime(timeStart, format='%H:%M').time()
                                return count + countCarPrice(timeStart, timeEnd, startingTime)
                        # Free parking if no rows found between timings
                        else:
                            count += 0
                            timeStart += datetime.timedelta(minutes=30)
                            startingTime = pd.to_datetime(timeStart, format='%H:%M').time()
                            return count + countCarPrice(timeStart, timeEnd, startingTime)
                    # Get rows of parking fees for starting time pass or equals to 22:30
                    elif startingTime >= pd.to_datetime('22:30', format='%H:%M').time():
                        # Break if timeStart is more than or equal to timeEnd
                        if timeStart >= timeEnd:
                            count += 0
                            return count
                        # Check if duration of overnight parking is less than 510 minutes
                        elif timeEnd - timeStart < datetime.timedelta(minutes=510):
                            # Check for 30 minutes parking for overnight parking is less than 510 minutes
                            if userOutput['Sunday Minimum'].iloc[a] == '30 mins':
                                timeStart += datetime.timedelta(minutes=30)
                                startingTime = pd.to_datetime(timeStart, format='%H:%M').time()
                                count += float(userOutput['Sunday Rates'].iloc[a].replace('$', ""))
                                return count + countCarPrice(timeStart, timeEnd, startingTime)
                            # Free parking if there are no 30 minutes parking charge
                            else:
                                count += 0
                                timeStart += datetime.timedelta(minutes=30)
                                startingTime = pd.to_datetime(timeStart, format='%H:%M').time()
                                return count + countCarPrice(timeStart, timeEnd, startingTime)
                        # Check if duration of parking is full 510mins overnight parking and parking time not exceed
                        # 07:00, which is the cut off for midnight parking
                        elif timeEnd - timeStart >= datetime.timedelta(minutes=510) and pd.to_datetime(
                                timeStart + datetime.timedelta(minutes=510), format='%H:%M').time() <= pd.to_datetime(
                                '07:00', format='%H:%M').time():
                            if userOutput['Sunday Minimum'].iloc[a] == '510 mins':
                                timeStart += datetime.timedelta(minutes=510)
                                startingTime = pd.to_datetime(timeStart, format='%H:%M').time()
                                count += float(userOutput['Sunday Rates'].iloc[a].replace('$', ""))
                                return count + countCarPrice(timeStart, timeEnd, startingTime)
                            # Free parking for rows not found until next timing slot
                            else:
                                count += 0
                                timeStart += datetime.timedelta(minutes=30)
                                startingTime = pd.to_datetime(timeStart, format='%H:%M').time()
                                return count + countCarPrice(timeStart, timeEnd, startingTime)
                        # Free parking for rows not found until next timing slot
                        else:
                            count += 0
                            timeStart += datetime.timedelta(minutes=30)
                            startingTime = pd.to_datetime(timeStart, format='%H:%M').time()
                            return count + countCarPrice(timeStart, timeEnd, startingTime)
                    # Free parking for rows not found until next timing slot
                    else:
                        count += 0
                        timeStart += datetime.timedelta(minutes=30)
                        startingTime = pd.to_datetime(timeStart, format='%H:%M').time()
                        return count + countCarPrice(timeStart, timeEnd, startingTime)
            a += 1

    # Input lot type is Motorcycle
    elif inputLotType == "Motorcycle":
        count = 0  # Variable for cost
        a = 0  # Variable for looping
        # Loop not more than the total length of the dataframe
        while a < len(userOutput):
            if userOutput['Lot Type'].iloc[a] == 'Motorcycle':
                # Weekday parking rates
                if 0 <= timeStart.weekday() <= 4:
                    # Break if timeStart is more than or equal to timeEnd
                    if timeStart >= timeEnd:
                        count += 0
                        return count
                    # Get the row for when starting time is between two times
                    elif pd.to_datetime(userOutput['Start Time'].iloc[a],
                                        format='%H:%M').time() <= startingTime < pd.to_datetime(
                            userOutput['End Time'].iloc[a], format='%H:%M').time():
                        minMins = int(userOutput['WeekDay Minimum'].iloc[a].replace('mins', ""))
                        timeStart += datetime.timedelta(minutes=minMins)
                        startingTime = pd.to_datetime(timeStart, format='%H:%M').time()
                        count += float(userOutput['WeekDay Rates'].iloc[a].replace('$', ""))
                        return count + countCarPrice(timeStart, timeEnd, startingTime)
                    # Get the row for overnight parking
                    elif pd.to_datetime(userOutput['Start Time'].iloc[a], format='%H:%M').time() > pd.to_datetime(
                            userOutput['End Time'].iloc[a], format='%H:%M').time():
                        # If there is overnight parking fees, increment fees accordingly
                        if userOutput['WeekDay Minimum'].iloc[a] == '510 mins':
                            minMins = int(userOutput['WeekDay Minimum'].iloc[a].replace("mins", ""))
                            timeStart += datetime.timedelta(minutes=minMins)
                            startingTime = pd.to_datetime(timeStart, format='%H:%M').time()
                            count += float(userOutput['WeekDay Rates'].iloc[a].replace('$', ""))
                            return count + countCarPrice(timeStart, timeEnd, startingTime)
                        # Free parking for no rows found
                        else:
                            count += 0
                            timeStart += datetime.timedelta(minutes=30)
                            startingTime = pd.to_datetime(timeStart, format='%H:%M').time()
                            return count + countCarPrice(timeStart, timeEnd, startingTime)
                    # Free parking for no rows found
                    else:
                        count += 0
                        timeStart += datetime.timedelta(minutes=30)
                        startingTime = pd.to_datetime(timeStart, format='%H:%M').time()
                        return count + countCarPrice(timeStart, timeEnd, startingTime)
                # Saturday parking rates
                elif timeStart.weekday() == 5:
                    # Break if timeStart is more than or equal to timeEnd
                    if timeStart >= timeEnd:
                        count += 0
                        return count
                    # Get the row for when starting time is between two times
                    elif pd.to_datetime(userOutput['Start Time'].iloc[a],
                                        format='%H:%M').time() <= startingTime < pd.to_datetime(
                        userOutput['End Time'].iloc[a], format='%H:%M').time():
                        minMins = int(userOutput['Saturday Minimum'].iloc[a].replace('mins', ""))
                        timeStart += datetime.timedelta(minutes=minMins)
                        startingTime = pd.to_datetime(timeStart, format='%H:%M').time()
                        count += float(userOutput['Saturday Rates'].iloc[a].replace('$', ""))
                        return count + countCarPrice(timeStart, timeEnd, startingTime)
                    # Get the row for overnight parking
                    elif pd.to_datetime(userOutput['Start Time'].iloc[a], format='%H:%M').time() > pd.to_datetime(
                            userOutput['End Time'].iloc[a], format='%H:%M').time():
                        # If there is overnight parking fees, increment fees accordingly
                        if userOutput['Saturday Minimum'].iloc[a] == '510 mins':
                            minMins = int(userOutput['Saturday Minimum'].iloc[a].replace("mins", ""))
                            timeStart += datetime.timedelta(minutes=minMins)
                            startingTime = pd.to_datetime(timeStart, format='%H:%M').time()
                            count += float(userOutput['Saturday Rates'].iloc[a].replace('$', ""))
                            return count + countCarPrice(timeStart, timeEnd, startingTime)
                        # Free parking for no rows found
                        else:
                            count += 0
                            timeStart += datetime.timedelta(minutes=30)
                            startingTime = pd.to_datetime(timeStart, format='%H:%M').time()
                            return count + countCarPrice(timeStart, timeEnd, startingTime)
                    # Free parking for no rows found
                    else:
                        count += 0
                        timeStart += datetime.timedelta(minutes=30)
                        startingTime = pd.to_datetime(timeStart, format='%H:%M').time()
                        return count + countCarPrice(timeStart, timeEnd, startingTime)
                # Sunday parking rates
                elif timeStart.weekday() == 6:
                    # Break if timeStart is more than or equal to timeEnd
                    if timeStart >= timeEnd:
                        count += 0
                        return count
                    # Get the row for when starting time is between two times
                    elif pd.to_datetime(userOutput['Start Time'].iloc[a],
                                        format='%H:%M').time() <= startingTime < pd.to_datetime(
                        userOutput['End Time'].iloc[a], format='%H:%M').time():
                        minMins = int(userOutput['Sunday & PH Minimum'].iloc[a].replace('mins', ""))
                        timeStart += datetime.timedelta(minutes=minMins)
                        startingTime = pd.to_datetime(timeStart, format='%H:%M').time()
                        count += float(userOutput['Sunday & PH Rates'].iloc[a].replace('$', ""))
                        return count + countCarPrice(timeStart, timeEnd, startingTime)
                    # Get the row for overnight parking
                    elif pd.to_datetime(userOutput['Start Time'].iloc[a], format='%H:%M').time() > pd.to_datetime(
                            userOutput['End Time'].iloc[a], format='%H:%M').time():
                        # If there is overnight parking fees, increment fees accordingly
                        if userOutput['Sunday & PH Minimum'].iloc[a] == '510 mins':
                            minMins = int(userOutput['Sunday & PH Minimum'].iloc[a].replace("mins", ""))
                            timeStart += datetime.timedelta(minutes=minMins)
                            startingTime = pd.to_datetime(timeStart, format='%H:%M').time()
                            count += float(userOutput['Sunday & PH Rates'].iloc[a].replace('$', ""))
                            return count + countCarPrice(timeStart, timeEnd, startingTime)
                        # Free parking for no rows found
                        else:
                            count += 0
                            timeStart += datetime.timedelta(minutes=30)
                            startingTime = pd.to_datetime(timeStart, format='%H:%M').time()
                            return count + countCarPrice(timeStart, timeEnd, startingTime)
                    # Free parking for no rows found
                    else:
                        count += 0
                        timeStart += datetime.timedelta(minutes=30)
                        startingTime = pd.to_datetime(timeStart, format='%H:%M').time()
                        return count + countCarPrice(timeStart, timeEnd, startingTime)
            a += 1

    # Input lot type is Heavy Vehicle
    elif inputLotType == "Heavy Vehicle":
        count = 0  # Variable for cost
        a = 0  # Variable for looping
        # Loop not more than the total length of the dataframe
        while a < len(userOutput):
            if userOutput['Lot Type'].iloc[a] == 'Heavy Vehicle':
                # Weekday parking rates
                if 0 <= timeStart.weekday() <= 4:
                    # Break if timeStart is more than or equals to timeEnd
                    if timeStart >= timeEnd:
                        count += 0
                        return count
                    # Get the row for when starting time is between two times
                    elif pd.to_datetime(userOutput['Start Time'].iloc[a],
                                        format='%H:%M').time() <= startingTime < pd.to_datetime(
                        userOutput['End Time'].iloc[a], format='%H:%M').time():
                        minMins = int(userOutput['WeekDay Minimum'].iloc[a].replace('mins', ""))
                        timeStart += datetime.timedelta(minutes=minMins)
                        startingTime = pd.to_datetime(timeStart, format='%H:%M').time()
                        count += float(userOutput['WeekDay Rates'].iloc[a].replace('$', ""))
                        return count + countCarPrice(timeStart, timeEnd, startingTime)
                    # Get the row for overnight parking
                    elif pd.to_datetime(userOutput['Start Time'].iloc[a], format='%H:%M').time() > pd.to_datetime(
                            userOutput['End Time'].iloc[a], format='%H:%M').time():
                        if pd.to_datetime(userOutput['Start Time'].iloc[a],
                                          format='%H:%M').time() <= startingTime < pd.to_datetime('00:00',
                                                                                                  format='%H:%M').time() or pd.to_datetime(
                            '00:00', format='%H:%M').time() <= startingTime < pd.to_datetime(
                            userOutput['End Time'].iloc[a], format='%H:%M').time():
                            minMins = int(userOutput['WeekDay Minimum'].iloc[a].replace("mins", ""))
                            timeStart += datetime.timedelta(minutes=minMins)
                            startingTime = pd.to_datetime(timeStart, format='%H:%M').time()
                            count += float(userOutput['WeekDay Rates'].iloc[a].replace('$', ""))
                            return count + countCarPrice(timeStart, timeEnd, startingTime)
                        # Free parking if no rows found
                        else:
                            count += 0
                            timeStart += datetime.timedelta(minutes=30)
                            startingTime = pd.to_datetime(timeStart, format='%H:%M').time()
                            return count + countCarPrice(timeStart, timeEnd, startingTime)
                    # Free parking if no rows found
                    else:
                        count += 0
                        timeStart += datetime.timedelta(minutes=30)
                        startingTime = pd.to_datetime(timeStart, format='%H:%M').time()
                        return count + countCarPrice(timeStart, timeEnd, startingTime)
                # Saturday rates
                elif timeStart.weekday() == 5:
                    # Break if timeStart is more or equals to timeEnd
                    if timeStart >= timeEnd:
                        count += 0
                        return count
                    # Get the row for when starting time is between two times
                    elif pd.to_datetime(userOutput['Start Time'].iloc[a],
                                        format='%H:%M').time() <= startingTime < pd.to_datetime(
                        userOutput['End Time'].iloc[a], format='%H:%M').time():
                        minMins = int(userOutput['Saturday Minimum'].iloc[a].replace('mins', ""))
                        timeStart += datetime.timedelta(minutes=minMins)
                        startingTime = pd.to_datetime(timeStart, format='%H:%M').time()
                        count += float(userOutput['Saturday Rates'].iloc[a].replace('$', ""))
                        return count + countCarPrice(timeStart, timeEnd, startingTime)
                    # Get the row for overnight parking
                    elif pd.to_datetime(userOutput['Start Time'].iloc[a], format='%H:%M').time() > pd.to_datetime(
                            userOutput['End Time'].iloc[a], format='%H:%M').time():
                        if pd.to_datetime(userOutput['Start Time'].iloc[a],
                                          format='%H:%M').time() <= startingTime < pd.to_datetime('00:00',
                                                                                                  format='%H:%M').time() or pd.to_datetime(
                            '00:00', format='%H:%M').time() <= startingTime < pd.to_datetime(
                            userOutput['End Time'].iloc[a], format='%H:%M').time():
                            minMins = int(userOutput['Saturday Minimum'].iloc[a].replace("mins", ""))
                            timeStart += datetime.timedelta(minutes=minMins)
                            startingTime = pd.to_datetime(timeStart, format='%H:%M').time()
                            count += float(userOutput['Saturday Rates'].iloc[a].replace('$', ""))
                            return count + countCarPrice(timeStart, timeEnd, startingTime)
                        # Free parking if no rows found
                        else:
                            count += 0
                            timeStart += datetime.timedelta(minutes=30)
                            startingTime = pd.to_datetime(timeStart, format='%H:%M').time()
                            return count + countCarPrice(timeStart, timeEnd, startingTime)
                        # Free parking if no rows found
                    else:
                        count += 0
                        timeStart += datetime.timedelta(minutes=30)
                        startingTime = pd.to_datetime(timeStart, format='%H:%M').time()
                        return count + countCarPrice(timeStart, timeEnd, startingTime)
                # Sunday parking rates
                elif timeStart.weekday() == 6:
                    # Break if timeStart is more or equals to timeEnd
                    if timeStart >= timeEnd:
                        count += 0
                        return count
                    # Get the row for when starting time is between two times
                    elif pd.to_datetime(userOutput['Start Time'].iloc[a],
                                        format='%H:%M').time() <= startingTime < pd.to_datetime(
                        userOutput['End Time'].iloc[a], format='%H:%M').time():
                        minMins = int(userOutput['Sunday & PH Minimum'].iloc[a].replace('mins', ""))
                        timeStart += datetime.timedelta(minutes=minMins)
                        startingTime = pd.to_datetime(timeStart, format='%H:%M').time()
                        count += float(userOutput['Sunday & PH Rates'].iloc[a].replace('$', ""))
                        return count + countCarPrice(timeStart, timeEnd, startingTime)
                    # Get the row for overnight parking
                    elif pd.to_datetime(userOutput['Start Time'].iloc[a], format='%H:%M').time() > pd.to_datetime(
                            userOutput['End Time'].iloc[a], format='%H:%M').time():
                        if pd.to_datetime(userOutput['Start Time'].iloc[a],
                                          format='%H:%M').time() <= startingTime < pd.to_datetime('00:00',
                                                                                                  format='%H:%M').time() or pd.to_datetime(
                            '00:00', format='%H:%M').time() <= startingTime < pd.to_datetime(
                            userOutput['End Time'].iloc[a], format='%H:%M').time():
                            minMins = int(userOutput['Sunday & PH Minimum'].iloc[a].replace("mins", ""))
                            timeStart += datetime.timedelta(minutes=minMins)
                            startingTime = pd.to_datetime(timeStart, format='%H:%M').time()
                            count += float(userOutput['Sunday & PH Rates'].iloc[a].replace('$', ""))
                            return count + countCarPrice(timeStart, timeEnd, startingTime)
                        # Free parking if no rows found
                        else:
                            count += 0
                            timeStart += datetime.timedelta(minutes=30)
                            startingTime = pd.to_datetime(timeStart, format='%H:%M').time()
                            return count + countCarPrice(timeStart, timeEnd, startingTime)
                    # Free parking if no rows found
                    else:
                        count += 0
                        timeStart += datetime.timedelta(minutes=30)
                        startingTime = pd.to_datetime(timeStart, format='%H:%M').time()
                        return count + countCarPrice(timeStart, timeEnd, startingTime)
            a += 1


print 'The carpark you are analysing is: ' + inputText
print 'Starting Date is %s and Ending Date is %s' % (str(timeStart), str(timeEnd))

# If lot type does not exists for the given carpark name, recursive would have none value.
# Hence, we need to have a if statement to check and print accordingly
if countCarPrice(timeStart, timeEnd, startingTime) == None:
    print inputLotType + ' lot' + ' do not exists in ' + inputText
else:
    print 'The total price is %0.2f' % countCarPrice(timeStart, timeEnd, startingTime)
