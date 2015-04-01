""" The goal of this tool is to generate a list of prospects.
This tool finds tweets about our topic then ensures using twitter.py that
the person who wrote it is a prospect.
Inspiration : http://adilmoujahid.com/posts/2014/07/twitter-analytics/ """

import sys
import json
import argparse

import tweepy

import twitter


class Listener(tweepy.StreamListener):
    """
    This is a listener modified to stop after registering a certain number
    of tweets.
    """
    i = 0

    def __init__(self, number):
        """
        Number is a limit to the number of tweets we listen to.
        """
        self.number = number

    def on_data(self, data):
        """
        While we did not process number tweets, recover tweets about our topic
        and adds those tweets' writers who are prospects."""
        if self.i < self.number:
            tweet = json.loads(str(data))
            self.i += 1
            author_id = tweet['user']['id']
            if twitter.check_pos(tweet['text']):
                print('Went trough first stage')
                if twitter.is_prospect(author_id, keywords):
                    # Only do this once we have a test account
                    # twitter.follow(author_id)
                    twitter.follow(author_id)
                    print('We should follow this dude : %s' % author_id)
        else:
            # FIXME : Ugly.
            print("Recovered and processed %s tweets" % self.i)
            sys.exit(0)

    def on_error(self, status):
        "We do want to write errors to StdOut as it easier to see them."
        print(status)


def scan_tweets(keywords, number=1000, output_file='tweets'):
    """"
    This recovers number tweets which contains one of keywords.
    """
    l = Listener(number)
    stream = tweepy.Stream(auth=twitter.setup_auth(), listener=l)
    stream.filter(track=keywords)

# Just a generic call to get_tweets for testing purposes
if __name__ == '__main__':
    keywords = ['big data', 'machine learning', 'deep learning', 'hadoop',
            'data mining', 'open data', 'mapreduce', 'nosql']
    parser = argparse.ArgumentParser(description="This is a twitter-based prospect finder tool")
    parser.add_argument('-k', '--keywords', dest='keywords',
            help='Keywords that we should scan twitter for.')
    parser.add_argument('-t', '--tweet-number', default=20, dest='number',
            help='How many tweets we should scan before stopping')
    args = parser.parse_args()
    if args.keywords:
        keywords = args.keywords.split(', ')
    number = int(args.number)
    scan_tweets(keywords, number)
