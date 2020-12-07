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

    :param elite_percentage: a float between 0 and 1
    :param honest: boolean indicating if we are in reversible mode
    or irreversible mode
    :param influence_factor: integer indicating the influence of a node
    :param counter_measure: boolean indicating if we add the d-regular graph on top
    :return:tuple consisting of the winning color and how many nodes have this color.
    """
    num_nodes = len(our_graph.nodes)
    print("initial_prob_dens:", initial_prob_dens)

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
        print("num_reds_to_blue:", num_reds_to_blue)
        print("num_reds_to_red:", num_reds_to_red)
        print("#########################")
        print("cur_num_red:", cur_num_red)
        print("cur_num_blue:", cur_num_blue)
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$")
        # plot the network
        if change_prev == change:
            if cur_num_blue == prevprev_num_blue and cur_num_red == prevprev_num_red:
                # print("blink 1", prev_num_blue, prev_num_red)
                # print("blink 2", cur_num_blue, cur_num_red)
                redsum = prev_num_red + cur_num_red
                bluesum = prev_num_blue + cur_num_blue
                print("red density: ", redsum / (redsum + bluesum))
                print("------------------------------------------")
                return (redsum / (redsum + bluesum))

        if change == 0:
            # print(cur_num_blue, cur_num_red)
            print("red density:", cur_num_red /(cur_num_red + cur_num_blue))
            print("-------------------------------------------------")
            return (cur_num_red / (cur_num_red + cur_num_blue))