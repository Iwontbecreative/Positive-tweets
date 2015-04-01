"""
interact.py : Get followers through retweeting and favs.
Some functions here are also simply helpers to check our twitter account.
"""

import tweepy
import twitter
import random

def choose_tweet(api, id):
    """
    Given some userid, choose which tweet should be acted upon. To do that,
    chose the tweet Twitter users liked the most."""
    # Count = 10 to avoid retweeting too old things so we're less robot-like
    tweets = api.user_timeline(user_id=id, count=10)
    most_popular = max(t.retweet_count + t.favorite_count for t in tweets)
    for t in tweets:
        if t.retweet_count + t.favorite_count == most_popular:
            return t.id

def pick_prospect(api):
    """
    Chooses a prospect to interact with.
    This is our id : 3130995473.
    Twitter's doc states that we will receive last followed people first, but
    that this behaviour is subject to change.
    For now we chose at random.
    """
    friends = api.friends_ids(user_id=3130995473)
    return random.choice(friends)

def random_action(api):
    """
    Returns a randomly selected function between retweeting and adding to fav.
    """
    return random.choice((api.create_favorite, api.retweet))

if __name__ == '__main__':
    api = tweepy.API(twitter.setup_auth())
    random_action(api)(choose_tweet(api, pick_prospect(api)))
