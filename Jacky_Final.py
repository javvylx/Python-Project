import pandas as pd
import matplotlib.pyplot as plt
'''This is Jacky's Functions'''

def sortByArea():
    """Sorts the major shopping malls, attractions and hotel carpark by their area"""

    df = pd.read_csv('Datasets/Carpark Rates.csv', index_col='carpark')
    cat = df['category']

    cat_dict = {}

    #This is to add BOTH THE OCCURRENCE and NAME into a dictionary so can call it and display
    for x in cat:
        if x in cat_dict:
            cat_dict[x] +=1

        else:
            cat_dict[x] = 1

    cat_name = list(cat_dict.keys())
    cat_v = list(cat_dict.values())

    #plotting the chart, formatting the chart, bar chart to prevent labels from being cut off, automatically
    plt.rcParams.update({'figure.autolayout': True})
    fig, ax = plt.subplots()
    ax.barh(cat_name, cat_v)

    #this is to gain access to the label on x axis
    labels = ax.get_xticklabels()

    #rotation is the make the x axis text rotate
    plt.setp(labels, rotation=45, horizontalalignment='right')

    #setting the name
    ax.set(xlabel="Number of carparks", ylabel="Category/Area", title="Major Shopping Malls, Attractions and Hotels sorted by Category/Area")
    plt.show()


def sortByCarparkType():
    """Displays a piechart on the different types of carpark available in HDB Carparks"""
    df = pd.read_csv('Datasets/Hdb Carpark Information.csv')
    type = df['car_park_type']

    type_dict = {}

    #This is to add BOTH THE OCCURRENCE and NAME into a dictionary so can call it and display
    for x in type:
        if x in type_dict:
            type_dict[x] +=1

        else:
            type_dict[x] = 1
    newdict = {}
    otherNum = 0
    #Copying the data into another dictionary, compiling those below a certain number of occurrence into 1 category
    for (key, value) in type_dict.items():
        if type_dict[key] < 50:
            otherNum += value
            newdict.update({'Others': otherNum})
        else:
            newdict.update({key: value})

    #assigning the values into a list to be placed into the chart
    type_name = list(newdict.keys())
    type_v = list(newdict.values())
    #explode is used to pull a specific data in the chart so that it stands out
    explode = [0,0,1]

    fig1, ax1 = plt.subplots()
    #autopct is to show the percentage, based on the formatting selected
    #therefore chosen formatting is to display in 2 d.p.
    ax1.pie(type_v, labels=type_name, autopct='%.2f%%', explode=explode,
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    ax1.legend(type_name,
              title="The Different Types of Carpark",
               bbox_to_anchor=(1, 0), loc="lower right")

    ax1.set_title("Type of HDB Carparks")
    plt.show()


def sortCarTypeLots():
    """Displays a piechart for the total number of lots for the different vehicle type from URA Carpark data set"""
    df = pd.read_csv('Datasets/URA Carpark Information By Type Of Lot.csv')
    lotType = df.loc[:,['type_of_lot','number_of_lots']]

    lotType_dict = {}

    #This is to iterate through each and every rows in the data set
    for index,rows in lotType.iterrows():
        #to check if the type of lot is already in the dictionary or not
        if rows["type_of_lot"] in lotType_dict:
            #this is to retrieve SPECIFIC number of lots to add on to SPECIFIC type of lot
            lotType_dict[rows["type_of_lot"]] += rows["number_of_lots"]
        else:
            lotType_dict[rows["type_of_lot"]] = rows["number_of_lots"]

    #print(lotType_dict)


    #assigning the values to be placed in a list
    lotType_name = list(lotType_dict.keys())
    lotType_v = list(lotType_dict.values())

    fig1, ax1 = plt.subplots()
    #autopct is to show the percentage, based on the formatting selected
    #For this part, because showing the number of lots has more value than the percentage
    #i chose to show the value instead of percentage
    total = sum(lotType_v)
    ax1.pie(lotType_v, labels=lotType_name, autopct=lambda(p): '{:.0f}'.format(p * total / 100), startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    ax1.legend(lotType_name,
              title="The Different Types of Carpark",
               bbox_to_anchor=(1, 0), loc="lower right")

    ax1.set_title("Number of lots for different vehicle type")
    plt.show()

sortByArea()
sortByCarparkType()
sortCarTypeLots()