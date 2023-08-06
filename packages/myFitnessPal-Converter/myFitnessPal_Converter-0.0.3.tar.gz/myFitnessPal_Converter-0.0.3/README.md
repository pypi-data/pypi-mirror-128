
<!-- ABOUT THE PROJECT -->
## About The Project
myFitnesspal's premium "Export your Information" feature exports a CSV file of your progress meal data into 4 categories being Breakfast, Lunch, Dinner and Snacks. 

This project is a Python package created to show the average of those 4 categories to add up towards the whole day to be able to see total Macronutrients and Micronutrients for the day or month instead of total Macronutrients and Micronutrients for Breakfast, Lunch, Dinner, and Snacks. 

This was created to be able to see the average Macronutrients and Micronutrients including vitamins and other data pieces as a whole/all-in-one per day or month in a CSV instead of the total being split up per Breakfast, Lunch, Dinner and Snacks by default. 

Seeing this data as a whole helps understand progress better and allows for better visualization and data analysis depending on the use case.

This converter produces two new .csv files from the original .csv file you provide. (*Disclaimer:* The csv you provide is received in an email from myFitnessPal when using the export function if you have a premium membership)
## Example conversion:
### By Month
![converter](https://i.gyazo.com/8fc6817903d664ce945f75f2744d6d99.png)
### By Day
![converterday](https://i.gyazo.com/ba7a3ed0c244dc6fc0904eb1111c28dd.png)
## Example dashboard that can be derived from using this package:
![conv](https://github.com/YoussefSultan/myFitnesspalDataConverter/blob/master/myFitnesspal_Dashboard.png?raw=true)
### Built With
 
* [Python](https://www.python.org/downloads/) 

<!-- GETTING STARTED -->
## Getting Started
`pip install myFitnessPal-Converter`
```python
from mfp_converter.convert import convert
convert(r"\Directory\Of\myFitnessPalExport.csv")
```
### More information on the project
* [GitHub](https://github.com/YoussefSultan/myFitnesspalDataConverter)
<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request
