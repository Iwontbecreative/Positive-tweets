"""
interact.py : Get followers through retweeting and favs.
"""

import tweepy
import json
import twitter

def choose_tweet(api, id):
    """
    Given some userid, choose which tweet should be acted upon. To do that,
    chose the tweet Twitter users liked the most."""
    tweets = api.user_timeline(user_id=id)
    most_popular = max(t.retweet_count + t.favorite_count for t in tweets)
    for t in tweets:
        if t.retweet_count + t.favorite_count == most_popular:
            return t.id

if __name__ == '__main__':
    api = tweepy.API(twitter.setup_auth())
    #api.retweet(choose_tweet(api, 2777103822))
