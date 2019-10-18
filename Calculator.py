import datetime
from datetime import timedelta
from Tkinter import *
import Tkinter as tk
from PIL import Image, ImageTk
from ttk import *
import pandas as pd

# Read CSV
df = pd.read_csv("carparkFees.csv")

# inputText = 'BANDA STREET / SAGO LANE OFF STREET'

# Input Text = Carpark Name, can use callback function , User has to input the desired lot type
# output dataframe based on carpark name
inputText = "BEATTY ROAD OFF STREET"
inputLotType = "Motorcycle"
output = (df.loc[df['Carpark Name'] == inputText])
userOutput = output[
    ['Lot Type', 'WeekDay Rates', 'WeekDay Minimum', 'Saturday Rates', 'Saturday Minimum', 'Sunday & PH Rates',
     'Sunday & PH Minimum', 'Start Time', 'End Time']]


# User has to input the year, month, day, start time
startYear = '2019'
startMonth = '10'
startDay = '14'
startTime = '09:00' # time must be based on this format HH:MM

# This block of lines are to format the datatype of the time into datetime for calculation
timeStart = startYear + ' ' + startMonth + ' ' + startDay + ' ' + startTime
timeStart = pd.to_datetime(timeStart).strftime('%Y/%m/%d %H:%M')
timeStart = datetime.datetime.strptime(timeStart, '%Y/%m/%d %H:%M')
startingTime = pd.to_datetime(timeStart, format='%H:%M').time() # Get Only the time, removing dates
dayofweek = timeStart.weekday() # Get the day of week (e.g. Monday-Friday/Saturday/Sunday)

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
        count = 0 # Variable for cost
        a = 0 # Variable for looping
        # Loop not more than the total length of the dataframe
        while a < len(userOutput):
            if userOutput['Lot Type'].iloc[a] == 'Car':
                # Date is within Weekdays
                if 0 <= timeStart.weekday() <= 4:
                    # Check if its overnight parking
                    if pd.to_datetime('00:00', format='%H:%M').time() <= startingTime < pd.to_datetime('22:30', format='%H:%M').time():
                        # Break if timeStart is more than or equal to timeEnd
                        if timeStart >= endTime:
                            count += 0
                            return count
                        # Get the row for when starting time is between two times
                        elif pd.to_datetime(userOutput['Start Time'].iloc[a], format='%H:%M').time() <= startingTime < pd.to_datetime(userOutput['End Time'].iloc[a], format='%H:%M').time():
                            minMins = int(userOutput['WeekDay Minimum'].iloc[a].replace('mins', ""))
                            timeStart += datetime.timedelta(minutes=minMins)
                            startingTime = pd.to_datetime(timeStart, format='%H:%M').time()
                            count += float(userOutput['WeekDay Rates'].iloc[a].replace('$', ""))
                            return count + countCarPrice(timeStart, timeEnd, startingTime)
                        # Check if start
                        elif pd.to_datetime(userOutput['Start Time'].iloc[a], format='%H:%M').time() >  pd.to_datetime(userOutput['End Time'].iloc[a], format='%H:%M').time() >= startingTime:
                            if userOutput['WeekDay Minimum'].iloc[a] == '30 mins':
                                timeStart += datetime.timedelta(minutes=30)
                                startingTime = pd.to_datetime(timeStart, format='%H:%M').time()
                                count += float(userOutput['WeekDay Rates'].iloc[a].replace('$',""))
                                return count + countCarPrice(timeStart, timeEnd, startingTime)
                            else:
                                count += 0
                                timeStart += datetime.timedelta(minutes=30)
                                startingTime = pd.to_datetime(timeStart, format='%H:%M').time()
                                return count + countCarPrice(timeStart, timeEnd, startingTime)
                        else:
                            count += 0
                            timeStart += datetime.timedelta(minutes=30)
                            startingTime = pd.to_datetime(timeStart, format='%H:%M').time()
                            return count + countCarPrice(timeStart, timeEnd, startingTime)
                    elif startingTime >= pd.to_datetime('22:30', format='%H:%M').time():
                        if timeStart == timeEnd or timeStart > timeEnd:
                            count += 0
                            return count
                        elif timeEnd - timeStart < datetime.timedelta(minutes=510):
                            if userOutput['WeekDay Minimum'].iloc[a] != '30 mins':
                                count += 0
                            elif userOutput['WeekDay Minimum'].iloc[a] == '30 mins' and pd.to_datetime(userOutput['Start Time'].iloc[a], format='%H:%M').time() == pd.to_datetime('22:30', format='%H:%M').time():
                                timeStart += datetime.timedelta(minutes=30)
                                startingTime = pd.to_datetime(timeStart, format='%H:%M').time()
                                count += float(userOutput['WeekDay Rates'].iloc[a].replace('$', ""))
                                return count + countCarPrice(timeStart, timeEnd, startingTime)
                            else:
                                count += 0
                                timeStart += datetime.timedelta(minutes=30)
                                startingTime = pd.to_datetime(timeStart, format='%H:%M').time()
                                return count + countCarPrice(timeStart, timeEnd, startingTime)
                        elif timeEnd - timeStart >= datetime.timedelta(minutes=510) and pd.to_datetime(timeStart + datetime.timedelta(minutes=510), format='%H:%M').time() <= pd.to_datetime('07:00', format='%H:%M').time():
                            if userOutput['WeekDay Minimum'].iloc[a] == '510 mins':
                                timeStart += datetime.timedelta(minutes=510)
                                startingTime = pd.to_datetime(timeStart, format='%H:%M').time()
                                count += float(userOutput['WeekDay Rates'].iloc[a].replace('$',""))
                                return count + countCarPrice(timeStart, timeEnd, startingTime)
                            else:
                                count += 0
                                timeStart += datetime.timedelta(minutes=30)
                                startingTime = pd.to_datetime(timeStart, format='%H:%M').time()
                                return count + countCarPrice(timeStart, timeEnd, startingTime)
                        else:
                            count += 0
                            timeStart += datetime.timedelta(minutes=30)
                            startingTime = pd.to_datetime(timeStart, format='%H:%M').time()
                            return count + countCarPrice(timeStart, timeEnd, startingTime)
                    else:
                        count += 0
                        timeStart += datetime.timedelta(minutes=30)
                        startingTime = pd.to_datetime(timeStart, format='%H:%M').time()
                        print 'wtf'
                        return countCarPrice(timeStart, timeEnd, startingTime)
                elif timeStart.weekday() == 5:
                    if pd.to_datetime('00:00', format='%H:%M').time() <= startingTime < pd.to_datetime('22:30', format='%H:%M').time():
                        if timeStart == timeEnd:
                            count += 0
                            return count
                        elif pd.to_datetime(userOutput['Start Time'].iloc[a], format='%H:%M').time() <= startingTime < pd.to_datetime(userOutput['End Time'].iloc[a], format='%H:%M').time():
                            minMins = int(userOutput['Saturday Minimum'].iloc[a].replace('mins', ""))
                            timeStart += datetime.timedelta(minutes=minMins)
                            startingTime = pd.to_datetime(timeStart, format='%H:%M').time()
                            count += float(userOutput['Saturday Rates'].iloc[a].replace('$', ""))
                            print count, startingTime, '1'
                            return count + countCarPrice(timeStart, timeEnd, startingTime)
                        elif pd.to_datetime(userOutput['Start Time'].iloc[a], format='%H:%M').time() >  pd.to_datetime(userOutput['End Time'].iloc[a], format='%H:%M').time() >= startingTime:
                            if userOutput['Saturday Minimum'].iloc[a] == '30 mins':
                                timeStart += datetime.timedelta(minutes=30)
                                startingTime = pd.to_datetime(timeStart, format='%H:%M').time()
                                count += float(userOutput['Saturday Rates'].iloc[a].replace('$',""))
                                print count, startingTime, '2'
                                return count + countCarPrice(timeStart, timeEnd, startingTime)
                            else:
                                count += 0
                                timeStart += datetime.timedelta(minutes=30)
                                startingTime = pd.to_datetime(timeStart, format='%H:%M').time()
                                return count + countCarPrice(timeStart, timeEnd, startingTime)
                        else:
                            count += 0
                            timeStart += datetime.timedelta(minutes=30)
                            startingTime = pd.to_datetime(timeStart, format='%H:%M').time()
                            return count + countCarPrice(timeStart, timeEnd, startingTime)

                    elif startingTime >= pd.to_datetime('22:30', format='%H:%M').time():
                        if timeStart == timeEnd:
                            count += 0
                            return count
                        elif timeEnd - timeStart < datetime.timedelta(minutes=510):
                            if userOutput['Saturday Minimum'].iloc[a] != '30 mins':
                                count += 0
                                print count, startingTime, 'yo'
                            elif userOutput['Saturday Minimum'].iloc[a] == '30 mins' and pd.to_datetime(userOutput['Start Time'].iloc[a], format='%H:%M').time() == pd.to_datetime('22:30', format='%H:%M').time():
                                timeStart += datetime.timedelta(minutes=30)
                                startingTime = pd.to_datetime(timeStart, format='%H:%M').time()
                                count += float(userOutput['Saturday Rates'].iloc[a].replace('$', ""))
                                return count + countCarPrice(timeStart, timeEnd, startingTime)
                        elif timeEnd - timeStart >= datetime.timedelta(minutes=510) and pd.to_datetime(timeStart + datetime.timedelta(minutes=510), format='%H:%M').time() <= pd.to_datetime('07:00', format='%H:%M').time():
                            if userOutput['Saturday Minimum'].iloc[a] == '510 mins':
                                timeStart += datetime.timedelta(minutes=510)
                                startingTime = pd.to_datetime(timeStart, format='%H:%M').time()
                                count += float(userOutput['Saturday Rates'].iloc[a].replace('$',""))
                                return count + countCarPrice(timeStart, timeEnd, startingTime)
                            else:
                                count += 0
                                timeStart += datetime.timedelta(minutes=30)
                                startingTime = pd.to_datetime(timeStart, format='%H:%M').time()
                                return count + countCarPrice(timeStart, timeEnd, startingTime)
                        else:
                            count += 0
                            timeStart += datetime.timedelta(minutes=30)
                            startingTime = pd.to_datetime(timeStart, format='%H:%M').time()
                            return count + countCarPrice(timeStart, timeEnd, startingTime)
                elif timeStart.weekday() == 6:
                    if pd.to_datetime('00:00', format='%H:%M').time() <= startingTime < pd.to_datetime('22:30', format='%H:%M').time():
                        if timeStart == timeEnd:
                            count += 0
                            return count
                        elif pd.to_datetime(userOutput['Start Time'].iloc[a], format='%H:%M').time() <= startingTime < pd.to_datetime(userOutput['End Time'].iloc[a], format='%H:%M').time():
                            minMins = int(userOutput['Sunday & PH Minimum'].iloc[a].replace('mins', ""))
                            timeStart += datetime.timedelta(minutes=minMins)
                            startingTime = pd.to_datetime(timeStart, format='%H:%M').time()
                            count += float(userOutput['Sunday & PH Rates'].iloc[a].replace('$', ""))
                            return count + countCarPrice(timeStart, timeEnd, startingTime)
                        elif pd.to_datetime(userOutput['Start Time'].iloc[a], format='%H:%M').time() >  pd.to_datetime(userOutput['End Time'].iloc[a], format='%H:%M').time() >= startingTime:
                            if userOutput['Sunday & PH Minimum'].iloc[a] == '30 mins':
                                timeStart += datetime.timedelta(minutes=30)
                                startingTime = pd.to_datetime(timeStart, format='%H:%M').time()
                                count += float(userOutput['Sunday & PH Rates'].iloc[a].replace('$',""))
                                return count + countCarPrice(timeStart, timeEnd, startingTime)
                            else:
                                count += 0
                                timeStart += datetime.timedelta(minutes=30)
                                startingTime = pd.to_datetime(timeStart, format='%H:%M').time()
                                return count + countCarPrice(timeStart, timeEnd, startingTime)
                        else:
                            count += 0
                            timeStart += datetime.timedelta(minutes=30)
                            startingTime = pd.to_datetime(timeStart, format='%H:%M').time()
                            return count + countCarPrice(timeStart, timeEnd, startingTime)

                    elif startingTime >= pd.to_datetime('22:30', format='%H:%M').time():
                        if timeStart == timeEnd:
                            count += 0
                            return count
                        elif timeEnd - timeStart < datetime.timedelta(minutes=510):
                            if userOutput['Sunday & PH Minimum'].iloc[a] != '30 mins':
                                count += 0
                            elif userOutput['Sunday & PH Minimum'].iloc[a] == '30 mins' and pd.to_datetime(userOutput['Start Time'].iloc[a], format='%H:%M').time() == pd.to_datetime('22:30', format='%H:%M').time():
                                timeStart += datetime.timedelta(minutes=30)
                                startingTime = pd.to_datetime(timeStart, format='%H:%M').time()
                                count += float(userOutput['Sunday & PH Rates'].iloc[a].replace('$', ""))
                                return count + countCarPrice(timeStart, timeEnd, startingTime)
                        elif timeEnd - timeStart >= datetime.timedelta(minutes=510) and pd.to_datetime(timeStart + datetime.timedelta(minutes=510), format='%H:%M').time() <= pd.to_datetime('07:00', format='%H:%M').time():
                            if userOutput['Sunday & PH Minimum'].iloc[a] == '510 mins':
                                timeStart += datetime.timedelta(minutes=510)
                                startingTime = pd.to_datetime(timeStart, format='%H:%M').time()
                                count += float(userOutput['Sunday & PH Rates'].iloc[a].replace('$',""))
                                return count + countCarPrice(timeStart, timeEnd, startingTime)
                            else:
                                count += 0
                                timeStart += datetime.timedelta(minutes=30)
                                startingTime = pd.to_datetime(timeStart, format='%H:%M').time()
                                return count + countCarPrice(timeStart, timeEnd, startingTime)
                        else:
                            count += 0
                            timeStart += datetime.timedelta(minutes=30)
                            startingTime = pd.to_datetime(timeStart, format='%H:%M').time()
                            return count + countCarPrice(timeStart, timeEnd, startingTime)
            a += 1
    elif inputLotType == "Motorcycle":
        count = 0
        a = 0
        while a < len(userOutput):
            if userOutput['Lot Type'].iloc[a] == 'Motorcycle':
                if 0 <= timeStart.weekday() <= 4:
                    if timeStart == timeEnd or timeStart > timeEnd:
                        count += 0
                        return count
                    elif pd.to_datetime(userOutput['Start Time'].iloc[a], format='%H:%M').time() <= startingTime < pd.to_datetime(userOutput['End Time'].iloc[a], format='%H:%M').time():
                        minMins = int(userOutput['WeekDay Minimum'].iloc[a].replace('mins', ""))
                        timeStart += datetime.timedelta(minutes=minMins)
                        startingTime = pd.to_datetime(timeStart, format='%H:%M').time()
                        count += float(userOutput['WeekDay Rates'].iloc[a].replace('$',""))
                        return count + countCarPrice(timeStart, timeEnd, startingTime)
                    elif pd.to_datetime(userOutput['Start Time'].iloc[a], format='%H:%M').time() > pd.to_datetime(userOutput['End Time'].iloc[a], format='%H:%M').time():
                        # if pd.to_datetime(userOutput['Start Time'].iloc[a], format='%H:%M').time() <= startingTime <  pd.to_datetime('00:00', format='%H:%M').time() or pd.to_datetime('00:00', format='%H:%M').time() <= startingTime < pd.to_datetime(userOutput['End Time'].iloc[a], format='%H:%M').time():
                        #     minMins = int(userOutput['WeekDay Minimum'].iloc[a].replace("mins", ""))
                        #     timeStart += datetime.timedelta(minutes=minMins)
                        #     startingTime = pd.to_datetime(timeStart, format='%H:%M').time()
                        #     count += float(userOutput['WeekDay Rates'].iloc[a].replace('$',""))
                        #     return count + countCarPrice(timeStart, timeEnd, startingTime)
                        if userOutput['WeekDay Minimum'].iloc[a] == '510 mins':
                            minMins = int(userOutput['WeekDay Minimum'].iloc[a].replace("mins", ""))
                            timeStart += datetime.timedelta(minutes=minMins)
                            startingTime = pd.to_datetime(timeStart, format='%H:%M').time()
                            count += float(userOutput['WeekDay Rates'].iloc[a].replace('$',""))
                            return count + countCarPrice(timeStart, timeEnd, startingTime)
                        else:
                            count += 0
                            timeStart += datetime.timedelta(minutes=30)
                            startingTime = pd.to_datetime(timeStart, format='%H:%M').time()
                            return count + countCarPrice(timeStart, timeEnd, startingTime)
                    else:
                        count += 0
                        timeStart += datetime.timedelta(minutes=30)
                        startingTime = pd.to_datetime(timeStart, format='%H:%M').time()
                        return count + countCarPrice(timeStart, timeEnd, startingTime)

                elif timeStart.weekday() == 5:
                    if timeStart == timeEnd or timeStart > timeEnd:
                        count += 0
                        return count
                    elif pd.to_datetime(userOutput['Start Time'].iloc[a], format='%H:%M').time() <= startingTime < pd.to_datetime(userOutput['End Time'].iloc[a], format='%H:%M').time():
                        minMins = int(userOutput['Saturday Minimum'].iloc[a].replace('mins', ""))
                        timeStart += datetime.timedelta(minutes=minMins)
                        startingTime = pd.to_datetime(timeStart, format='%H:%M').time()
                        count += float(userOutput['Saturday Rates'].iloc[a].replace('$',""))
                        return count + countCarPrice(timeStart, timeEnd, startingTime)
                    elif pd.to_datetime(userOutput['Start Time'].iloc[a], format='%H:%M').time() > pd.to_datetime(userOutput['End Time'].iloc[a], format='%H:%M').time():
                        if userOutput['Saturday Minimum'].iloc[a] == '510 mins':
                            minMins = int(userOutput['Saturday Minimum'].iloc[a].replace("mins", ""))
                            timeStart += datetime.timedelta(minutes=minMins)
                            startingTime = pd.to_datetime(timeStart, format='%H:%M').time()
                            count += float(userOutput['Saturday Rates'].iloc[a].replace('$', ""))
                            return count + countCarPrice(timeStart, timeEnd, startingTime)
                        else:
                            count += 0
                            timeStart += datetime.timedelta(minutes=30)
                            startingTime = pd.to_datetime(timeStart, format='%H:%M').time()
                            return count + countCarPrice(timeStart, timeEnd, startingTime)
                elif timeStart.weekday() == 6:
                    if timeStart == timeEnd or timeStart > timeEnd:
                        count += 0
                        return count
                    elif pd.to_datetime(userOutput['Start Time'].iloc[a], format='%H:%M').time() <= startingTime < pd.to_datetime(userOutput['End Time'].iloc[a], format='%H:%M').time():
                        minMins = int(userOutput['Sunday & PH Minimum'].iloc[a].replace('mins', ""))
                        timeStart += datetime.timedelta(minutes=minMins)
                        startingTime = pd.to_datetime(timeStart, format='%H:%M').time()
                        count += float(userOutput['Sunday & PH Rates'].iloc[a].replace('$',""))
                        return count + countCarPrice(timeStart, timeEnd, startingTime)
                    elif pd.to_datetime(userOutput['Start Time'].iloc[a], format='%H:%M').time() > pd.to_datetime(userOutput['End Time'].iloc[a], format='%H:%M').time():
                        if userOutput['Sunday & PH Minimum'].iloc[a] == '510 mins':
                            minMins = int(userOutput['Sunday & PH Minimum'].iloc[a].replace("mins", ""))
                            timeStart += datetime.timedelta(minutes=minMins)
                            startingTime = pd.to_datetime(timeStart, format='%H:%M').time()
                            count += float(userOutput['Sunday & PH Rates'].iloc[a].replace('$', ""))
                            return count + countCarPrice(timeStart, timeEnd, startingTime)
                        else:
                            count += 0
                            timeStart += datetime.timedelta(minutes=30)
                            startingTime = pd.to_datetime(timeStart, format='%H:%M').time()
                            return count + countCarPrice(timeStart, timeEnd, startingTime)
            a += 1


    elif inputLotType == "Heavy Vehicle":
        count = 0
        a = 0
        while a < len(userOutput):
            if userOutput['Lot Type'].iloc[a] == 'Heavy Vehicle':
                if 0 <= timeStart.weekday() <= 4:
                    print timeStart, timeEnd
                    if timeStart == timeEnd:
                        count += 0
                        return count
                    elif pd.to_datetime(userOutput['Start Time'].iloc[a], format='%H:%M').time() <= startingTime < pd.to_datetime(userOutput['End Time'].iloc[a], format='%H:%M').time():
                        minMins = int(userOutput['WeekDay Minimum'].iloc[a].replace('mins', ""))
                        timeStart += datetime.timedelta(minutes=minMins)
                        startingTime = pd.to_datetime(timeStart, format='%H:%M').time()
                        count += float(userOutput['WeekDay Rates'].iloc[a].replace('$',""))
                        print 'works', count

                        return count + countCarPrice(timeStart, timeEnd, startingTime)
                    elif pd.to_datetime(userOutput['Start Time'].iloc[a], format='%H:%M').time() > pd.to_datetime(userOutput['End Time'].iloc[a], format='%H:%M').time():
                        if pd.to_datetime(userOutput['Start Time'].iloc[a], format='%H:%M').time() <= startingTime <  pd.to_datetime('00:00', format='%H:%M').time() or pd.to_datetime('00:00', format='%H:%M').time() <= startingTime < pd.to_datetime(userOutput['End Time'].iloc[a], format='%H:%M').time():
                            minMins = int(userOutput['WeekDay Minimum'].iloc[a].replace("mins", ""))
                            timeStart += datetime.timedelta(minutes=minMins)
                            startingTime = pd.to_datetime(timeStart, format='%H:%M').time()
                            count += float(userOutput['WeekDay Rates'].iloc[a].replace('$',""))
                            return count + countCarPrice(timeStart, timeEnd, startingTime)
                        else:
                            count += 0
                            timeStart += datetime.timedelta(minutes=30)
                            startingTime = pd.to_datetime(timeStart, format='%H:%M').time()
                            return count + countCarPrice(timeStart, timeEnd, startingTime)

                elif timeStart.weekday() == 5:
                    if timeStart == timeEnd or timeStart > timeEnd:
                        count += 0
                        return count
                    elif pd.to_datetime(userOutput['Start Time'].iloc[a], format='%H:%M').time() <= startingTime < pd.to_datetime(userOutput['End Time'].iloc[a], format='%H:%M').time():
                        minMins = int(userOutput['Saturday Minimum'].iloc[a].replace('mins', ""))
                        timeStart += datetime.timedelta(minutes=minMins)
                        startingTime = pd.to_datetime(timeStart, format='%H:%M').time()
                        count += float(userOutput['Saturday Rates'].iloc[a].replace('$',""))
                        return count + countCarPrice(timeStart, timeEnd, startingTime)
                    elif pd.to_datetime(userOutput['Start Time'].iloc[a], format='%H:%M').time() > pd.to_datetime(userOutput['End Time'].iloc[a], format='%H:%M').time():
                        if pd.to_datetime(userOutput['Start Time'].iloc[a], format='%H:%M').time() <= startingTime <  pd.to_datetime('00:00', format='%H:%M').time() or pd.to_datetime('00:00', format='%H:%M').time() <= startingTime < pd.to_datetime(userOutput['End Time'].iloc[a], format='%H:%M').time():
                            minMins = int(userOutput['Saturday Minimum'].iloc[a].replace("mins", ""))
                            timeStart += datetime.timedelta(minutes=minMins)
                            startingTime = pd.to_datetime(timeStart, format='%H:%M').time()
                            count += float(userOutput['Saturday Rates'].iloc[a].replace('$',""))
                            return count + countCarPrice(timeStart, timeEnd, startingTime)
                        else:
                            count += 0
                            timeStart += datetime.timedelta(minutes=30)
                            startingTime = pd.to_datetime(timeStart, format='%H:%M').time()
                            return count + countCarPrice(timeStart, timeEnd, startingTime)
                    else:
                        count += 0
                        timeStart += datetime.timedelta(minutes=30)
                        startingTime = pd.to_datetime(timeStart, format='%H:%M').time()
                        return count + countCarPrice(timeStart, timeEnd, startingTime)

                elif timeStart.weekday() == 6:
                    if timeStart == timeEnd or timeStart > timeEnd:
                        count += 0
                        return count
                    elif pd.to_datetime(userOutput['Start Time'].iloc[a], format='%H:%M').time() <= startingTime < pd.to_datetime(userOutput['End Time'].iloc[a], format='%H:%M').time():
                        minMins = int(userOutput['Sunday & PH Minimum'].iloc[a].replace('mins', ""))
                        timeStart += datetime.timedelta(minutes=minMins)
                        startingTime = pd.to_datetime(timeStart, format='%H:%M').time()
                        count += float(userOutput['Sunday & PH Rates'].iloc[a].replace('$',""))
                        return count + countCarPrice(timeStart, timeEnd, startingTime)
                    elif pd.to_datetime(userOutput['Start Time'].iloc[a], format='%H:%M').time() > pd.to_datetime(userOutput['End Time'].iloc[a], format='%H:%M').time():
                        if pd.to_datetime(userOutput['Start Time'].iloc[a], format='%H:%M').time() <= startingTime <  pd.to_datetime('00:00', format='%H:%M').time() or pd.to_datetime('00:00', format='%H:%M').time() <= startingTime < pd.to_datetime(userOutput['End Time'].iloc[a], format='%H:%M').time():
                            minMins = int(userOutput['Sunday & PH Minimum'].iloc[a].replace("mins", ""))
                            timeStart += datetime.timedelta(minutes=minMins)
                            startingTime = pd.to_datetime(timeStart, format='%H:%M').time()
                            count += float(userOutput['Sunday & PH Rates'].iloc[a].replace('$',""))
                            return count + countCarPrice(timeStart, timeEnd, startingTime)
                        else:
                            count += 0
                            timeStart += datetime.timedelta(minutes=30)
                            startingTime = pd.to_datetime(timeStart, format='%H:%M').time()
                            return count + countCarPrice(timeStart, timeEnd, startingTime)
                    else:
                        count += 0
                        timeStart += datetime.timedelta(minutes=30)
                        startingTime = pd.to_datetime(timeStart, format='%H:%M').time()
                        return count + countCarPrice(timeStart, timeEnd, startingTime)
            a += 1


print 'The carpark you are analysing is: ' + inputText
print 'Starting Date is %s and Ending Date is %s' % (str(timeStart), str(timeEnd))


if countCarPrice(timeStart, timeEnd, startingTime) == NoneType:
    pass
else:
    print 'The total price is %0.2f' % countCarPrice(timeStart, timeEnd, startingTime)
