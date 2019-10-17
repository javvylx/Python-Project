import pandas as pd
import matplotlib.pyplot as plt
import requests


def carparkInfoList():
    url = "https://api.data.gov.sg/v1/transport/carpark-availability"  # Calling API data from Data.gov.sg {Function 1]
    carparkdata = requests.get(url).json()["items"][0][
        "carpark_data"]  # Requests the URL data into Json format then store carparkdata into a list
    """ Creating a list to store the parameters """
    lottypelist = []
    lotavaillist = []
    totallotlist = []
    updatetimelist = []
    updatedatelist = []
    carparknumlist = []
    lotsoccupiedlist = []

    for key in carparkdata:  # Loop thru carpark data & put the values into a list
        lottypelist.append(key["carpark_info"][0]["lot_type"])
        lotavaillist.append(key["carpark_info"][0]["lots_available"])
        totallotlist.append(key["carpark_info"][0]["total_lots"])
        updatedatelist.append(key["update_datetime"][:10])
        updatetimelist.append(key["update_datetime"][11:])  # Slice of
        carparknumlist.append(key["carpark_number"])
        lotsoccupiedlist.append(  # Deducting count of the total lots - totalavailable
            int(key["carpark_info"][0]["total_lots"]) - int(key["carpark_info"][0]["lots_available"]))

    carparkpandadict = {"car_park_no": carparknumlist,
                        "Lot Type": lottypelist,
                        "Lots Available": lotavaillist,
                        "Lots Occupied": lotsoccupiedlist,
                        "Total Lots": totallotlist,
                        "Update Date": updatedatelist,
                        "Update Time": updatetimelist
                        }

    df = pd.DataFrame(carparkpandadict)  # Integrating dictionary carpark dictionary to pandas dataframe

    print df  # Print out whole dataframe for carpark availablity

    carparkinfodf = pd.read_csv("Datasets/Hdb Carpark Information.csv")  # Read the HDB Carpark Info csv dataset

    finaldf = pd.merge(df, carparkinfodf[['car_park_no', 'address']], on=['car_park_no'])
    # Merging API to CSV's key "car_park_no", to join "address" to "carpark availability" dataset

    finalef = finaldf[["car_park_no", "address"]]

    print finalef  # Print only two parameters in this dataframe
    # finaldf.to_csv("Sample.csv")

    userInput1 = raw_input("Please choose the Carpark Number that you would want to search: ")
    # Request for user input to allow use to choose the carpark no they want to search

    carparkNumber = userInput1.upper()
    # Increase the font size so that it will match the dataset value's uppercase too.

    SearchCarParkNum = finaldf[finaldf['car_park_no'].str.match(carparkNumber)]
    # Create a dataframe of the carpark number that was searched by the unit n find a match for it

    print "\n", "The Carpark Information selected is:\n ", SearchCarParkNum[["car_park_no", "address"]]
    # List out the carpark number & address selected by the user. {Function 2}

    print "\n", SearchCarParkNum[["Total Lots", "Lots Available", "Lots Occupied", "Update Date", "Update Time"]]

    # List the Total Lots, Lots Available, Lots Occupied, Update Date & Update Time {Function 3}

    print "\nData has also been output into a text file."

    textout = open('carparkquery.txt', 'w')
    print >> textout, "\n", "The Carpark Information selected is:\n ", SearchCarParkNum[["car_park_no", "address"]]
    print >> textout, "\n", SearchCarParkNum[
        ["Total Lots", "Lots Available", "Lots Occupied", "Update Date", "Update Time"]]

    # Export into text file {Function 4}

    lotsoccupied = 0  # Iterate 0 to lotsoccupied
    lotsavail = 0  # Iterate 0 to lotsavail

    for index, rows in SearchCarParkNum.iterrows():
        if rows["Lots Occupied"] > 0:  # loop thru, the rows of the user search data
            lotsoccupied += rows[
                "Lots Occupied"]  # if there are more than one row, the lots occupied, in the row to total up everything
        else:
            lotsoccupied = rows["Lots Occupied"]  # if there is one row, the value will be equals the searched item

        if rows["Lots Available"] > 0:
            lotsavail += int(rows[
                                 "Lots Available"])  # if there are more than one row, the lots available, in the row to total up everything
        else:
            lotsavail = int(rows["Lots Available"])  # if there is one row, the value will be equals the searched item

    labels = ["Carpark\nOccupied", "Carpark\nAvailable"]  # Create Labels for Bar Chart
    values = [lotsoccupied, lotsavail]  # Store Values in List
    totaldata = lotsoccupied + lotsavail  # Get the total lots data
    plt.bar(labels, values)  # Plot out bar graph
    plt.title(
        "Bar Chart of" + " " + carparkNumber + " " + "carpark(s) that has Occupied lots & Lots available" + "\n" + "(Total HDB Parking Lots = %d)" % totaldata)
    plt.show()  # Show bar graph


def BasementCarparkPieChart():
    """User searches for carpark address, then displays carpark basement available for that carpark. Then finally display all the information in a pie chart."""
    carparkinfodf = pd.read_csv("Datasets/Hdb Carpark Information.csv", index_col=0)  # Read the HDB Carpark Info csv dataset

    print carparkinfodf[["address", "car_park_basement"]]  # Print only two parameters in this dataframe

    carparkInput = raw_input("Please enter a carkpark address: ").title()  # Convert the input to title
    carparkInputUpper = carparkInput.upper()  # Convert the input to upper case
    # test = (carparkinfodf.loc[(carparkinfodf['address'] == carparkInput)])

    SearchCarParkName = carparkinfodf[
        carparkinfodf['address'].str.contains(carparkInputUpper)]  # Convert the input to upper case
    SearchCarParkName.sort_values(by="car_park_basement",
                                  ascending=True)  # Sorting the values of carpark basement in ascending case

    ndata = SearchCarParkName.loc[SearchCarParkName["car_park_basement"] == "N"].count()[
        0]  # Locate carpark basement parameter 'N' in the dataframe
    ydata = SearchCarParkName.loc[SearchCarParkName["car_park_basement"] == "Y"].count()[
        0]  # Locate carpark basement parameter 'Y' in the dataframe
    explodeplt = (0, 0.1)
    labels = ["No\nCarpark\nBasement", "Carpark\nhas\nBasement"]  # Labels for the pie chart

    plt.pie([ndata, ydata], explode=explodeplt, labels=labels, autopct="%.2f%%", shadow=True)
    # Display lotsoccupied & lotsavail in pie chart

    plt.title("Pie Chart of" + " " + carparkInput + " " + "carpark(s) that has basements")

    plt.show()  # Show Pie Chart

"""Pak's Function"""
def TypesOfCarparkSystemBarGraph():
    carparkinfodf = pd.read_csv("Hdb Carpark Information.csv", index_col=0)
    carparksystemdf = carparkinfodf[["address", "type_of_parking_system"]]

    eparkingdata = carparksystemdf.loc[carparksystemdf["type_of_parking_system"] == "ELECTRONIC PARKING"].count()[0]
    cparkingdata = carparksystemdf.loc[carparksystemdf["type_of_parking_system"] == "COUPON PARKING"].count()[0]

    explodeplt = (0, 0.1) # Explode the data to make it look neater
    labels = ["Electronic\nParking", "Coupon\nParking"]
    totaldata = eparkingdata + cparkingdata # Total the parking lots

    plt.pie([eparkingdata, cparkingdata], explode=explodeplt, labels=labels, autopct="%.2f%%", shadow=True)
    plt.title("Electronic Parking vs Coupon Parking\n (Total HDB Parking Lots = %d)" % totaldata)  # Display EPS vs CP & display total parking lots
    plt.show()  # Show PieChart


# carparkInfoList()
# BasementCarparkPieChart()
# TypesOfCarparkSystemBarGraph()
