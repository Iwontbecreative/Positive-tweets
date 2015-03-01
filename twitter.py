from __future__ import division
from string import punctuation
import json

# Recovering and preprocessing tweets

# It's easier to make 2 lists than alist of list, especially for debugging
# purposes.
tweets = []
authors = []
clients = []

# This is commented out, don't remove, needed to document steps taken
# tweets = open("obama_tweets.txt").read()

# Json loader bugs with very large files. Therefore, we will parse it line
# by line. Don't try to use load() to gain space, it won't work.

with open("tweets", "r") as parsed_tweets:
    for line in parsed_tweets:
        # Need to save it to avoid calling json.loads twice
        tweet = json.loads(line) 
        tweets.append(tweet['text'])
        authors.append(tweet['user']['id'])

# Standardizing tweets to enhance detection rate
tweets = [t.lower() for t in tweets]
for p in punctuation:
    tweets = [t.replace(p, '') for t in tweets]

#print tweets, authors

# Setting up lists to check whether a file is good or not
with open("positive.txt", "r") as pos:
    positive_words = pos.read().splitlines()

with open("negative.txt", "r") as neg:
    negative_words = neg.read().splitlines()

# Processing tweets
for i, tweet in enumerate(tweets):
    positive_counter, negative_counter = 0, 0

    words = tweet.split(' ')
    for word in words:
        if word in positive_words:
            positive_counter += 1
        elif word in negative_words:
            negative_counter += 1

    # FIXME This might be too leniant a definition of a positive tweet
    if positive_counter > negative_counter:
        clients.append(authors[i])


