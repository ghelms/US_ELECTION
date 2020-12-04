import pandas as pd
import numpy as np

# Importing the original data
df_donald = pd.read_csv("donald_with_sentiment.csv",
                        lineterminator='\n',
                        parse_dates=True)

df_joe = pd.read_csv("joe_with_sentiment.csv",
                     lineterminator='\n',
                     parse_dates=True)

# Creating a hashtag variable
df_donald['Hashtag'] = "DonaldTrump"
df_joe['Hashtag'] = "JoeBiden"

# Combining the two dataframes into one
df_both = pd.concat([df_donald, df_joe])

# Renaming USA
df_both.loc[df_donald['country'] == "United States", 'country'] = "United States of America"

# Filtering out results from USA
df_both = df_both.loc[df_both['country'] == 'United States of America']


########################### DATE MANIPULATION ###################################

# convert date columns into datetime object
df_both[['user_join_date', 'collected_at', 'created_at']] = df_both[
    ['user_join_date', 'collected_at', 'created_at']].apply(pd.to_datetime, format='%Y-%m-%d %H:%M:%S.%f')

# create columns for day_tweeted and hour_tweeted
df_both['day_tweeted'] = df_both['created_at'].dt.strftime('%Y-%m-%d')
df_both['hour_tweeted'] = df_both['created_at'].dt.strftime('%Y-%m-%d %H' + ":00")

# create column for days since user creation
election_date = pd.to_datetime('2020-11-03')
df_both['days_since_user_creation'] = election_date - df_both['user_join_date']
df_both['days_since_user_creation'] = df_both['days_since_user_creation'] / np.timedelta64(1, 'D')

# create column indicating which year-month the account was created
df_both["account_year_month"] = df_both["user_join_date"].dt.strftime('%Y-%m')

######################## ADDING THE VOTING RESULTS ###############################

# Listing all the states and the voting result of that state
states = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "Florida",
          "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine",
          "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska",
          "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio",
          "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas",
          "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"]
result = ["Donald", "Donald", "Biden", "Donald", "Biden", "Biden", "Biden", "Biden", "Donald", "Biden", "Biden",
          "Donald", "Biden", "Donald", "Donald", "Donald", "Donald", "Donald", "Biden", "Biden", "Biden", "Biden",
          "Biden", "Donald", "Donald", "Donald", "Donald", "Biden", "Biden", "Biden", "Biden", "Biden", "Donald",
          "Donald", "Donald", "Donald", "Biden", "Biden", "Biden", "Donald", "Donald", "Donald", "Donald", "Donald",
          "Biden", "Biden", "Biden", "Donald", "Biden", "Donald"]

# Creating a dictionaire with the voting results
data = {'state': states,
        'Result': result}

# Converting it to a data frame
df_results = pd.DataFrame(data)

# Merging the result to the data frame
df = pd.merge(df_both, df_results, how = "outer", on= "state")

# Exporting to csv file
df.to_csv("./FINAL_DATA.csv")