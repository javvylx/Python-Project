import datetime
from datetime import timedelta
from Tkinter import *
import Tkinter as tk
from PIL import Image, ImageTk
from ttk import *
import pandas as pd

df = pd.read_csv("carparkFees.csv")

# df['Start Time'] = (df['Start Time'].str.replace('.', ':', regex=True))
# df['End Time'] = (df['End Time'].str.replace('.', ':', regex=True))
#
fmt = '%H:%M'
# timeStart = datetime.strptime('08:00', fmt)
# timeStart = pd.to_datetime(timeStart)
# timeEnd = datetime.strptime('14:00', fmt)
#
# x = 0
# for n in df['Start Time']:
#     while x < len(df['Start Time']):
#         df['Start Time'].iloc[x] = pd.to_datetime(df['Start Time'].iloc[x]).strftime('%H:%M')
#         df['Start Time'].iloc[x] = datetime.strptime(df['Start Time'].iloc[x], '%H:%M')
#         x += 1
#
# y = 0
# for n in df['End Time']:
#     while y < len(df['End Time']):
#         df['End Time'].iloc[y] = pd.to_datetime(df['End Time'].iloc[y]).strftime('%H:%M')
#         df['End Time'].iloc[y] = datetime.strptime(df['End Time'].iloc[y], '%H:%M')
#         y += 1


# difference = timeEnd - timeStart
# difference = int(round(difference.total_seconds() / 60))
# print 'The difference is %d mins' % difference
# newtime = timeStart + timedelta(minutes=30)
# newtime = newtime.strftime(fmt)
# print newtime


# timeStart = pd.to_datetime('08:00', format='%H%M', errors='ignore')
# timeStart = pd.to_datetime('08:00').strftime('%H:%M')
# timeStart = datetime.datetime.strptime(timeStart, '%H:%M')
# print type(timeStart)
inputText = "ARMENIAN STREET OFF STREET"
inputLotType = "Car"
output = (df.loc[df['Carpark Name'] == inputText])
userOutput = output[
    ['Lot Type', 'WeekDay Rates', 'WeekDay Minimum', 'Saturday Rates', 'Saturday Minimum', 'Sunday & PH Rates',
     'Sunday & PH Minimum', 'Start Time', 'End Time']]

startYear = '2019'
startMonth = '10'
startDay = '14'
startTime = '00:00'

timeStart = startYear + ' ' + startMonth + ' ' + startDay + ' ' + startTime
timeStart = pd.to_datetime(timeStart).strftime('%Y/%m/%d %H:%M')
timeStart = datetime.datetime.strptime(timeStart, '%Y/%m/%d %H:%M')
startingTime = pd.to_datetime(timeStart, format='%H:%M').time()
dayofweek = timeStart.weekday()

endYear = '2019'
endMonth = '10'
endDay = '20'
endTime = '00:00'
timeEnd = endYear + ' ' + endMonth + ' ' + endDay + ' ' + endTime
timeEnd = pd.to_datetime(timeEnd).strftime('%Y/%m/%d %H:%M')
timeEnd = datetime.datetime.strptime(timeEnd, '%Y/%m/%d %H:%M')
endTime = pd.to_datetime(endTime).strftime('%H:%M')
# midnight = pd.to_datetime('00:00').strftime('%H:%M')
# midnight = datetime.datetime.strptime(midnight, '%H:%M')


# def countCarPrice(timeStart, timeEnd, startingTime, count):
#     a = 0
#     b = 0
#     for n in userOutput['Start Time']:
#         for y in userOutput['End Time']:
#             while a < len(userOutput):
#                 while userOutput['Lot Type'].iloc[a] == 'Car':
#                     while (pd.to_datetime(userOutput['Start Time'].iloc[b], format='%H:%M').time() <= startingTime < pd.to_datetime(userOutput['End Time'].iloc[b], format='%H:%M').time()) and timeStart != timeEnd:
#                         minMins = int(userOutput['WeekDay Minimum'].iloc[b].replace('mins', ""))
#                         timeStart += datetime.timedelta(minutes=minMins)
#                         startingTime = pd.to_datetime(timeStart, format='%H:%M').time()
#                         count += float(userOutput['WeekDay Rates'].iloc[b].replace('$', ""))
#
#                     b += 1
#                     a += 1
#                 return count + countCarPrice(timeStart, timeEnd, startingTime, count)

print type(timeEnd - timeStart)

count = 0


def countCarPrice(timeStart, timeEnd, startingTime):
    count = 0
    if inputLotType == "Car":
        a = 0
        while a < len(userOutput):
            if userOutput['Lot Type'].iloc[a] == 'Car':
                if 0 <= timeStart.weekday() <= 4:
                    if pd.to_datetime('00:00', format='%H:%M').time() <= startingTime < pd.to_datetime('22:30', format='%H:%M').time():
                        if timeStart == timeEnd:
                            count += 0
                            return count
                        elif pd.to_datetime(userOutput['Start Time'].iloc[a], format='%H:%M').time() <= startingTime < pd.to_datetime(userOutput['End Time'].iloc[a], format='%H:%M').time():
                            minMins = int(userOutput['WeekDay Minimum'].iloc[a].replace('mins', ""))
                            timeStart += datetime.timedelta(minutes=minMins)
                            startingTime = pd.to_datetime(timeStart, format='%H:%M').time()
                            count += float(userOutput['WeekDay Rates'].iloc[a].replace('$', ""))
                            print count, startingTime, '1'
                            return count + countCarPrice(timeStart, timeEnd, startingTime)
                        elif pd.to_datetime(userOutput['Start Time'].iloc[a], format='%H:%M').time() >  pd.to_datetime(userOutput['End Time'].iloc[a], format='%H:%M').time() >= startingTime:
                            if userOutput['WeekDay Minimum'].iloc[a] == '30 mins':
                                timeStart += datetime.timedelta(minutes=30)
                                startingTime = pd.to_datetime(timeStart, format='%H:%M').time()
                                count += float(userOutput['WeekDay Rates'].iloc[a].replace('$',""))
                                print count, startingTime, '2'
                                return count + countCarPrice(timeStart, timeEnd, startingTime)
                            else:
                                count += 0
                                print count, startingTime
                    elif startingTime >= pd.to_datetime('22:30', format='%H:%M').time():
                        if timeStart == timeEnd:
                            count += 0
                            return count
                        elif timeEnd - timeStart < datetime.timedelta(minutes=510):
                            if userOutput['WeekDay Minimum'].iloc[a] != '30 mins':
                                count += 0
                                print count, startingTime, 'yo'
                            elif userOutput['WeekDay Minimum'].iloc[a] == '30 mins' and pd.to_datetime(userOutput['Start Time'].iloc[a], format='%H:%M').time() == pd.to_datetime('22:30', format='%H:%M').time():
                                timeStart += datetime.timedelta(minutes=30)
                                startingTime = pd.to_datetime(timeStart, format='%H:%M').time()
                                count += float(userOutput['WeekDay Rates'].iloc[a].replace('$', ""))
                                print count, startingTime, '3'
                                return count + countCarPrice(timeStart, timeEnd, startingTime)
                        elif timeEnd - timeStart >= datetime.timedelta(minutes=510) and pd.to_datetime(timeStart + datetime.timedelta(minutes=510), format='%H:%M').time() <= pd.to_datetime('07:00', format='%H:%M').time():
                            if userOutput['WeekDay Minimum'].iloc[a] == '510 mins':
                                timeStart += datetime.timedelta(minutes=510)
                                startingTime = pd.to_datetime(timeStart, format='%H:%M').time()
                                count += float(userOutput['WeekDay Rates'].iloc[a].replace('$',""))
                                print count, startingTime, '4'
                                return count + countCarPrice(timeStart, timeEnd, startingTime)
                            else:
                                count += 0
                                print count, startingTime
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
                                print count, startingTime
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
                                print count, startingTime, '3'
                                return count + countCarPrice(timeStart, timeEnd, startingTime)
                        elif timeEnd - timeStart >= datetime.timedelta(minutes=510) and pd.to_datetime(timeStart + datetime.timedelta(minutes=510), format='%H:%M').time() <= pd.to_datetime('07:00', format='%H:%M').time():
                            if userOutput['Saturday Minimum'].iloc[a] == '510 mins':
                                timeStart += datetime.timedelta(minutes=510)
                                startingTime = pd.to_datetime(timeStart, format='%H:%M').time()
                                count += float(userOutput['Saturday Rates'].iloc[a].replace('$',""))
                                print count, startingTime, '4'
                                return count + countCarPrice(timeStart, timeEnd, startingTime)
                            else:
                                count += 0
                                print count, startingTime

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
                            print count, startingTime, '1'
                            return count + countCarPrice(timeStart, timeEnd, startingTime)
                        elif pd.to_datetime(userOutput['Start Time'].iloc[a], format='%H:%M').time() >  pd.to_datetime(userOutput['End Time'].iloc[a], format='%H:%M').time() >= startingTime:
                            if userOutput['Sunday & PH Minimum'].iloc[a] == '30 mins':
                                timeStart += datetime.timedelta(minutes=30)
                                startingTime = pd.to_datetime(timeStart, format='%H:%M').time()
                                count += float(userOutput['Sunday & PH Rates'].iloc[a].replace('$',""))
                                print count, startingTime, '2'
                                return count + countCarPrice(timeStart, timeEnd, startingTime)
                            else:
                                count += 0
                                print count, startingTime
                    elif startingTime >= pd.to_datetime('22:30', format='%H:%M').time():
                        if timeStart == timeEnd:
                            count += 0
                            return count
                        elif timeEnd - timeStart < datetime.timedelta(minutes=510):
                            if userOutput['Sunday & PH Minimum'].iloc[a] != '30 mins':
                                count += 0
                                print count, startingTime, 'yo'
                            elif userOutput['Sunday & PH Minimum'].iloc[a] == '30 mins' and pd.to_datetime(userOutput['Start Time'].iloc[a], format='%H:%M').time() == pd.to_datetime('22:30', format='%H:%M').time():
                                timeStart += datetime.timedelta(minutes=30)
                                startingTime = pd.to_datetime(timeStart, format='%H:%M').time()
                                count += float(userOutput['Sunday & PH Rates'].iloc[a].replace('$', ""))
                                print count, startingTime, '3'
                                return count + countCarPrice(timeStart, timeEnd, startingTime)
                        elif timeEnd - timeStart >= datetime.timedelta(minutes=510) and pd.to_datetime(timeStart + datetime.timedelta(minutes=510), format='%H:%M').time() <= pd.to_datetime('07:00', format='%H:%M').time():
                            if userOutput['Sunday & PH Minimum'].iloc[a] == '510 mins':
                                timeStart += datetime.timedelta(minutes=510)
                                startingTime = pd.to_datetime(timeStart, format='%H:%M').time()
                                count += float(userOutput['Sunday & PH Rates'].iloc[a].replace('$',""))
                                print count, startingTime, '4'
                                return count + countCarPrice(timeStart, timeEnd, startingTime)
                            else:
                                count += 0
                                print count, startingTime
            a += 1


print 'The total price is %0.2f' % countCarPrice(timeStart, timeEnd, startingTime)
