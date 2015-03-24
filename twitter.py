"""
Builds a list of prospects. This will be the prospects we will try to interact
with. To work, this needs a file of tweets such as the one generated by
gather_tweets.py. 
"""

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
        tweet = tweet.replace(p, "")
    return tweet

# Json loader bugs with very large files. Therefore, we will parse it line
# by line. Don't try to use load() to gain space, it won't work.
def parse(filename):
    """
    This parses a file to recover tweets and user_ids and puts them on their
    respective lists.
    """
    with open(filename, "r") as json_tweets:
        for line in json_tweets:
            # Need to save it to avoid calling json.loads twice
            tweet = json.loads(line)
            tweets.append(tweet['text'])
            authors.append(tweet['user']['id'])

def check_pos(tweet):
    """Checks whether a tweet is positive or not."""
    positive_counter, negative_counter = 0, 0
    for word in tweet.split(' '):
        if word in positive_words:
            positive_counter += 1
        elif word in negative_words:
            negative_counter += 1

    # FIXME This might be too leniant a definition of a positive tweet
    if positive_counter > negative_counter:
        return True

parse("test")
tweets = [preprocess(t) for t in tweets]

# Setting up lists to check whether a word is good or not
with open("positive.txt", "r") as pos:
    positive_words = pos.read().splitlines()

with open("negative.txt", "r") as neg:
    negative_words = neg.read().splitlines()

# Processing tweets
for i, tweet in enumerate(tweets):
    if check_pos(tweet):
        prospects.append(authors[i])

with open("potential clients2.txt", "a") as c:
    c.write("\n".join([str(i) for i in prospects]))
