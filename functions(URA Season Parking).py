import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#data processing into dataframe
raw_data = pd.read_csv("Datasets/URA Season Parking.csv")
columns = raw_data.columns.tolist()
df = pd.DataFrame(raw_data, columns = columns)

def sortby_ticketType(chart_type = 'pie'):
    commercial = 0
    residential = 0

    for row in range(len(df)):
        if df.loc[row].ticket_type == 'Commercial':
            commercial += 1
        if df.loc[row].ticket_type == 'Residential':
            residential += 1
            
    labels = ('Commercial', 'Residential')
    sizes = [commercial, residential]

    fig1, ax1 = plt.subplots()
    colors = ['yellowgreen', 'lightskyblue']
    ax1.pie(sizes, labels=labels, colors = colors, autopct='%1.1f%%', shadow=True, startangle=90)

    ax1.axis('equal')
    plt.title("Types of Season Parking")

    plt.show()

#sortby_ticketType()

def sortby_montlyRate(chart_type = 'pie'):
    '''show a chart. pie/bar'''
    types = {}
    for item in df['monthly_rate'].tolist():
        if item not in types:
            types[int(item)] = 0
    types_keys = sorted(types.keys())
    
    for row in range(len(df)):
        types[int(df.loc[row].monthly_rate)] += 1
    

    objects = tuple('$' + str(v) for v in types_keys)
    y_pos = np.arange(len(objects))
    performance = [types[v] for v in types_keys]

    plt.bar(y_pos, performance, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    plt.ylabel('Number of URA Season Parking')
    plt.title('Costs of URA Season Parking')

    plt.show()

#sortby_montlyRate()

