""" The goal of this tool is to gather tweets for analysis. This will send 
it to a file using StreamingApi, as we are yet conducting real-time analysis.
Inspiration : http://adilmoujahid.com/posts/2014/07/twitter-analytics/ """

#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

# Variables that contains the user credentials to access Twitter API
# This is private info, should not be used against me
access_token = "3013515967-8zWpVd26XIoYw7B0JttqiX01MkEmc3jarGFQsCX"
access_token_secret = "LZVguFlA60pGEwdLn97xgZkmWID5aYfnmw51FlajCwTYc"
consumer_key = "8R5XvwFGKmKm5Sdr73PUNVyMF"
consumer_secret = "RBbTqIJbfXzmM1eC7P9z3czR041rtu9N7ZrU3NAQAJCa5GhB5c"

# We want to use Streeaming Api to send to a file. Instead of printing
# directly to StdOut and then redirecting thanks to > to a text file, we want
# to write it to a text file directly from python so there are no issues with
# Windows users.
class Listener(StreamListener):
    def write_data(self, data):
	with open('tweets', 'a') as tweets:
            tweets.write(data)

    def write_error(self, status):
        "We do want to write errors to StdOut as it easier to see them."
        print status

