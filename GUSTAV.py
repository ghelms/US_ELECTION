import pandas as pd
from wordcloud import WordCloud, STOPWORDS

# Importing full dataset for donald trump
df_donald = pd.read_csv("hashtag_donaldtrump.csv",
                        lineterminator='\n',
                        parse_dates=True)
# Subsetting the data
columns_of_interest = ["created_at", "tweet", "likes", "retweet_count", "user_join_date", "user_followers_count", "state"]
df_donald = df_donald[columns_of_interest].iloc[0:2000]


# Importing data from Biden
df_biden = pd.read_csv("hashtag_donaldtrump.csv",
                        lineterminator='\n',
                        parse_dates=True)

# Subsetting Biden data
df_biden = df_biden[columns_of_interest].iloc[0:2000]

tweets_donald = "".join(df_donald['tweet'].tolist())

# Updating the stopwords for wordclouds
STOPWORDS.update({"https", "co","amp"})
print("https" in STOPWORDS)


# Trying to make a wordcloud
wordcloud = WordCloud(
    width=3000,
    height=2000,
    random_state=1,
    collocations=False,
    background_color="Green").generate(tweets_donald)

wordcloud.to_file("./plots/wordcloud_donald.png")

df = pd.read_csv("co2_emission.csv")

print(df.columns)

print(df.Year)

df_min = df[["Entity","Year"]]
print(df_min.iloc[0:200])


