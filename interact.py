"""
interact.py : Get followers through retweeting and favs.
Some functions here are also simply helpers to check our twitter account.
"""

import tweepy
import positive
import random
import os
from credentials import our_id

def choose_tweet(api, id):
    """
    Given some userid, choose which tweet should be acted upon. To do that,
    chose the tweet Twitter users liked the most."""
    # Count = 10 to avoid retweeting old things so we're less robot-like
    tweets = api.user_timeline(user_id=id, count=10)
    most_popular = max(t.retweet_count + t.favorite_count for t in tweets)
    for t in tweets:
        if t.retweet_count + t.favorite_count == most_popular:
            return t.id

def pick_prospect(api):
    """
    So far we just choose at random.
    """
    return random.choice(get_prospect_list(api, False))

def get_prospect_list(api=None, refresh=False):
    """Builds a list of prospects from Twitter if refresh, else uses the cached one.
    This is our id : 3130995473.
    Twitter's doc states that we will receive last followed people first, but
    that this behaviour is subject to change.
    """
    if refresh:
        os.remove('prospects')
        friends = api.friends_ids(user_id=our_id)
        with open('prospects', 'w') as prospects:
            prospects.write("\n".join(str(f) for f in friends))
    with open('prospects', 'r') as prospects:
        return prospects.read().split('\n')

def random_action(api):
    """
    Returns a randomly selected function between retweeting and adding to fav.
    """
    return random.choice((api.create_favorite, api.retweet))

if __name__ == '__main__':
    api = tweepy.API(positive.setup_auth())
    for i in range(7):
        print(i)
        tweet_id = choose_tweet(api, pick_prospect(api))
        #FIXME: Understand why sometimes next line throws a 403.
        try:
            a = random_action(api)
            a(tweet_id)
        except:
            print(a, tweet_id)
            break
