"""
Draws a graph of the network of our Twitter account. Shows:
-> Persons we follow and whether they follow us back
-> How many tweets and favorites we made
-> Relationships between the persons we follow
-> Their importance
"""

import networkx as nx
import matplotlib.pyplot as plt
import tweepy
import positive
import datetime
from credentials import our_id


class prospect_map(nx.DiGraph):
    """
    A graph of prospects. Even if we retweet stuff from other people or that
    people we did not add added us, we do not wish to represent those.
    """
    def __init__(self, api, workaround):
        nx.DiGraph.__init__(self)
        self.followed = set(api.friends_ids())
        # Fixme : Find a workaround for when we have more than 200 of either
        # Favorites come in batches of 200 and so do retweets. To get all of
        # them, here is a dirty hack : we say how many times 200 we have of
        # of each...
        # FIXME : ^
        fav = api.favorites(count=200)
        ret = api.home_timeline(count=200)
        for i in range(workaround-1):
            oldest_fav = min(f.id for f in fav)
            oldest_ret = min(r.id for r in ret)
            fav += api.favorites(count=200, max_id=oldest_fav)
            ret += api.home_timeline(count=200, max_id=oldest_ret)

        self.favorited = set(i.user.id for i in fav) & self.followed
        self.retweeted = set(i.user.id for i in ret) & self.followed
        self.followers = set(api.followers_ids()) & self.followed

    def construct_nodes(self):
        """
        Nodes will be different depending on the interactions
        -> Users we just followed -> f
        -> Users we interacted with and did not follow us -> fi
        -> Users we did not interact with and that followed us -> ff
        -> Users we interacted with and that followed us. -> ffi
        """
        # We also add our id because it will be needed for edges.
        prospect_map.add_nodes_from(self, self.followed)
        f = self.followed - (self.favorited | self.retweeted | self.followers)
        fi = (self.favorited | self.retweeted) - self.followers
        ff = self.followers - (self.favorited & self.retweeted)
        ffi = self.followers & (self.favorited | self.retweeted)
        print(len(f), len(fi), len(ff), len(ffi))

        self.pos = nx.circular_layout(self)
        # We center ourself, it's prettier.
        self.pos[our_id] = (0.5, 0.5)
        nx.draw_networkx_nodes(self, self.pos, nodelist=[our_id], 
                               node_size=250, node_color='#0000ff')

        nx.draw_networkx_nodes(self, self.pos, nodelist=f, labels=False,
                               node_size=1, node_color='#000000')
        nx.draw_networkx_nodes(self, self.pos, nodelist=fi, labels=False,
                               node_size=20, node_color='#ccff00')
        nx.draw_networkx_nodes(self, self.pos, nodelist=ff, labels=False,
                               node_size=50, node_color='#ff6600')
        nx.draw_networkx_nodes(self, self.pos, nodelist=ffi, labels=False,
                               node_size=100, node_color='#990000')

    def construct_edges(self):
        """
        Add links from us to people we interacted with.
        Add links from people to us when they followed us.
        """
        prospect_map.add_edges_from(self,
                                    set((i, our_id) for i in self.followers))
        prospect_map.add_edges_from(self,
                                    set((our_id, i) for i in self.retweeted | self.favorited))
        nx.draw_networkx_edges(self, self.pos)

    def stats(self):
        """
        Give basic info about ourself.
        """
        return {'fol': len(self.followed),
                'fav': len(self.favorited),
                'ret': len(self.retweeted),
                'fri': len(self.followers),
                'folfri': len(self.followed & self.followers)}


if __name__ == '__main__':
    api = tweepy.API(positive.setup_auth())
    pm = prospect_map(api, workaround=2)
    pm.construct_nodes()
    pm.construct_edges()
    print(""" We follow {fol} accounts, have {fri} followers,
          made {ret} retweets and added {fav} tweets to favorites. However,
          only {folfri} of those friends we befriended first.
          """.format(**pm.stats()))
    plt.get_current_fig_manager().resize(1600, 1000)

    now = datetime.datetime.now()
    plt.savefig('Snapshot at %s.png' % now)
