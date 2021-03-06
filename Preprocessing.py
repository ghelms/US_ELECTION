# Defining a function for preprocessing the
def get_tweets():
    # Importing the modules needed
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

    # Creating absolute sentiment column
    df_both['abs_sentiment'] = abs(df_both['sentiment'])

    ########################### DATE MANIPULATION ###################################

    # convert date columns into datetime object
    df_both[['user_join_date', 'collected_at', 'created_at']] = df_both[
        ['user_join_date', 'collected_at', 'created_at']].apply(pd.to_datetime, format='%Y-%m-%d %H:%M:%S.%f')

    # create columns for day_tweeted and hour_tweeted
    df_both['day_tweeted'] = df_both['created_at'].dt.strftime('%Y-%m-%d')

    # create column for days since user creation
    election_date = pd.to_datetime('2020-11-03')
    df_both['days_since_user_creation'] = df_both['created_at'] - df_both['user_join_date']
    df_both['days_since_user_creation'] = df_both['days_since_user_creation'] / np.timedelta64(1, 'D')

    # Create column days before election
    df_both['days_before_election'] = election_date - df_both['created_at']
    df_both['days_before_election'] = df_both['days_before_election'] / np.timedelta64(1, 'D')
    df_both['days_before_election'] = [round(number) for number in
                                       df_both['days_before_election']]  # Rounding to next whole integer

    # create column indicating which year-month the account was created
    df_both["account_year_month"] = df_both["user_join_date"].dt.strftime('%Y-%m')

    ######################## ADDING THE VOTING RESULTS ###############################

    # Listing all the states and the voting result of that state
    states = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware",
              "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana",
              "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana",
              "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina",
              "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina",
              "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia",
              "Wisconsin", "Wyoming"]
    result = ["Donald", "Donald", "Biden", "Donald", "Biden", "Biden", "Biden", "Biden", "Donald", "Biden", "Biden",
              "Donald", "Biden", "Donald", "Donald", "Donald", "Donald", "Donald", "Biden", "Biden", "Biden", "Biden",
              "Biden", "Donald", "Donald", "Donald", "Donald", "Biden", "Biden", "Biden", "Biden", "Biden", "Donald",
              "Donald", "Donald", "Donald", "Biden", "Biden", "Biden", "Donald", "Donald", "Donald", "Donald", "Donald",
              "Biden", "Biden", "Biden", "Donald", "Biden", "Donald"]
    code = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA',
            'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK',
            'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']

    # Creating a dictionaire with the voting results
    data = {'state': states,
            'code': code,
            'Result': result}

    # Converting it to a data frame
    df_results = pd.DataFrame(data)

    # Merging the result to the data frame and filtering all data with no state out
    df = pd.merge(df_both, df_results, how="outer", on="state")
    df = df.loc[:, ~df.columns.str.match('Unnamed: 0')]

    return df
