import networkx as nx
import matplotlib.pyplot as plt
import random
import pandas as pd
import numpy as np
import networkit as nk
import math




def elite_experiment(our_graph,our_stubborn_size, stubbornness_ratio, def_ratio, centrality_measure):
    """
    A function simulating the majority model as described in

    :param elite_percentage: a float between 0 and 1
    :param honest: boolean indicating if we are in reversible mode
    or irreversible mode
    :param influence_factor: integer indicating the influence of a node
    :param counter_measure: boolean indicating if we add the d-regular graph on top
    :return:tuple consisting of the winning color and how many nodes have this color.
    """
    num_nodes = len(our_graph.nodes)
    stubborn_size = int(num_nodes * our_stubborn_size)

    #define which nodes are the stubborn nodes. Choose them at random
    node_list = list(our_graph.nodes)
    random.shuffle(node_list)
    stubborn_node_list = node_list[:stubborn_size]

    if centrality_measure == 0:
        for node in list(our_graph.nodes):
            our_graph.nodes[node]['vote'] = 0
            our_graph.nodes[node]['stubborn'] = False
            our_graph.nodes[node]['stubbornness_ratio'] = def_ratio

        for node in stubborn_node_list:
            our_graph.nodes[node]['vote'] = 1
            our_graph.nodes[node]['stubborn'] = True
            our_graph.nodes[node]['stubbornness_ratio'] = stubbornness_ratio

    if centrality_measure == 1:
        centrality = nx.eigenvector_centrality_numpy(our_graph)
        threshold = sorted(list(centrality.values()), reverse=True)[:stubborn_size][-1]

        for (node, EVC) in centrality.items():
            if EVC > threshold - 1:
                our_graph.nodes[node]['vote'] = 1
                our_graph.nodes[node]['stubborn'] = True
                our_graph.nodes[node]['stubbornness_ratio'] = stubbornness_ratio
            if EVC < threshold:
                our_graph.nodes[node]['vote'] = 0
                our_graph.nodes[node]['stubborn'] = False
                our_graph.nodes[node]['stubbornness_ratio'] = def_ratio



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
            #print("num neighs our graph", len(list(our_graph.adj[i])))
            #print("num neighs cm graph", len(list(cm_graph.adj[i])))
            total_vote = 0
            for j in our_graph.adj[i]:

                total_vote = our_graph.nodes[j]['vote'] + total_vote

            if total_vote == 0:
                cur_rat = 0
            else:
                denominator = 0
                for j in our_graph.adj[i]:
                    denominator = denominator + 1

                cur_rat = total_vote / denominator
                # ASK: is this the right denominator

            ratio = our_graph.nodes[i]['stubbornness_ratio']
            if personal_vote == 0:
                if cur_rat > ratio:
                    our_graph.nodes[i]['pseudo_vote'] = 1
                    change = change + 1
                else:
                    our_graph.nodes[i]['pseudo_vote'] = 0
            if personal_vote == 1:
                if cur_rat < (1 - ratio):
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
        # plot the network
        if change_prev == change:
            if cur_num_blue == prevprev_num_blue and cur_num_red == prevprev_num_red:
                print("blink 1", prev_num_blue, prev_num_red)
                print("blink 2", cur_num_blue, cur_num_red)
                redsum = prev_num_red + cur_num_red
                bluesum = prev_num_blue + cur_num_blue
                if (bluesum >= redsum):
                    print("the end, blue won")
                    return "blue"
                else:
                    print("the end, red won")
                    return "red"

        if change == 0:
            print(cur_num_blue, cur_num_red)
            if (cur_num_blue >= cur_num_red):
                print("the end, blue won")
                return "blue"
            else:
                print("the end, red won")
                return "red"

