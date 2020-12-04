import pandas as pd
import numpy


# Importing the original data
df_donald = pd.read_csv("hashtag_donaldtrump.csv",
                        lineterminator='\n',
                        parse_dates=True)

df_joe = pd.read_csv("hashtag_joebiden.csv",
                        lineterminator='\n',
                        parse_dates=True)


# Subsetting the data
columns_of_interest = ["created_at", "tweet", "likes", "retweet_count", "user_join_date", "user_followers_count", "state"]
df_donald = df_donald[columns_of_interest].iloc[0:2000]
df_joe = df_joe[columns_of_interest].iloc[0:2000]

# Combining the two dataframes into one
df_both = pd.concat([df_donald, df_joe])

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

# Making it into a dictionaire
data = {'state': states,
        'Result': result}

# Converting it to a data frame
df_results = pd.DataFrame(data)

# Merging the result to the data frame and sorting all those tweets out that does not have a state indicator
df = pd.merge(df_both, df_results, on= "state")