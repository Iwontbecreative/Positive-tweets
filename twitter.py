"""
Builds a list of prospects. This will be the prospects we will try to interact
with. To work, this needs a file of tweets such as the one generated by
gather_tweets.py.
"""

from __future__ import division
from string import punctuation
import json
import tweepy
from gather_tweets import setup_auth, keywords

tweets = []
authors = []


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


parse("tweets")
tweets = [preprocess(t) for t in tweets]

# Setting up lists to check whether a word is good or not
with open("positive.txt", "r") as pos:
    positive_words = pos.read().splitlines()

with open("negative.txt", "r") as neg:
    negative_words = neg.read().splitlines()

# Stringent tests to check whether someone is a prospect.
for prospect, tweet in zip(authors, tweets):
    if check_pos(tweet):
        # We need to make sure the person is worth interacting with before
        # adding it to our prospect list. For that, we make sure at least x%
        # (default is 10%) of tweets are about data.
        api = tweepy.API(setup_auth())
        try:
            tweets = [t.text for t in api.user_timeline(user_id=prospect, count=100)]
        except:
            print "Too many requests"
            break
        topic_tweets = [True for t in tweets if any(True for k in keywords if k in preprocess(t))]
        if len(topic_tweets) > 10:
            with open("prospects", "a") as prospects:
                prospects.write(str(prospect) + "\n")
