"""
The goal of this programme is to get a taste of machine learning through the
data we collected. We'll try to do both supervised and unsupervised learning.
"""

import numpy as np
import random
import tweepy
from positive import setup_auth
from pandas import DataFrame as df
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.cross_validation import train_test_split



lin_reg = 0 #True
forest_reg = False
supervised = True
unsupervised = False

api = tweepy.API(setup_auth())


def linear_regression(dataset):
    model = LinearRegression(normalize=True)
    X = dataset.retweet_count[:, np.newaxis]
    model.fit(X, dataset.favorite_count)
    max_value = max(max(dataset.favorite_count), max(dataset.retweet_count))

    # Plotting
    xx = np.linspace(0, max_value, 100)
    yy = xx
    yy = yy * model.coef_ + model.intercept_
    print(model.residues_, model.coef_, model.intercept_)
    plt.plot(xx, yy)
    plt.show()


def forest_regression(dataset):
    model = RandomForestRegressor()
    max_value = max(max(dataset.favorite_count), max(dataset.retweet_count))
    x_fit = np.linspace(0, max_value, 100)[:, np.newaxis]
    y_fit = model.predict(x_fit)
    print(model.residues)
    plt.plot(X.squeeze())
    plt.plot(x_fit.squeeze(), y_fit)
    plt.show()

if lin_reg or forest_reg:
    # We need to save someone who is popular and has a lot of tweets to have
    # meaningful results. Unfortunately, even with MongoDB (157k followers)
    # our regression does not work that well.
    friends = api.friends(count=200)
    maximum_friends = max(i.followers_count for i in friends)
    print(maximum_friends)
    for f in friends:
        if f.followers_count == maximum_friends:
            user = f.id
            print(f.name)
            break
    user = 813286  # Obama's id.

    user_tweets = [t.__dict__ for t in api.user_timeline(user_id=user, count=200)]

    ds = df(user_tweets)
    # Remove non-retweetable tweets as they obvisouly skew results.
    # Since we're analyzing someone popular, if a tweet is never retweeted it
    # must mean that it is not retweetable
    ds = ds[ds.retweet_count >= 1]

    # Keep only the columns we need for analysis.
    ds = ds[['id', 'text', 'created_at', 'lang', 'retweet_count',
             'favorite_count']]
    ds.text = ds.text.apply(lambda t: len(t))
    plt.scatter(ds.retweet_count, ds.favorite_count)
    if lin_reg:
        linear_regression(ds)
    if forest_reg:
        forest_regression(ds)

if supervised:
    friends = api.friends_ids()
    to_test = [random.choice(friends), random.choice(friends), random.choice(friends)]
    print(to_test)
    user_tweets = [api.user_timeline(user_id=id, count=200) for id in to_test]
    tweet_dicts = [[t.__dict__ for t in u] for u in user_tweets]
    tweets = [tweet for sublist in tweet_dicts for tweet in sublist]
    ds = df(tweets)

    ds = ds[['id', 'user', 'text', 'created_at', 'lang', 'retweet_count',
             'favorite_count', 'retweeted_status', 'entities']]

    # Improving data :
    ds.user = ds.user.apply(lambda i: i.id)
    ds.text = ds.text.apply(lambda t: len(t))  # No better option so far.

