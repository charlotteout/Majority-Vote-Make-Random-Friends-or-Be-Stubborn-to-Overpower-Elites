import networkx as nx
import matplotlib.pyplot as plt
import random
import pandas as pd
import numpy as np
import networkit as nk
import math




def simulation_dens_TT(our_graph,initial_prob_dens, stubrat_blue, stubrat_red):
    """
    A function simulating the majority model as described in

    :param our_graph: a networkx object representing our graph
    :param initial_prob_dens: float between 0 and 1 representing the probability with which nodes
    in the first round are colored red
    :param stubrat_blue: float between 1/2 and 1 representing the stubbornness factor for blue nodes
    :param stubrat_red: float between 1/2 and 1 representing the stubbornness factor for red nodes
    :return the faction of red nodes in the final configuration
    """
    #initialize the nodes
    for node in our_graph.nodes:
        if (random.random() < (1-initial_prob_dens)):
            our_graph.nodes[node]['vote'] = 0
        else:
            our_graph.nodes[node]['vote'] = 1


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
        num_reds_to_blue = 0
        num_reds_to_red = 0
        for i in our_graph.nodes:
            personal_vote = our_graph.nodes[i]['vote']
            total_vote = 0

            #make sure that isolate nodes do not get updated
            if our_graph.adj[i] == {}:
                our_graph.nodes[i]['pseudo_vote'] = our_graph.nodes[i]['vote']
            else:
                for j in our_graph.adj[i]:
                    total_vote = our_graph.nodes[j]['vote'] + total_vote

                if total_vote == 0:
                    cur_rat = 0
                else:
                    denominator = 0
                    for j in our_graph.adj[i]:
                        denominator = denominator + 1

                    cur_rat = total_vote / denominator


                if personal_vote == 0:
                    if cur_rat > stubrat_blue:
                        our_graph.nodes[i]['pseudo_vote'] = 1
                        change = change + 1
                    else:
                        our_graph.nodes[i]['pseudo_vote'] = 0
                if personal_vote == 1:
                    if (cur_rat < (1-stubrat_red)):
                        our_graph.nodes[i]['pseudo_vote'] = 0
                        change = change + 1
                        num_reds_to_blue = num_reds_to_blue + 1
                    else:
                        num_reds_to_red = num_reds_to_red + 1
                        our_graph.nodes[i]['pseudo_vote'] = 1


        # create the pseudovotes into actual votes.
        for i in our_graph.nodes:
            if our_graph.nodes[i]['pseudo_vote'] == 0:
                our_graph.nodes[i]['vote'] = 0
                cur_num_blue = cur_num_blue + 1
            if our_graph.nodes[i]['pseudo_vote'] == 1:
                our_graph.nodes[i]['vote'] = 1
                cur_num_red = cur_num_red + 1

        round = round + 1
        if change_prev == change:
            if cur_num_blue == prevprev_num_blue and cur_num_red == prevprev_num_red:
                redsum = prev_num_red + cur_num_red
                bluesum = prev_num_blue + cur_num_blue
                return (redsum / (redsum + bluesum))

        if change == 0:
            return (cur_num_red / (cur_num_red + cur_num_blue))