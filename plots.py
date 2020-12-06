import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
from Preprocessing import get_tweets

# Importing the tweets
df = get_tweets()

############################ TWEETS PER STATE ######################################

# Grouping by state code and counting the number of tweets within each state
tweets_per_state = df.groupby(['code']).size().reset_index(name='counts').sort_values(by=['counts'], ascending=False)

# Doing the plotly magic
fig = go.Figure(data=go.Choropleth(
    locations=tweets_per_state['code'], # Spatial coordinates
    z = tweets_per_state['counts'].astype(float), # Data to be color-coded
    locationmode = 'USA-states', # set of locations match entries in `locations`
    colorscale = 'Reds',
    colorbar_title = "Tweets",
))

# Making labels
fig.update_layout(
    title_text = '2020 US Election Number of Tweets per State',
    geo_scope='usa', # limite map scope to USA
)

fig.show()

################### NUMBER OF TWEETS PR SENTIMENT ##################

# Grouping by sentiment label
grouped_by_overall_sentiment = df.groupby('sentiment_overall').size().reset_index(name = 'counts').sort_values(
    by =['counts'], ascending= False)

# Creating the indexes for the x axis
ind_3 = np.arange(3)

# Defining the x and y axis
plt.bar(ind_3, grouped_by_overall_sentiment['counts'], color = ['red','salmon','green'], width= 0.5)

# Creating the labels for the axis
plt.xticks(ind_3, grouped_by_overall_sentiment['sentiment_overall'])
plt.ylabel('Number of Tweets')
plt.title('Number of Tweets pr. sentiment')

plt.show()
plt.savefig('./plots/number_of_tweets_pr_sentiment.png')
plt.clf()


##################### NEGATIVE SENTIMENT PER STATE ##############################

# Filtering out all negative tweets
df_negative = df.loc[df['sentiment_overall'] == 'Negative']

# Grouping by state code and getting the mean sentiment value
abs_sentiment_per_state = df_negative.groupby('code')['sentiment'].mean().reset_index()

# Doing the plotly magic
fig = go.Figure(data=go.Choropleth(
    locations=abs_sentiment_per_state['code'], # Spatial coordinates
    z = abs_sentiment_per_state['sentiment'].astype(float), # Data to be color-coded
    locationmode = 'USA-states', # set of locations match entries in `locations`
    colorscale = 'Reds',
    colorbar_title = "Tweets",
))

# Making labels
fig.update_layout(
    title_text = '2020 US Election Negative Sentiment per State',
    geo_scope='usa', # limite map scope to USA
)

fig.show()

################### DEMOCRATIC STATES ARE MORE PRO BIDEN #######################

# Filtering out all Tweets from democratic states
democratic = df.loc[df['Result'] == 'Biden']

# Grouping by Hashtag and states
demo_grouped = democratic.groupby(['Hashtag', 'code'])['sentiment'].mean().reset_index()

# Making two new dataframes for trump tweets and for biden tweets
demo_grouped_trump = demo_grouped.loc[demo_grouped['Hashtag'] == 'DonaldTrump']
demo_grouped_biden = demo_grouped.loc[demo_grouped['Hashtag'] == 'JoeBiden']

# Making a list of uniques state codes
unique_demstates = demo_grouped.code.unique()

# Getting an array of the length of the state codes
state_codes = np.arange(len(unique_demstates))
width = 0.30

# Creating the plot
fig, ax = plt.subplots()
trump = ax.bar(state_codes - width/2, demo_grouped_trump['sentiment'], color = 'red', width = width, label = 'Trump')
biden = ax.bar(state_codes + width/2, demo_grouped_biden['sentiment'], color = 'blue', width = width, label = 'Biden')
ax.set_xticks(state_codes)
ax.set_xticklabels(demo_grouped_trump['code'])
plt.xticks(rotation=90)
# Making the layout
ax.legend()
ax.set_ylabel('Sentiment')
ax.set_title('Mean Sentiment in Democratic States')
fig.tight_layout()

plt.show()
plt.clf()

################### SENTIMENT AS ELECTION DAY APPROACHES #####################

# Grouping by days before election
days = df.groupby('days_before_election')['abs_sentiment'].mean().reset_index()

# Making the plot
fig, ax = plt.subplots()
ax.plot('days_before_election', 'abs_sentiment', data=days)
ax.set_ylabel('Sentiment')
ax.set_title('The sentiment as election day approaches')

plt.show()
plt.savefig("./plots/sentiment_as_election_day_approaches")
plt.clf()

################## TRUMP TWEETS MORE VALENCED THAN BIDEN TWEETS? ###########################

# Grouping tweets by hashtag and getting the mean absolute valence
grouped_by_hashtag = df.groupby('Hashtag')['abs_sentiment'].mean().reset_index()

# Creating the plot
ind = np.arange(2)
p1 = plt.bar(ind, grouped_by_hashtag['abs_sentiment'], color = ['red', 'blue'], width = 0.5)
plt.xticks(ind, grouped_by_hashtag['Hashtag'])
plt.ylabel('Sentiment')
plt.title('Mean Absolute Sentiment per Hashtag')

plt.show()
plt.clf()


