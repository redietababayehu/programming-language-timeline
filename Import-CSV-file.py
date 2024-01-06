import pandas as pd 


df = pd.read_csv('QueryResults.csv', names=['DATE', 'TAG', 'POSTS'], header=0)

#reading the amount of posts each language has
df.groupby('TAG').sum()

#number of months of entries for each language
df.groupby('TAG').count()

# looking at the dates and changing the format
df.DATE[1]
df.DATE = pd.to_datetime(df.DATE)
#changes all of the date format 
df.head()

#change the order of the table 
table = df.pivot(index='DATE', columns='TAG', values='POSTS')

# remove the NaN values 
table.count()
table.fillna(0, inplace=True) 
table.fillna(0)

table.isna().values.any()

