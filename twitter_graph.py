"""
Draws a graph of the network of our Twitter account. Shows:
-> Persons we follow and whether they follow us back
-> How many tweets and favorites we made
-> Relationships between the persons we follow
-> Their importance
"""

import networkx as nx
import matplotlib.pyplot as plt
import interact
import tweepy
import positive


def construct_nodes():
    """
    We do not want to waste calls to REST api, so we used the cached list.
    """
    return set(interact.get_prospect_list(None, False))


def construct_edges():
    """
    Get the list of people who follow us.
    """
    api = tweepy.API(positive.setup_auth())
    return ([(i, 3130995473) for i in api.followers_ids(user_id=3130995473)])


prospect_map = nx.DiGraph()
prospect_map.add_nodes_from(construct_nodes())
prospect_map.add_edges_from(construct_edges())
nx.draw(prospect_map)
plt.show()
