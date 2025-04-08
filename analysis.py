import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns
import sqlite3

from clean_data import load_data

df = load_data()

# Create a column in the dataset to show revenue per month. 
df['revenue_per_month'] = (df['price'] + df['service_fee']) * df['reviews_per_month']
df = df.dropna(subset=['revenue_per_month'])

# Create a dataframe including the top 1% of listings based on revenue per month.
top_df = df.sort_values('revenue_per_month', ascending=False).head(int(len(df)/100))

# Find the number of duplicates in each column. 
col = ['host_identity_verified', 'host_name', 'neighbourhood_group', 'neighbourhood', 'instant_bookable', 'cancellation_policy', 'room_type', 'price', 'service_fee', 'minimum_nights', 'reviews_per_month', 'review_rate_number', 'calculated_host_listings_count', 'availability_365']

# Value counts to count each unique value.
# Top duplicates to show duplicates present in more than 15% of the relevant column.

queries = {}
for i in col:
    value_counts = top_df[i].value_counts()
    top_duplicates = value_counts[value_counts > int(len(top_df)*0.15)]

    if not top_duplicates.empty:
        queries[i] = top_duplicates.to_frame().reset_index()
 
sql_col = ['neighbourhood_group', 'instant_bookable', 'cancellation_policy', 'room_type', 'minimum_nights', 'review_rate_number', 'calculated_host_listings']

# Converting the dataframe to a database to be used with sqlite.                      
conn = sqlite3.connect("airbnb_db.db")
cursor = conn.cursor()

# Create a table 
cursor.execute(""" 
CREATE TABLE IF NOT EXISTS airbnb_db (
               id INTEGER PRIMARY KEY,
               name TEXT,
               host_id INTEGER, 
               host_identity_verified TEXT,
               host_name TEXT,
               neighbourhood_group TEXT,
               neighbourhood TEXT, 
               lat FLOAT,
               long FLOAT,
               country TEXT,
               country_code TEXT,
               instant_bookable TEXT,
               cancellation_policy TEXT,
               room_type TEXT,
               construction_year FLOAT,
               price FLOAT,
               service_fee FLOAT, 
               minimum_nights FLOAT, 
               number_of_reviews FLOAT,
               last_review TEXT,
               reviews_per_month FLOAT,
               review_rate_number FLOAT,
               calculated_host_listings_count FLOAT,
               availability_365 FLOAT,
               house_rules TEXT,
               license TEXT
)
""")

# Drop existing table if exists before replacing the data.
cursor.execute("DROP TABLE IF EXISTS airbnb_db")
conn.commit()

df.to_sql('airbnb_db', conn, if_exists='replace', index=False)

# Verify the data has been imported
#cursor.execute("SELECT * FROM airbnb_db LIMIT 1")

# Query average revenue per month based on the above columns. 
def query_average_revenue_per_month(x):
    return pd.read_sql_query(f"""
        SELECT ROUND(AVG((price + service_fee) * reviews_per_month)) AS revenue_per_month,
        {x}
        FROM airbnb_db
        WHERE price IS NOT NULL AND service_fee IS NOT NULL AND reviews_per_month IS NOT NULL AND {x} IS NOT NULL
        GROUP BY {x}
        ORDER BY revenue_per_month DESC
        LIMIT 10
    """, conn)

sql_col = ['neighbourhood_group', 'instant_bookable', 'cancellation_policy', 'room_type', 'minimum_nights', 'review_rate_number', 'calculated_host_listings_count']
sql_queries = {}

for i in sql_col:
    sql_queries[i] = query_average_revenue_per_month(i)

# Charts
# Neighbourhood Groups
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 4)) 

# Neighbourhood Groups - Top 1% plot
ax1 = sns.barplot(data=queries['neighbourhood_group'], x = 'neighbourhood_group', y='count', color='dimgrey', ax=ax1)
ax1.set_ylim(0, 180)
ax1.set_title("Neighbourhood Groups - Top 1% of listings")
ax1.set_xlabel('Trending Neighbourhood Groups in the 1%')
ax1.set_ylabel('Quantity of listings in the 1%')
for i in ax1.containers:
    ax1.bar_label(i, fmt=lambda x: f'{int(x)} ({(x / (len(df)/100) * 100):.0f}% of the 1%)')

# Neighbourhood Groups - Whole dataset plot
ax2 = sns.barplot(data=sql_queries['neighbourhood_group'], x='neighbourhood_group', y='revenue_per_month', color='dimgrey', ax=ax2)
ax2.set_title("Neighbourhoods and Average Revenue per Month - Whole dataset")
ax2.set_xlabel('Neighbourhood Groups')
ax2.set_ylabel('Average Revenue per month')
ax2.set_ylim(800, 1400)
for i in ax2.containers:
    ax2.bar_label(i,)

plt.tight_layout()
plt.savefig("charts/1_neighbourhood_groups_-_1%_vs_whole_dataset.png")
plt.close()

# Cancellation Policy
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 4)) 

# Cancellation Policy - Top 1% plot
ax1 = sns.barplot(data=queries['cancellation_policy'], x = 'cancellation_policy', y='count', color='dimgrey', ax=ax1)
ax1.set_title("Cancellation Policy - Top 1% of listings")
ax1.set_xlabel('Cancellation Policy')
ax1.set_ylabel('Quantity of listings in the 1%')
ax1.set_ylim(110, 170)
for i in ax1.containers:
    ax1.bar_label(i, fmt=lambda x: f'{int(x)} ({(x / (len(df)/100) * 100):.0f}% of the 1%)')

# Cancellation Policy - Whole dataset plot
ax2 = sns.barplot(data=sql_queries['cancellation_policy'], x='cancellation_policy', y='revenue_per_month', color='dimgrey', ax=ax2)
ax2.set_title("Cancellation Policy and Average Revenue per Month - Whole dataset")
ax2.set_xlabel('Cancellation Policy')
ax2.set_ylabel('Average Revenue per month')
ax2.set_ylim(950, 1100)
for i in ax2.containers:
    ax2.bar_label(i,)

plt.tight_layout()
plt.savefig("charts/2_cancellation_policy_-_1%_vs_whole_dataset.png")
plt.close()


# Instantly Bookable
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 4)) 

# Instantly Bookable - Top 1% plot
ax1 = sns.barplot(data=queries['instant_bookable'], x = 'instant_bookable', y='count', color='dimgrey', ax=ax1)
ax1.set_title("Instantly Bookable - Top 1% of listings")
ax1.set_xlabel('Instantly Bookabile')
ax1.set_ylabel('Quantity of listings in the 1%')
ax1.set_ylim(170, 240)
for i in ax1.containers:
    ax1.bar_label(i, fmt=lambda x: f'{int(x)} ({(x / (len(df)/100) * 100):.0f}% of the 1%)')

# Instantly Bookable - Whole dataset plot
ax2 = sns.barplot(data=sql_queries['instant_bookable'], x='instant_bookable', y='revenue_per_month', color='dimgrey', ax=ax2)
ax2.set_title("Instantly Bookable and Average Revenue per Month - Whole dataset")
ax2.set_xlabel('Instantly Bookable')
ax2.set_ylabel('Average Revenue per month')
ax2.set_ylim(990, 1100)
ax2.set_xticks([0, 1])
ax2.set_xticklabels(['False', 'True'])
for i in ax2.containers:
    ax2.bar_label(i,)

plt.tight_layout()
plt.savefig("charts/3_instantly_bookable_-_1%_vs_whole_dataset.png")
plt.close()

# Room Type
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 4)) 

# Room Type - Top 1% plot
ax1 = sns.barplot(data=queries['room_type'], x = 'room_type', y='count', color='dimgrey', ax=ax1)
ax1.set_title("Room Type - Top 1% of listings")
ax1.set_xlabel('Trending Room Types in the 1%')
ax1.set_ylabel('Quantity of listings in the 1%')
ax1.set_ylim(160, 240)
for i in ax1.containers:
    ax1.bar_label(i, fmt=lambda x: f'{int(x)} ({(x / (len(df)/100) * 100):.0f}% of the 1%)')

# Room Type - Whole dataset plot
ax2 = sns.barplot(data=sql_queries['room_type'], x='room_type', y='revenue_per_month', color='dimgrey', ax=ax2)
ax2.set_title("Room Type and Average Revenue per Month - Whole dataset")
ax2.set_xlabel('Room Types')
ax2.set_ylabel('Average Revenue per month')
ax2.set_ylim(800, 1150)
for i in ax2.containers:
    ax2.bar_label(i,)

plt.tight_layout()
plt.savefig("charts/4_room_type_-_1%_vs_whole_dataset.png")
plt.close()

# Minimum Nights
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 4)) 

# Minimum Nights - Top 1% plot
ax1 = sns.barplot(data=queries['minimum_nights'], x = 'minimum_nights', y='count', color='dimgrey', ax=ax1)
ax1.set_title("Minimum Nights - Top 1% of listings")
ax1.set_xlabel('Trending No. of Minimum Nights in the 1%')
ax1.set_ylabel('Quantity of listings in the 1%')
ax1.set_ylim(0, 350)
for i in ax1.containers:
    ax1.bar_label(i, fmt=lambda x: f'{int(x)} ({(x / (len(df)/100) * 100):.0f}% of the 1%)')

# Minimum Nights - Whole dataset plot
ax2 = sns.barplot(data=sql_queries['minimum_nights'], x='minimum_nights', y='revenue_per_month', color='dimgrey', order=sql_queries['minimum_nights']['minimum_nights'], ax=ax2)
ax2.set_title("Minimum Nights and Average Revenue per Month - Whole dataset")
ax2.set_xlabel('Minimum No. of Nights')
ax2.set_ylabel('Average Revenue per month')
ax2.set_ylim(300, 1650)
for i in ax2.containers:
    ax2.bar_label(i,)

plt.tight_layout()
plt.savefig("charts/5_minimum_no_nights_-_1%_vs_whole_dataset.png")
plt.close()

# Review Rate Number
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 4)) 

# Review Rate Number - Top 1% plot
ax1 = sns.barplot(data=queries['review_rate_number'], x ='review_rate_number', y='count', color='dimgrey', ax=ax1)
ax1.set_title("Review Rate Number - Top 1% of listings")
ax1.set_xlabel('Trending Review Ratings in the 1%')
ax1.set_ylabel('Quantity of listings in the 1%')
ax1.set_ylim(80, 130)
for i in ax1.containers:
    ax1.bar_label(i, fmt=lambda x: f'{int(x)} ({(x / (len(df)/100) * 100):.0f}% of the 1%)')

# Review Rate Number - Whole dataset plot
ax2 = sns.barplot(data=sql_queries['review_rate_number'], x='review_rate_number', y='revenue_per_month', color='dimgrey', ax=ax2)
ax2.set_title("Reveiw Rate Number and Average Revenue per Month - Whole dataset")
ax2.set_xlabel('Review Rating')
ax2.set_ylabel('Average Revenue per month')
ax2.set_ylim(720, 1150)
for i in ax2.containers:
    ax2.bar_label(i,)

plt.tight_layout()
plt.savefig("charts/6_review_rating_-_1%_vs_whole_dataset.png.png")
plt.close()

# No. of Listings
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 4)) 

# No. of Listings - Top 1% plot
ax1 = sns.barplot(data=queries['calculated_host_listings_count'], x = 'calculated_host_listings_count', y='count', color='dimgrey', ax=ax1)
ax1.set_title("No. Host Listings - Top 1% of listings")
ax1.set_xlabel('Trending No. of Host Listings in the 1%')
ax1.set_ylabel('Quantity of listings in the 1%')
ax1.set_ylim(0, 230)
for i in ax1.containers:
    ax1.bar_label(i, fmt=lambda x: f'{int(x)} ({(x / (len(df)/100) * 100):.0f}% of the 1%)')

# No. of Listings - Whole dataset plot
ax2 = sns.barplot(data=sql_queries['calculated_host_listings_count'], x='calculated_host_listings_count', y='revenue_per_month', color='dimgrey', order=sql_queries['calculated_host_listings_count']['calculated_host_listings_count'], ax=ax2)
ax2.set_title("No. Host Listings and Average Revenue per Month - Whole dataset")
ax2.set_xlabel('No. of Host Listings')
ax2.set_ylabel('Average Revenue per month')
ax2.set_ylim(1050, 2350)
for i in ax2.containers:
    ax2.bar_label(i,)

plt.tight_layout()
plt.savefig("charts/7_no_host_listings_-_1%_vs_whole_dataset.png")
plt.close()

conn.close()
