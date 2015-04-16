"""
The goal of this programme is to get a taste of machine learning through the
data we collected. We'll try to do both supervised and unsupervised learning.
"""

import tweepy
from positive import setup_auth
from pandas import DataFrame as df
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
import numpy as np

api = tweepy.API(setup_auth())

# We need to save someone who is popular and has a lot of tweets to have
# meaningful results.
friends = api.friends(count=200)
maximum_friends = max(i.followers_count for i in friends)
print(maximum_friends)
for f in friends:
    if f.followers_count == maximum_friends:
        user = f.id
        print(f.name)
        break

user_tweets = [t.__dict__ for t in api.user_timeline(user_id=user, count=200)]

ds = df(user_tweets)

# Keep only the rows we need for analysis.
ds = ds[['id', 'text', 'created_at', 'lang', 'retweet_count',
         'favorite_count']]
ds.text = ds.text.apply(lambda t: len(t))

plt.scatter(ds.retweet_count, ds.favorite_count)

# Implement a small linear regression
model = LinearRegression(normalize=True)
model = RandomForestRegressor()
X = ds.retweet_count[:, np.newaxis]
model.fit(X, ds.favorite_count)
max_value = max(max(ds.favorite_count), max(ds.retweet_count))

# Linear regression plotting
#xx = np.linspace(0, max_value, 100)
#yy = xx
#yy = yy * model.coef_ + model.intercept_
#print(model.residues_, model.coef_, model.intercept_)
#plt.plot(xx, yy)
#plt.show()

# RandomForest plotting
x_fit = np.linspace(0, max_value, 100)[:, np.newaxis]
y_fit = model.predict(x_fit)
plt.plot(X.squeeze())
plt.plot(x_fit.squeeze(), y_fit)
plt.show()
