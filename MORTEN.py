import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors
from matplotlib.ticker import PercentFormatter

# load csv files
df_donald = pd.read_csv("donald_with_sentiment.csv", lineterminator="\n", parse_dates=True)  # read donald csv file
df_joe = pd.read_csv("joe_with_sentiment.csv", lineterminator="\n", parse_dates=True)  # read joe csv file
df_both = pd.concat([df_donald, df_joe])

# replace "United States" with "United States of America"
df_donald.loc[df_donald['country'] == "United States", 'country'] = "United States of America"
df_joe.loc[df_donald['country'] == "United States", 'country'] = "United States of America"
df_both.loc[df_donald['country'] == "United States", 'country'] = "United States of America"

# subset csv file to test code faster
donald_small = df_donald.dropna(subset=['country', 'tweet']).iloc[0:10000]
joe_small = df_joe.dropna(subset=['country', 'tweet']).iloc[0:10000]
both_small = df_both.dropna(subset=['country', 'tweet']).iloc[0:10000]

# group by country and count number of tweets
country_both = both_small.groupby(['country']).size().reset_index(name='counts').sort_values(by=['counts'],
                                                                                             ascending=False)
country_both = country_both.loc[country_both['counts'] > 100]

# group by source and count number of tweets

source_both = both_small.groupby(['source']).size().reset_index(name='count').sort_values(by=['count'], ascending=False)

# making "other" category

source_both_top = source_both[:5].copy()
source_both_other = pd.DataFrame(data={'source': ['others'], 'count': [source_both['count'][5:].sum()]})
source_both_new = pd.concat([source_both_top, source_both_other])

# make bar plot

# plt.bar(source_joe['source'], source_joe['count'])
# plt.xlabel('Sources')
# plt.xticks(rotation=90)
# plt.ylabel('Frequency')
# plt.savefig('./plots/sources.png')
# plt.clf()

# make pie chart:
# fig, axes = plt.subplots(nrows = 1, ncols = 2, figsize = (20,8))
# source_joe_new.plot(kind = 'pie', y = 'count', labels = source_joe_new['source'], ax = axes[0], autopct='%1.1f%%')
# source_joe_top.plot(kind = 'pie', y = 'count', labels = source_joe_top['source'], ax = axes[1], autopct='%1.1f%%')
# axes[0].set_title('all countries')
# axes[1].set_title('top 5')
# plt.savefig('./plots/sources_pie_top.png')
# plt.clf()

# convert date columns into datetime object

both_small[['user_join_date', 'collected_at', 'created_at']] = both_small[['user_join_date', 'collected_at', 'created_at']].apply(pd.to_datetime, format='%Y-%m-%d %H:%M:%S.%f')

# create columns for day_tweeted and hour_tweeted

both_small['day_tweeted'] = both_small['created_at'].dt.strftime('%Y-%m-%d')
both_small['hour_tweeted'] = both_small['created_at'].dt.strftime('%Y-%m-%d %H' + ":00")

# create column for days since user creation
election_date = pd.to_datetime('2020-11-03')
both_small['days_since_user_creation'] = election_date - both_small['user_join_date']
both_small['days_since_user_creation'] = both_small['days_since_user_creation'] / np.timedelta64(1, 'D')

# finding hourly tweets and daily tweets
hourly_tweeting = both_small.groupby(['hour_tweeted']).size().reset_index(name='counts')
daily_tweeting = both_small.groupby(['day_tweeted']).size().reset_index(name='counts')

# create column indicating which year-month the account was created

both_small["account_year_month"] = both_small["user_join_date"].dt.strftime('%Y-%m')
user_creation = both_small.groupby(['account_year_month']).size().reset_index(name='counts')

# selecting only US tweets and dropping rows where state is na

usa_both = both_small.loc[both_small['country'] == 'United States of America'].dropna(
    subset=['state'])

usa_joe

usa_donald




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




states = set(sent_don_small1['state'])
states.remove('District of Columbia')
states.remove('Northern Mariana Islands')

# sent_don_small1['voting_rights']=sent_don_small1['state'].apply(lambda x: 'Yes' if x in states else 'No')

don_states_mean = sent_don_small1.groupby('state')['sentiment'].mean().reset_index()
joe_states_mean = sent_joe_small1.groupby('state')['sentiment'].mean().reset_index()

states_sent = pd.DataFrame({'state': joe_states_mean['state'],
                            'biden': joe_states_mean['sentiment'],
                            'trump': don_states_mean['sentiment']})

plt.plot(states_sent['state'], states_sent['biden'], label='Biden')
plt.plot(states_sent['state'], states_sent['trump'], label='Trump')
plt.ylabel('sentiment')
plt.xticks(rotation=90)
plt.show()

plt.clf()

# descriptive stats

# plot sentiment per day per data set

# state results combined with sentiment and number of tweets

# data visualization with ggplot or other packages

# does time since joining twitter predict sentiment analysis (x-axis: how long on twitter, y-axis: sentiment score)


import plotly.express as px

fig = px.choropleth(locationmode="USA-states", color=[1,2,3], scope="usa")
fig.show()


import plotly.graph_objects as go

import pandas as pd
df = pd.read_csv('2011_us_ag_exports.csv')

fig = go.Figure(data=go.Choropleth(
    locations=df['code'], # Spatial coordinates
    z = df['total exports'].astype(float), # Data to be color-coded
    locationmode = 'USA-states', # set of locations match entries in `locations`
    colorscale = 'Reds',
    colorbar_title = "Millions USD",
))

fig.update_layout(
    title_text = '2011 US Agriculture Exports by State',
    geo_scope='usa', # limite map scope to USA
)

fig.show()

dict = {'code' : df['code'], 'state' : df['state']}

df_state_code = pd.DataFrame(dict)