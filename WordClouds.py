import pandas as pd
from wordcloud import WordCloud, STOPWORDS
from Preprocessing import get_tweets

# Importing the tweets
df = get_tweets()

# Filtering out #DonaldTrump tweets
trump = df.loc[df['Hashtag'] == 'DonaldTrump']

# Filtering out #JoeBiden tweets
biden = df.loc[df['Hashtag'] == 'JoeBiden']

# Making a string with the tweets
tweets_donald = "".join(trump['tweet'].tolist())
tweets_biden = "".join(biden['tweet'].tolist())

# Updating the stopwords for wordclouds
STOPWORDS.update({"https", "co","amp","Twitter","will","DonaldTrump","JoeBiden","go","el","il","per","now","U"})
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
wordclouder(tweets_biden, "Wordcloud_Biden")



