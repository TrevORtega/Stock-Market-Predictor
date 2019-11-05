import math

"""Author:  Trevor Ortega
   Date:    Started: 9/2018, Last Update: 5/2019
   Purpose: User inputs a date or a price. Based on the input choice
            of the user, the program makes predictions on the Dow Jones
            market. (i.e. given a price, the program predicts the date when the
            market will be at that price. Given a date, the program predicts the
            price of the market at that time
"""

# checks if price is correct format xx.xx(needed in order to match the .txt files)
def is_price(intitialPrice):
    #check the digit that is third from last (should be a decimal)
    periodChecker = intitialPrice[len(intitialPrice) - 3]
    
    if periodChecker == '.':
        return float(intitialPrice)
    else:
        raise Exception("Incorrect Format (maybe add decimal point)")

#determine if year is valid and seperates year into 3 categories
#3 different types of dates: in 1985.txt, in 1914.txt, or not included in .txt files
def yearSort(year, dateType):
    # dates not included in .txt files
    if year > 2018 or (year > 1968 and year < 1984):
        dateType = 2
        return dateType
    
    # dow jones 1985.txt
    elif year > 1984:
        dateType = 3
        return dateType
    
    # dow jones 1914.txt    
    elif year > 1914:
        dateType = 1
        return dateType
    
    else:
        raise Exception("Year needs to be after 1914")
        

#make sure month is a valid month of the year
def monthSort(month):
    if month < 0 or month > 13:
        raise Exception("Year needs to be after 1914")


#determines whether or not input is a date or a price, 
def dateOrPrice(userInput):
    
    if userInput == "price":
        initial_price = input("Enter a price e.g(1709.06)\n")
        
        #check if price is correct format
        priceFin = is_price(initial_price)
        
        #runs the prediction functions around the price
        price(priceFin)
        
    elif userInput == "date":
        #runs the prediction functions around the date
        date()
        
    else:
        raise Exception("Incorrect Format (maybe add decimal point)")

# determines months since 1915 and creates the final date if a date is given
def dateFormat(y, m):
    # calculates months since 1915
    monthsSince1915 = ((y - 1915) * 12) + m
    
    # final date format m/1/yyyy 
    finalDate = str(m) + "/1/" + str(y)
    
    return monthsSince1915, finalDate


# predict the price if a correct date is given
def priceFormula(monthsSince):
    # Date formula
    PredictPrice = round(12.315 * (1.54 * monthsSince + 20.73 * math.sin((2 * 3.14159 / 51) * monthsSince)) + 1315.88, 2)
    print("Predicted Price: $" + str(PredictPrice))
    
    
#predict the future date with the given price and find if price is in dow jones files
def price(price1):
    isPrice = True
    
    #predict the future date the price will be at
    predictDate(price1)
    
    getFrom1985(None, None, isPrice)
    getFrom1914(None, None, isPrice)
    return

def date():
    #represents which dataset the year is in (if it's in one at all)
    dateType = None;
    
    year = int(input("Enter a year\n"))
    #make sure year is valid, and if return which type of dataset it is in
    dateType = yearSort(year, dateType)
    
    month = int(input("Enter the month\n"))
    monthSort(month)
    
    #get final version of date and months since 1985
    monthsSince, dateFin = dateFormat(year, month)
    priceFormula(monthsSince)
    
    #price is included in 1985.txt
    if(dateType == 3):
        getFrom1985(dateFin, dateType, None)
        
    #price is included in 1914.txt
    elif(dateType == 2):
        getFrom1914(dateFin, dateType, None)
    investPeriod(monthsSince)
    





# predict the date if a correct price is given
def predictDate(price):
    #initialize the month and year
    month = 0
    year = 0
    # price formula is months = (price - 1315.88) / 19.051
    monthsSince = int(round((price - 1315.88) / 19.051))
    print(str(monthsSince) + " months since 1915")
    # find the month for the date
    if monthsSince > 12:
        year = int(monthsSince / 12)
        month = monthsSince - (year * 12)
    # the month can never be zero in a date
    if monthsSince == 0 or month == 0:
        month = 1
    else:
        month = monthsSince
    print("Predicted date:", month, "/1/", year + 1915)
    investPeriod(monthsSince)

# value will be in dow jones 1985.txt
def getFrom1985(date, dateType, isPrice):
    # open up file and give back the correct date or price
    data1985 = open("Dow Jones 1985.txt")
    # for every line in data, check if the file date matches the given date
    for lines in data1985:
        values85 = lines.split()
        if dateType == 3:
            if values85[0] == date:
                print("Actual price: $" + str(values85[1]))
        if isPrice == True:
            if str(price) == values85[1]:
               print("Actual date: " + str(values85[0]))
    data1985.close()
    
    
# value will be in dow jones 1914.txt
def getFrom1914(date, dateType, isPrice):
    # open up file and give back the correct date or price
    data1914 = open("dow jones 1914 with inflation.txt")
    # for every line in data, check if the file date matches the given date
    for rows in data1914:
        values14 = rows.split()
        if dateType == 1:
            if values14[0] == date:
                print("Actual price: $" + str(values14[2]))
        if isPrice == True:
            if str(price) == values14[2]:
               print("Actual date: " + str(values14[0]))
    data1914.close()


# predict whether or not to invest for a period of time
# avg market pattern intervals is 36 month increase followed by 15 month decrease (36+15=51)
def investPeriod(monthsSince):
    interval = int(monthsSince / 51)
    monthsSinceInterval = monthsSince - (51 * interval)
    
    # this is the derivative of the other price function; if positive the market is profitable, if negeative it is not
    is_positive = 34.04 * math.cos(.1232 * monthsSince) + 20.53
    
    if (is_positive > 0): # the month is profitable
        print("Advice: Invest as soon as possible during this month")
    else: # the month is not profitable
        print("Advice: Don't invest or sell during this month")

"""
Format: 1. ask for price / date
2. determine whether price / date is valid
3. if date is valid, format it properly. if price is valid, convert to float/ format
4. for a price: find date value in text files. for date: find price value in text files
5. for price: predict date value. for date: predict price value
6. determine timeframe to invest

"""


# ask user for a date or a price
userInput = input("Enter whether you wish to enter a date or a price\n")
#determine whether input is price or date
dateOrPrice(userInput)

