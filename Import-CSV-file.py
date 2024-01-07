import pandas as pd 
import matplotlib.pyplot as plt 

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

rolling_df = table.rolling(window=6).mean()

plt.figure(figsize=(15,10)) 
plt.xticks(fontsize=11)
plt.yticks(fontsize=11)
plt.xlabel('Date',fontsize=12)
plt.ylabel('Number of posts',fontsize=12)
plt.ylim(0,30000)


for column in rolling_df.columns:
    plt.plot(rolling_df.index, rolling_df[column],linewidth=2,label=rolling_df[column].name)
plt.legend(fontsize=12)

