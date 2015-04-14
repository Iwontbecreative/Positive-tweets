"""
Those are functions that use REST api to check users timelines and add
them and check whether text is positive or negative about a topic.
"""

from __future__ import division
from string import punctuation
import tweepy
import credentials as c
from credentials import our_id

with open("positive.txt", "r") as pos:
    positive_words = pos.read().splitlines()

with open("negative.txt", "r") as neg:
    negative_words = neg.read().splitlines()


def preprocess(tweet):
    """
    Takes a tweet and preprocesses it so as to enhance detection rate.
    """
    tweet = tweet.lower()
    for p in punctuation:
        tweet = tweet.replace(p, "")
    return tweet


def check_on_topic(tweet, keywords):
    """
    Checks whether some text is on the right topic
    """
    return any(True for k in keywords if k in preprocess(tweet))


def check_pos(tweet):
    """Checks whether a tweet is positive or not."""
    positive_counter, negative_counter = 0, 0
    for word in tweet.split(' '):
        if word in positive_words:
            positive_counter += 1
        elif word in negative_words:
            negative_counter += 1

    if positive_counter > negative_counter:
        return True


def setup_auth():
    """
    Dummy function to avoid importing credentials everytime
    """
    auth = tweepy.OAuthHandler(c.consumer_key, c.consumer_secret)
    auth.set_access_token(c.access_token, c.access_token_secret)
    return auth


def is_prospect(author, topic, about_topic=0.15):
    """
    Checks whether enough (about_topic) of author tweets are about topic.
    """
    if author == our_id:
        return False
    api = tweepy.API(setup_auth())
    try:
        tweets = [t.text for t in api.user_timeline(user_id=author, count=50)]
    except tweepy.error.TweepError:
        print("Too many requests")
        return
    # Checks whether enough tweets are about our topic.
    # This is quite stringent : only about 5% of authors pass this stage
    return len([True for t in tweets if check_on_topic(t, topic)]) > about_topic * len(tweets)


def follow(author_id):
    """
    Follows the id user on Twitter.
    """
    api = tweepy.API(setup_auth())
    api.create_friendship(user_id=author_id)
