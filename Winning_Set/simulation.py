import networkx as nx
import matplotlib.pyplot as plt
import random
import pandas as pd
import numpy as np
import networkit as nk
import math




def elite_experiment(our_graph,our_elite_size, influence_factor,
                     def_ratio):
    """
    A function simulating the majority model as described in

    :param our_graph: a networkx object representing the graph on which we perform the
    majority model
    :param our_elite_size: a float such that n^our_elite_size is the number of elite nodes in the graph
    :param influence_factor: integer indicating the influence factor assigned to the elite nodes
    :return: A string "blue", "red" corresponding to the color that won.
    """
    num_nodes = len(our_graph.nodes)
    elite_size = int(pow(num_nodes, our_elite_size))

    # we define the elite set of nodes to be the highest degree nodes
    degrees = [val for (node, val) in sorted(our_graph.degree(), key=lambda pair: pair[0])]
    threshold = sorted(degrees, reverse=True)[:elite_size][-1]

    #initialize the nodes
    for (node, degrees) in our_graph.degree():
        if degrees > threshold:
            our_graph.nodes[node]['vote'] = 1
            our_graph.nodes[node]['influence'] = influence_factor
            our_graph.nodes[node]['elite'] = 1
        if degrees < threshold + 1:
            our_graph.nodes[node]['vote'] = 0
            our_graph.nodes[node]['influence'] = 1
            our_graph.nodes[node]['elite'] = 0

    change = 2
    round = 1
    cur_num_blue = 0
    cur_num_red = 0
    prev_num_blue = 0
    prev_num_red = 0
    while change != 0:
        change_prev = change
        change = 0
        prevprev_num_blue = prev_num_blue
        prevprev_num_red = prev_num_red
        prev_num_blue = cur_num_blue
        prev_num_red = cur_num_red
        cur_num_blue = 0
        cur_num_red = 0
        for i in our_graph.nodes:
            personal_vote = our_graph.nodes[i]['vote']
            total_vote = 0
            #make sure that isolate nodes do not update
            if our_graph.adj[i] == {}:
                our_graph.nodes[i]['pseudo_vote'] = our_graph.nodes[i]['vote']
            else:
                for j in our_graph.adj[i]:
                    total_vote = our_graph.nodes[j]['vote'] * our_graph.nodes[j]['influence'] + total_vote
                if total_vote == 0:
                    cur_rat = 0
                else:
                    denominator = 0
                    for j in our_graph.adj[i]:
                        denominator = denominator + our_graph.nodes[j]['influence']
                    cur_rat = total_vote / denominator
                #update pseudovotes to make sure that updates do not interfere
                if personal_vote == 0:
                    if cur_rat > def_ratio:
                        our_graph.nodes[i]['pseudo_vote'] = 1
                        change = change + 1
                    else:
                        our_graph.nodes[i]['pseudo_vote'] = 0
                if personal_vote == 1:
                    if cur_rat < (1 - def_ratio):
                        our_graph.nodes[i]['pseudo_vote'] = 0
                        change = change + 1
                    else:
                        our_graph.nodes[i]['pseudo_vote'] = 1

        #create the pseudovodes into actual votes.
        for i in our_graph.nodes:
            if our_graph.nodes[i]['pseudo_vote'] == 0:
                our_graph.nodes[i]['vote'] = 0
                cur_num_blue = cur_num_blue + 1
            if our_graph.nodes[i]['pseudo_vote'] == 1:
                our_graph.nodes[i]['vote'] = 1
                cur_num_red = cur_num_red + 1

        round = round + 1
        #period of the cycle is 2
        if change_prev == change:
            if cur_num_blue == prevprev_num_blue and cur_num_red == prevprev_num_red:
                redsum = prev_num_red + cur_num_red
                bluesum = prev_num_blue + cur_num_blue
                #take the average of the two stable configurations
                if (bluesum >= redsum):
                    return "blue"
                else:
                    return "red"
        #period of the cycle is 1
        if change == 0:
            if (cur_num_blue >= cur_num_red):
                return "blue"
            else:
                return "red"










