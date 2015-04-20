"""
interact.py : Get followers through retweeting and favs.
Some functions here are also simply helpers to check our twitter account.
"""

import tweepy
import positive
from find_followees import keywords
import random
import os
import argparse
import re
import lxml.html
import bitly_api
from credentials import bitly_token

def get_prospect_list(api=None, refresh=False):
    """
    Builds a list of prospects from Twitter if refresh, else uses the cached
    one. Twitter's doc states that we will receive last followed people first,
    but that this behaviour is subject to change.
    """
    if refresh:
        os.remove('prospects')
        friends = api.friends_ids()
        with open('prospects', 'w') as prospects:
            prospects.write("\n".join(str(f) for f in friends))
    with open('prospects', 'r') as prospects:
        return [int(i) for i in prospects.read().split('\n')]

def choose_tweet(api, tweets, keywords):
    """
    Given some userid, choose which tweet should be acted upon. To do that,
    chose the tweet Twitter users liked the most.
    """
    topic_tweets = [t for t in tweets if positive.check_topic(t.text, keywords)]
    if topic_tweets:
        most_popular = max(t.retweet_count + t.favorite_count for t in topic_tweets)
        for t in tweets:
            if t.retweet_count + t.favorite_count == most_popular:
                return t.id
    return

def create_tweet(api, bitly, keywords):
    """
    There are no good reliable sources for data science news that work with
    newspaper. Therefore, we steal popular tweets and rewrite the title.
    """
    tweets = api.search("big data" + ' :)')
    links = re.compile(r"(http://[^ ]+)")
    for tweet in tweets:
        match = re.search(links, tweet.text)
        if match:
            url = bitly.shorten(match.group(0))['url']
            try:
                article = lxml.html.parse(url)
                title = article.find(".//title").text
                tweet = "%s %s" % (title[:100] + "... ", url)
                print(tweet, len(tweet))
                api.update_status(status=tweet)
                break
            except:
                print('Failed %s' % url)


def random_action(api):
    """
    Returns a randomly selected function between retweeting and adding to fav.
    """
    return random.choice((api.create_favorite, api.retweet))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Interact with prospects.")
    parser.add_argument('-k', '--keywords', dest='keywords',
                        help='Keywords that we should scan twitter for.')
    parser.add_argument('-a', '--action_number', default=20, dest='number',
                        help='How many actions we should do before stopping')
    parser.add_argument('-t', '--tweet', default=False, dest='create',
                        help='Create tweets or not')
    args = parser.parse_args()
    if args.keywords:
        keywords = args.keywords.split(', ')
    number = int(args.number)

    api = tweepy.API(positive.setup_auth())
    i = 0

    # Content creation mode
    if args.create:
        while i < number:
            # We initialize bitly api here to avoid calling it more than once
            bitly = bitly_api.Connection(access_token=bitly_token)
            create_tweet(api, bitly, keywords)
            i += 1
    # Retweeting/Favoriting mode
    else:
        prospect_list = get_prospect_list(api, refresh=True)
        while i < number:
            tweets = api.user_timeline(random.choice(prospect_list), count=15)
            chosen_tweet = choose_tweet(api, tweets, keywords)
            # Sometimes no_retweet is specified.
            try:
                if chosen_tweet:
                    action = random_action(api)
                    action(chosen_tweet)
                    i += 1
                    print("Action %s taken" % i)
            except tweepy.error.TweepError:
                print('Tweet number %s is not retweetable' % chosen_tweet)
                continue
