import random
import networkx
import networkit

def simulation_stab(our_graph, initial_prob_dens, def_ratio):
    """
    :param our_graph: a networkx object representing our graph
    :param initial_prob_dens: float between 0 and 1 denoting the initial probability probability
    that a node is colored red (corresponding to black in the paper)
    :param def_ratio: stubbornness of the nodes. Set to 0.5 here by default
    :return: Integer, denoting how many rounds the process takes
    """

    #initialize the nodes
    for node in our_graph.nodes:
        if (random.random() < initial_prob_dens):
            our_graph.nodes[node]['vote'] = 1
        else:
            our_graph.nodes[node]['vote'] = 0

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
            # make sure that isolate nodes do not update
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
        #period is 2
        if change_prev == change:
            if cur_num_blue == prevprev_num_blue and cur_num_red == prevprev_num_red:
                return round
        #period is 1
        if change == 0:
            return(round)

