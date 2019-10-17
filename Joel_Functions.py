import pandas as pd
##############FUNCTION 1 AND 2######################################
def sortbyinputandbarh_hdbcarpark():
    data = pd.read_csv('data/hdb-carpark-information.csv') #reads the csv
    print data.columns

    try:
        firstchoice = raw_input('First filter: ')  # first category
        secchoice = raw_input('Second filter: ')  # second category
#check why the try and exccept is not working. [check]
    except:
        print "Please key in the correct category!"
        quit()

    selectionofcategories= data[[firstchoice.lower(),secchoice.lower()]] #this will show the results of the selected categories
    print selectionofcategories

    sortby1= raw_input('Sort by ? : ') #sorting first category by Type of parking* to follow the function
    sortby2= raw_input('Sort by ? : ') #sort by second category Type of parking system
    firstmainchoices = (selectionofcategories.loc[(selectionofcategories[firstchoice.lower()].str.contains(sortby1.upper())) & #this sorts based on first choice followed by 2nd
                                              (selectionofcategories[secchoice.lower()]).str.contains(sortby2.upper())])
    print firstmainchoices


#####################################################FUNCTION 3###########################################################
def sortbyinputandplotbar_uracp():
    data = pd.read_csv('data/ura-carpark-information-by-type-of-lot.csv')  # reads the csv
    sorteddata= data.sort_values(['number_of_lots','type_of_lot'],ascending=False) #initially will sort the list based on the lots in descending order
    wanttoparkarea= raw_input('Key in the area that you would like to park at eg, Pasir ris, Tampines etc. :')
    typeoflot=raw_input('What type of lot would you like? Motor Car / Motor Cycle / Heavy Vehicle:') #take in user inputs based on the titles
    sortbylocation= (sorteddata.loc[(sorteddata['ura_carpark_name']).str.contains(wanttoparkarea.upper()) &
                                (sorteddata['type_of_lot']).str.contains(typeoflot.title())]) #sorts the list based on the input keyed in, take nte .title will take in
    print sortbylocation

#1) labels the 'town' and 'number of lots' so that it is the arguement taken in, 2) use the bar graph to plot
#for plotting the graph
    import matplotlib.pyplot as plt
    labelingbyarea= sortbylocation.ura_carpark_name  #sorting by the carpark address
    lotsavailable= sortbylocation.number_of_lots #sorting by the number of lots
    plt.barh(labelingbyarea,lotsavailable)
    plt.subplots_adjust(left = 0.38) #subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=None) adjusted so that the text can be seen
    plt.show()




