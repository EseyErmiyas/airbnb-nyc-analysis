# Airbnb NYC Data Analysis

An analysis project reviewing the listings in New York City. The project identifies factors influencing revenue and compares high performing listings with the overall dataset, providing insights from the available data. 

## Project Structure
Airbnb_Open_data.csv    # Original dataset
clean_data.py           # Cleans and Filters the dataset
analysis.py             # Runs Pandas queries, SQL queries and generates charts. 
notebook.ipynb          # Jupyter notebook combining data cleaning, analysis, and insights
airbnb_db.db            # SQLite database created from cleaned data
/charts                 # Output folder for generated charts
requirements.txt        # Required python packages
README.md               # This file

## How to Run

Option 1                # Run analysis.ipynb in VSCode or Jupyter
Option 2                # Run clean_data.py followed by analysis.py

## Dataset 
[Airbnb NYC Open Data](https://www.kaggle.com/datasets/arianazmoudeh/airbnbopendata/data)

## Key features
Cleans and filters the dataset for analysis
Identifies and drop outliers based on percentile
Includes a method for finding dominant/duplicate values in a dataset
Converts the clean dataset into sql database for further analysis
Compares the 1% of performing listings against the dataset as a whole
Generates charts side by side for comparison

## Conclusion
This analysis reveals patterns among high performing listings, though has limitations. 
The Top 1% analysis may reflect more popular factors rather than factors that improve revenue. 
Averages can be significant skewed by outliers. Including group counts and/or filtering groups with a low representation may help. 
Revenue doesn't equate to profit and thus balanced results provide limited insight.

## Key Insights
A private or shared room, in the Bronx or Queens would be best when listing your property. 
The cancellation policy and being able to book the listing instantly doesn't seem to have a direct relation to revenue per month. 
The optimal minimum number of nights is 1 or 2. 
A rating of 3 or 4 is optimal. Having a rating of 1 negatively impacts revenue. A rating of 5 shows less revenue than a rating of 4 indicating diminishing returns. 
The number of properties owned by the host doesn't impact the average revenue for a specific listing. 
