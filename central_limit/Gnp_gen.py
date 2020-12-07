import itertools
import random
import math
import networkx as nx
from networkx.generators.classic import empty_graph, path_graph, complete_graph


def our_gnp_fixed_assignment(n):
    """vote 0 correpsonds to blue and vote 1 corresponds to red"""
    our_graph = nx.Graph()
    our_graph.add_nodes_from(range(n))
    #print(our_graph.nodes)
    print("edges before adding:",our_graph.edges)

    num_nodes = our_graph.number_of_nodes()

    for node in our_graph.nodes:
        if node <= num_nodes / 2 :
            our_graph.nodes[node]['vote'] = 1
        else:
            our_graph.nodes[node]['vote'] = 0
    return our_graph




