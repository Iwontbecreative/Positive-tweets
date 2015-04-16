"""
interact.py : Get followers through retweeting and favs.
Some functions here are also simply helpers to check our twitter account.
"""

import tweepy
import positive
import random
import os
import argparse
from credentials import our_id


def choose_tweet(api, id, keywords):
    """
    Given some userid, choose which tweet should be acted upon. To do that,
    chose the tweet Twitter users liked the most.
    """
    tweets = api.user_timeline(user_id=id, count=15)
    topic_tweets = [t for t in tweets if positive.check_on_topic(t.text, keywords)]
    if topic_tweets:
        most_popular = max(t.retweet_count + t.favorite_count for t in topic_tweets)
        for t in tweets:
            if t.retweet_count + t.favorite_count == most_popular:
                return t.id
    return


def get_prospect_list(api=None, refresh=False):
    """
    Builds a list of prospects from Twitter if refresh, else uses the cached
    one. Twitter's doc states that we will receive last followed people first,
    but that this behaviour is subject to change.
    """
    if refresh:
        os.remove('prospects')
        friends = api.friends_ids(user_id=our_id)
        with open('prospects', 'w') as prospects:
            prospects.write("\n".join(str(f) for f in friends))
    with open('prospects', 'r') as prospects:
        return [int(i) for i in prospects.read().split('\n')]

def random_action(api):
    """
    Returns a randomly selected function between retweeting and adding to fav.
    """
    return random.choice((api.create_favorite, api.retweet))

if __name__ == '__main__':
    keywords = ['big data', 'machine learning', 'deep learning', 'hadoop',
                'data mining', 'open data', 'mapreduce', 'nosql', 'analytics',
                'mongodb', 'cassandra', 'analytics']
    parser = argparse.ArgumentParser(description="Interact with prospects.")
    parser.add_argument('-k', '--keywords', dest='keywords',
                        help='Keywords that we should scan twitter for.')
    parser.add_argument('-a', '--action_number', default=20, dest='number',
                        help='How many actions we should do before stopping')
    args = parser.parse_args()
    if args.keywords:
        keywords = args.keywords.split(', ')
    number = int(args.number)

    api = tweepy.API(positive.setup_auth())
    prospect_list = get_prospect_list(api, refresh=True)
    i = 0
    while i < number:
        tweet_id = choose_tweet(api, random.choice(prospect_list), keywords)
        # Sometimes no_retweet is specified.
        try:
            if tweet_id:
                action = random_action(api)
                action(tweet_id)
                i += 1
                print("Action %s taken" % i)
        except tweepy.error.TweepError:
            print('Tweet number %s is not retweetable' % tweet_id)
            continue
        except:
            print('Another error, probably hit the limit.')
            break
