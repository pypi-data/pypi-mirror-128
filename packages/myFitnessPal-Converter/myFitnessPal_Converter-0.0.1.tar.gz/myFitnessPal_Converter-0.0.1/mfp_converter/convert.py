import pandas as pd
def convert(csv):
    df = pd.read_csv(csv) #import myFitnesspal dataframe through app
    a = df.groupby('Date') #group df by date
    b = a.sum() #sum of calories in Breakfast/Lunch/Dinner/Snacks
    b.index = pd.to_datetime(b.index) #changes dates to datetime format
    b.drop(columns='Note', inplace = True) #drop unneccessary column unless wanted
    b["Month"] = b.index.month_name(locale = 'English') #sets index by month
    c = b.groupby("Month") 
    d = c.mean()
    b.to_csv("myFitnesspal_avgbyday.csv") #shows average macronutrients/micronutrients/vitamins by day
    b
    print("Converted CSV to show averages by day as 'myFitnesspal_avgbyday.csv'.")
    d.to_csv("myFitnesspal_avgbymonth.csv") #shows average macronutrients/micronutrients/vitamins by month
    d
    print("Converted CSV to show averages by month as 'myFitnesspal_avgbymonth.csv'.")


