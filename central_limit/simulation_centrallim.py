import itertools
import random
import math
import networkx as nx

def sim_centrallim(n, def_ratio=0.5, p=0.5):

    our_graph = nx.Graph()
    our_graph.add_nodes_from(range(n))
    num_nodes = our_graph.number_of_nodes()
    initial_number_red = 0
    initial_number_blue = 0


    for node in our_graph.nodes:
        if node <= num_nodes / 2:
            our_graph.nodes[node]['vote'] = 1
            initial_number_red = initial_number_red + 1
        else:
            our_graph.nodes[node]['vote'] = 0
            initial_number_blue = initial_number_blue + 1
    edges = itertools.combinations(range(n), 2)
    for e in edges:
        if random.random() < p:
            our_graph.add_edge(*e)

    print("initial_number_red:", initial_number_red)
    print("initial_number_blue:", initial_number_blue)

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

        print("round:", round)
        print("cur_num_red:", cur_num_red)
        print("cur_num_blue:", cur_num_blue)
        round = round + 1
        if change_prev == change:
            if cur_num_blue == prevprev_num_blue and cur_num_red == prevprev_num_red:
                print("blink 1", prev_num_blue, prev_num_red)
                print("blink 2", cur_num_blue, cur_num_red)
                redsum = prev_num_red + cur_num_red
                bluesum = prev_num_blue + cur_num_blue
                if (bluesum >= redsum):
                    print("the end, blue won")
                    print("----------------------")
                    return "blue"
                else:
                    print("the end, red won")
                    print("----------------------")
                    return "red"

        if change == 0:
            print(cur_num_blue, cur_num_red)
            if (cur_num_blue >= cur_num_red):
                print("the end, blue won")
                print("----------------------")
                return "blue"
            else:
                print("the end, red won")
                print("----------------------")
                return "red"


