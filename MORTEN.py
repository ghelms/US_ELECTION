import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors
from matplotlib.ticker import PercentFormatter

# load csv files
df_donald = pd.read_csv("hashtag_donaldtrump.csv", lineterminator="\n", parse_dates=True) # read donald csv file
df_biden = pd.read_csv("hashtag_joebiden.csv", lineterminator="\n", parse_dates=True) # read joe csv file


# subset csv file
df_don_small = df_donald.dropna(subset=['country', 'tweet']).iloc[0:10000]
df_joe_small = df_biden.dropna(subset=['country', 'tweet']).iloc[0:10000]

# replace "United States" with "United States of America"
df_don_small.loc[df_donald['country'] == "United States", 'country'] = "United States of America"
df_joe_small.loc[df_joe_small['country'] == "United States", 'country'] = "United States of America"

# group by country and count number of tweets

country_don = df_don_small.groupby(['country']).size().reset_index(name='counts').sort_values(by=['counts'], ascending = False)
country_don = country_don.loc[country_don['counts'] > 100]

# make bar plot

plt.bar(country_don.country, country_don.counts, align = 'center')
plt.xlabel('Countries')
plt.xticks(rotation=90)
plt.ylabel('Frequency')
plt.savefig('./plots/countries.png')
plt.clf()

# group by source and count number of tweets

source_joe = df_joe_small.groupby(['source']).size().reset_index(name='count').sort_values(by=['count'], ascending = False)

# make bar plot

plt.bar(source_joe['source'], source_joe['count'])
plt.xlabel('Sources')
plt.xticks(rotation=90)
plt.ylabel('Frequency')
plt.savefig('./plots/sources.png')
plt.clf()

# making "other" category

source_joe_top =  source_joe[:5].copy()
source_joe_other = pd.DataFrame(data = {'source' : ['others'],'count' : [source_joe['count'][5:].sum()]})
source_joe_new = pd.concat([source_joe_top, source_joe_other])

# make pie chart:
fig, axes = plt.subplots(nrows = 1, ncols = 2, figsize = (20,8))
source_joe_new.plot(kind = 'pie', y = 'count', labels = source_joe_new['source'], ax = axes[0], autopct='%1.1f%%')
source_joe_top.plot(kind = 'pie', y = 'count', labels = source_joe_top['source'], ax = axes[1], autopct='%1.1f%%')
axes[0].set_title('all countries')
axes[1].set_title('top 5')
plt.savefig('./plots/sources_pie_top.png')
plt.clf()

# i want to see which days most tweets were made
# concatenate trump and biden data frames

df_both_small = pd.concat([df_don_small, df_joe_small])

# convert date columns into datetime object

df_both_small[['user_join_date','collected_at', 'created_at']] = df_both_small[['user_join_date','collected_at', 'created_at']].apply(pd.to_datetime, format='%Y-%m-%d %H:%M:%S.%f')

# create column in year-month-day format

df_both_small['day_tweeted'] = df_both_small['created_at'].dt.strftime('%Y-%m-%d')
df_both_small['hour_tweeted'] = df_both_small['created_at'].dt.strftime('%Y-%m-%d %H' + ":00")

hourly_tweeting = df_both_small.groupby(['hour_tweeted']).size().reset_index(name='counts')
daily_tweeting = df_both_small.groupby(['day_tweeted']).size().reset_index(name='counts')

# create column indicating which year-month the account was created

df_both_small["account_year_month"] = df_both_small["user_join_date"].dt.strftime('%Y-%m')
user_creation = df_both_small.groupby(['account_year_month']).size().reset_index(name='counts')

# create some visualization

fig, ax = plt.subplots()
ax.plot('account_year_month', 'counts', data=user_creation)
plt.show()
plt.clf()

# convert date columns to correct object type

# df_biden[['user_join_date','collected_at', 'created_at']] = df_biden[['user_join_date','collected_at',
# 'created_at']].apply(pd.to_datetime, format='%Y-%m-%d %H:%M:%S.%f') df_donald[['user_join_date','collected_at',
# 'created_at']] = df_donald[['user_join_date','collected_at', 'created_at']].apply(pd.to_datetime, format='%Y-%m-%d
# %H:%M:%S.%f')

# sentiment analysis

sentiment_donald = pd.read_csv("donald_with_sentiment.csv", lineterminator="\n", parse_dates=True)
sentiment_joe = pd.read_csv("joe_with_sentiment.csv", lineterminator="\n", parse_dates=True)

sentiment_donald.loc[sentiment_donald['country'] == "United States", 'country'] = "United States of America"
sentiment_joe.loc[sentiment_joe['country'] == "United States", 'country'] = "United States of America"

# creating subset
sentiment_don_small = sentiment_donald.loc[sentiment_donald['country'] == 'United States of America'].dropna(subset = ['state']).iloc[0:10000]
sent_don_small1 = sentiment_don_small[['created_at', 'likes', 'retweet_count', 'source', 'user_join_date', 'user_followers_count', 'state', 'sentiment', 'sentiment_overall']]

sentiment_joe_small = sentiment_joe.loc[sentiment_joe['country'] == 'United States of America'].dropna(subset = ['state']).iloc[0:10000]
sent_joe_small1 = sentiment_joe_small[['created_at', 'likes', 'retweet_count', 'source', 'user_join_date', 'user_followers_count', 'state', 'sentiment', 'sentiment_overall']]


states=set(sent_don_small1['state'])
states.remove('District of Columbia')
states.remove('Northern Mariana Islands')

# sent_don_small1['voting_rights']=sent_don_small1['state'].apply(lambda x: 'Yes' if x in states else 'No')

don_states_mean = sent_don_small1.groupby('state')['sentiment'].mean().reset_index()
joe_states_mean = sent_joe_small1.groupby('state')['sentiment'].mean().reset_index()

states_sent=pd.DataFrame({'state':joe_states_mean['state'],
                          'biden':joe_states_mean['sentiment'],
                          'trump':don_states_mean['sentiment']})

plt.plot(states_sent['state'], states_sent['biden'], label = 'Biden')
plt.plot(states_sent['state'], states_sent['trump'], label = 'Trump')
plt.ylabel('sentiment')
plt.xticks(rotation = 90)
plt.show()

plt.clf()


# descriptive stats

# plot sentiment per day per data set

# state results combined with sentiment and number of tweets

# data visualization with ggplot or other packages

# does time since joining twitter predict sentiment analysis (x-axis: how long on twitter, y-axis: sentiment score)

