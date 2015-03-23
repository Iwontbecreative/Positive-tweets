""" The goal of this tool is to gather tweets for analysis. This will send
it to a file using StreamingApi, as we are yet conducting real-time analysis.
Inspiration : http://adilmoujahid.com/posts/2014/07/twitter-analytics/ """

import tweepy
import credentials as c

# This is the list of words we want to follow. As we are focusing on big data
# those are related to that field.
# TODO Find a way to automatically generate it.
keywords = ['big data', 'machine learning', 'deep learning', 'hadoop',
            'data mining', 'open data', 'MapReduce', 'NoSQL']

# We want to use Streaming Api to send to a file. Instead of printing
# directly to StdOut and then redirecting thanks to > to a text file, we want
# to write it to a text file directly from python so there are no issues with
# Windows users.

class Listener(tweepy.StreamListener):

    def on_data(self, data):
        with open('test', 'a') as tweets:
            tweets.write(data)

    def on_error(self, status):
        "We do want to write errors to StdOut as it easier to see them."
        print status

#FIXME : Implement number limit. 
def get_tweets(number, keywords):
    """"
    This recovers number tweets which contains one of keywords.
    """
    l = Listener()
    auth = tweepy.OAuthHandler(c.consumer_key, c.consumer_secret)
    auth.set_access_token(c.access_token, c.access_token_secret)
    stream = tweepy.Stream(auth=auth, listener=l)
    stream.filter(track=keywords)

# Just a generic call to get_tweets for testing purposes
if __name__ == '__main__':
    get_tweets(2, keywords)
