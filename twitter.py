from __future__ import division
from string import punctuation

# Preprocessing tweets
tweets = open("obama_tweets.txt").read()
tweets_list = tweets.split('\n')
for t in tweets_list:
    t = t.lower()
for p in punctuation:
    tweets_list = [t.replace(p, '') for t in tweets_list]

# Setting up lists to check whether a file is good or not
with open("positive.txt", "r") as pos:
    positive_words = pos.read().splitlines()

with open("negative.txt", "r") as neg:
    negative_words = neg.read().splitlines()



# Processing tweets
for tweet in tweets_list:
    positive_counter, negative_counter = 0, 0

    words = tweet.split(' ')
    for word in words:
        if word in positive_words:
            positive_counter += 1
        elif word in negative_words:
            negative_counter += 1

    print positive_counter/len(words), ' ', negative_counter/len(words)
