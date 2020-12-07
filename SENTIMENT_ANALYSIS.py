import pandas as pd
import re
# Importing VADER the sentiment analysis model
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
# The sentiment analyzer model
sid = SentimentIntensityAnalyzer()

# Importing the data
df_donald = pd.read_csv("hashtag_donaldtrump.csv",
                        lineterminator='\n',
                        parse_dates=True)

df_joe = pd.read_csv("hashtag_joebiden.csv",
                        lineterminator='\n',
                        parse_dates=True)



# Function for cleaning the data
def clean_tweets(text):
  text = re.sub("RT @[\w]*:"," ",text) # REMOVING RETWEETS
  text = re.sub("@[\w]*"," ",text) # REMOVING TAGGING OF OTHER USERS
  text = re.sub("https?://[A-Za-z0-9./]*"," ",text) # REMOVING LINKS
  text = re.sub("\n"," ",text) # REMOVING NEW LINE INDICATIONS
  text = re.sub("#", " ", text) # REMOVING HASHTAGS
  return text

# Cleaning the tweets by using the apply function
df_donald['tweet'] = df_donald['tweet'].apply(lambda x: clean_tweets(x))
df_joe['tweet'] = df_joe['tweet'].apply(lambda x: clean_tweets(x))

############# EXAMPLE ############
#### TWEET BEFORE TOKENIZING
# @CLady62 Her 15 minutes were over long time ago. Omarosa never represented the black community! #TheReidOut \n\nShe
# cried to #Trump begging for a job!'

#### TWEET AFTER TOKENIZING
# Her 15 minutes were over long time ago. Omarosa never represented the black community!  TheReidOut   She cried to
# Trump begging for a job!


# Using VADER to get sentiment scores. The output is a dictionaire. Indexing to only get the final score
df_donald["sentiment_dic"] = df_donald['tweet'].apply(lambda x: sid.polarity_scores(x))
df_donald["sentiment"] = df_donald["sentiment_dic"].apply(lambda x: x["compound"])
#JOE BIDEN
df_joe["sentiment_dic"] = df_donald['tweet'].apply(lambda x: sid.polarity_scores(x))
df_joe["sentiment"] = df_joe["sentiment_dic"].apply(lambda x: x["compound"])

# Categorizing a sentiment score as either negative, neutral or positive
def sentimentVerdict(sentiment):
  if sentiment >= 0.05:
    return "Positive"
  elif sentiment <= -0.05:
    return "Negative"
  else:
    return "Neutral"

# Applying the function to the data
df_donald['sentiment_overall'] = df_donald['sentiment'].apply(lambda x: sentimentVerdict(x))
df_joe['sentiment_overall'] = df_joe['sentiment'].apply(lambda x: sentimentVerdict(x))

# Exporting the final data set as csv
df_donald.to_csv("./donald_with_sentiment.csv")
df_joe.to_csv("./joe_with_sentiment.csv")