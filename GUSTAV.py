import pandas as pd
from wordcloud import WordCloud, STOPWORDS
from varname import nameof

# Importing full dataset for donald trump
df_donald = pd.read_csv("hashtag_donaldtrump.csv",
                        lineterminator='\n',
                        parse_dates=True)
# Subsetting the data
columns_of_interest = ["created_at", "tweet", "likes", "retweet_count", "user_join_date", "user_followers_count", "state"]
df_donald = df_donald[columns_of_interest].iloc[0:2000]


# Importing data from Biden
df_biden = pd.read_csv("hashtag_joebiden.csv",
                        lineterminator='\n',
                        parse_dates=True)

# Subsetting Biden data
df_biden = df_biden[columns_of_interest].iloc[0:2000]

# Making a string with the tweets
tweets_donald = "".join(df_donald['tweet'].tolist())
tweets_biden = "".join(df_biden['tweet'].tolist())

# Updating the stopwords for wordclouds
STOPWORDS.update({"https", "co","amp","Twitter","will","DonaldTrump","JoeBiden"})
print("https" in STOPWORDS)


# Making a wordcloud function
def wordclouder(text, filename):
    wordcloud = WordCloud(
    width=3000,
    height=2000,
    random_state=1,
    collocations=False,
    background_color="salmon").generate(text)

    #Exporting the wordcloud as a file
    wordcloud.to_file("./plots/{}.png".format(filename))

#Using the function
wordclouder(tweets_donald, "Wordcloud_Trump")
wordclouder(tweets_biden, "Wordcloud_Donald")



