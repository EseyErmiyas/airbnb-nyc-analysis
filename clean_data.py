import pandas as pd

# Create a function to clean data for use in the analysis script. 
def load_data():
    """
    Load and Clean the New York Airbnb dataset
    Returns a cleaned dataframe
    """

    df = pd.read_csv('Airbnb_Open_Data.csv', parse_dates=['last review'], dtype={'license':object})

    # Correct the column names
    df.columns = df.columns.str.replace(' ','_').str.lower()

    # Correct the neighbourhood_group name from 'brookln' to 'Brooklyn'
    df.neighbourhood_group = df.neighbourhood_group.replace('brookln', 'Brooklyn')

    # Convert 'price' and 'service_fee' from string to float
    Col = ['price', 'service_fee']

    for i in Col:
        df[i] = pd.to_numeric(df[i].replace(r'[^\d.]', '', regex=True), errors='coerce')

    # Drop duplicates and NA values
    df = df.drop_duplicates(subset=['name', 'host_name', 'last_review', 'lat', 'long'], keep='first')

    check_na = ['price', 'neighbourhood', 'neighbourhood_group', 'number_of_reviews', 'host_name', 'review_rate_number', 'reviews_per_month', 'availability_365']
    df = df.dropna(subset=check_na)
 
    # Reset the index due to dropping duplicate and na values.
    df.reset_index(drop=True, inplace=True)

    # Review outliers based on the 1st and 99th percentile.
    check_outliers = ['price', 'service_fee', 'minimum_nights', 'number_of_reviews', 'reviews_per_month', 'calculated_host_listings_count']
    #print(df.describe()[check_outliers])

    qua1 = []
    qua2 = []
    
    for i in check_outliers:
        qua1.append(df[i].quantile(0.99))
        qua2.append(df[i].quantile(0.01))

    def check(x):
        for a in check_outliers:
            if x[a] > qua1[check_outliers.index(a)] or x[a] < qua2[check_outliers.index(a)]:
                return False
            
            elif x['minimum_nights'] <= 0:
                return False
            
            elif x['availability_365'] <= 0:
                return False
            
            else:
                continue
        
        return True
    
    df = df[df.apply(lambda x: True if (check(x) == True) else False, axis=1)]
    # Return the data frame. 
    return df
