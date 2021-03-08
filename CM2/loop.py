from CM2.bigsimulation import bigsimulation
import networkx as nx
import networkit as nk
import os
abs_path = os.path.abspath(os.path.dirname(__file__))
from Winning_Set import slashdot_loc, twitter_loc, fb_loc, yt_loc


def looptypegraph(graph_locs, mult):
    "A function that enables us to loop over multiple social networks at once"
    graph_dict = {}
    for graph_loc in graph_locs:
        elite_size_list = bigsimulation(graph_loc=graph_loc, mult=mult)
        graph_dict[graph_loc] = elite_size_list
    print(graph_dict)
    return(graph_dict)


