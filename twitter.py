from __future__ import division
from string import punctuation
import json

tweets = []
authors = []
prospects = []

def preprocess(tweet):
    """
    Takes a tweet and preprocesses it so as to enhance detection rate.
    """
    tweet = tweet.lower()
    for p in punctuation:
        tweet = tweet.replace(p, '')
    return tweet

# Json loader bugs with very large files. Therefore, we will parse it line
# by line. Don't try to use load() to gain space, it won't work.

with open("test", "r") as parsed_tweets:
    for line in parsed_tweets:
        # Need to save it to avoid calling json.loads twice
        tweet = json.loads(line)
        tweets.append(tweet['text'])
        authors.append(tweet['user']['id'])

tweets = [preprocess(t) for t in tweets]

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
        prospects.append(authors[i])

with open("potential clients2.txt", "a") as c:
    c.write("\n".join([str(i) for i in prospects]))
