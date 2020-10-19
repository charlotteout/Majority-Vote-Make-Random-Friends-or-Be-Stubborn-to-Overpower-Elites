import networkx as nx
import matplotlib.pyplot as plt
import random
import pandas as pd
import numpy as np
from graph_initialization import GraphInit
import networkit as nk
import math


def elite_experiment(our_graph, elite_percentage, honest, influence_factor, counter_measure):
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
    elite_size = int(elite_percentage * num_nodes)

    # we define the elite set of nodes to be the highest degree nodes
    degrees = [val for (node, val) in sorted(our_graph.degree(), key=lambda pair: pair[0])]
    threshold = sorted(degrees, reverse=True)[:elite_size][-1]

    for (node, degrees) in our_graph.degree():
        if degrees > threshold - 1:
            our_graph.nodes[node]['vote'] = 1
            our_graph.nodes[node]['influence'] = influence_factor
            our_graph.nodes[node]['elite'] = 1
        if degrees < threshold:
            our_graph.nodes[node]['vote'] = 0
            our_graph.nodes[node]['influence'] = 1
            our_graph.nodes[node]['elite'] = 0

    if counter_measure:
        total = sum(j for i, j in list(our_graph.degree(our_graph.nodes)))
        av_deg = total / num_nodes
        print("av_deg", av_deg)

        G_dreg = nx.random_regular_graph(d=int(3*av_deg), n=num_nodes)
        our_graph = nx.compose(our_graph, G_dreg)


    if honest:

        change = 2
        round = 1
        bluelist = [num_nodes - elite_size]
        print("initial blue list", num_nodes - elite_size)
        redlist = [elite_size]
        print("initial red list", elite_size)
        while change != 0:
            change_prev = change
            change = 0
            num_blue = 0
            num_red = 0
            for i in our_graph.nodes:
                total_vote = 0
                for j in our_graph.adj[i]:
                    total_vote = our_graph.nodes[j]['vote'] * our_graph.nodes[j]['influence'] + total_vote

                if total_vote == 0:
                    ratio = 0
                else:
                    denominator = 0
                    for j in our_graph.adj[i]:
                        denominator = denominator + our_graph.nodes[j]['influence']


                    ratio = total_vote / denominator
                    # ASK: is this the right denominator

                if ratio < 0.5:
                    if our_graph.nodes[i]['vote'] != 0:
                        change = 1 + change
                    our_graph.nodes[i]['pseudo_vote'] = 0
                else:
                    if our_graph.nodes[i]['vote'] != 1:
                        change = 1 + change
                    our_graph.nodes[i]['pseudo_vote'] = 1
            print("number of changed opinions", change)
            for i in our_graph.nodes:
                if our_graph.nodes[i]['pseudo_vote'] == 0:
                    our_graph.nodes[i]['vote'] = 0
                    num_blue = num_blue + 1
                if our_graph.nodes[i]['pseudo_vote'] == 1:
                    our_graph.nodes[i]['vote'] = 1
                    num_red = num_red + 1
            print(num_blue, num_red)
            bluelist.append(num_blue)
            redlist.append(num_red)
            round = round + 1
            # plot the network
            if change_prev == change:
                if bluelist[-1] == bluelist[-3] and redlist[-1] == redlist[-3]:
                    print("blink 1",bluelist[-2], redlist[-2])
                    print("blink 2", bluelist[-1], redlist[-1])
                    x = np.arange(0, round)
                    plt.plot(x, redlist, 'r')
                    plt.plot(x, bluelist, 'b')
                    plt.title('citation dishonest')
                    plt.show()
                    return (num_blue, num_red)

            if change == 0:
                print(num_blue,num_red)
                x = np.arange(0,round)
                plt.plot(x, redlist, 'r')
                plt.plot(x, bluelist, 'b')
                plt.title('citation dishonest')
                plt.show()
                return (num_blue, num_red)

    if not honest:

        change = 2
        round = 1
        bluelist = [num_nodes - elite_size]
        print("initial blue list", num_nodes - elite_size)
        redlist = [elite_size]
        print("initial red list", elite_size)
        while change != 0:
            change_prev = change
            change = 0
            num_blue = 0
            num_red = 0
            for i in our_graph.nodes:
                total_vote = 0
                for j in our_graph.adj[i]:
                    total_vote = our_graph.nodes[j]['vote'] * our_graph.nodes[j]['influence'] + total_vote

                if total_vote == 0:
                    ratio = 0
                else:
                    denominator = 0
                    for j in our_graph.adj[i]:
                        denominator = denominator + our_graph.nodes[j]['influence']


                    ratio = total_vote / denominator
                    # ASK: is this the right denominator

                if our_graph.nodes[i]['elite'] == 0:
                    if ratio < 0.5 :
                        if our_graph.nodes[i]['vote'] != 0:
                            change = 1 + change
                        num_blue = num_blue + 1
                        our_graph.nodes[i]['pseudo_vote'] = 0
                    if ratio >= 0.5:
                        if our_graph.nodes[i]['vote'] != 1:
                            change = 1 + change
                        our_graph.nodes[i]['pseudo_vote'] = 1
                        num_red = num_red + 1


                if our_graph.nodes[i]['elite'] == 1:
                    our_graph.nodes[i]['vote'] = 1
                    num_red = num_red + 1

            print("number of changed opinions", change)
            print(num_blue, num_red)
            bluelist.append(num_blue)
            redlist.append(num_red)
            round = round + 1
            for i in our_graph.nodes:
                if our_graph.nodes[i]['elite'] == 0:
                    if our_graph.nodes[i]['pseudo_vote'] == 0:
                        our_graph.nodes[i]['vote'] = 0
                    if our_graph.nodes[i]['pseudo_vote'] == 1:
                        our_graph.nodes[i]['vote'] = 1
                else:
                    continue
            if change_prev == change:
                if bluelist[-1] == bluelist[-3] and redlist[-1] == redlist[-3]:
                    print("blink 1",bluelist[-2], redlist[-2])
                    print("blink 2", bluelist[-1], redlist[-1])
                    x = np.arange(0, round)
                    plt.plot(x, redlist, 'r')
                    plt.plot(x, bluelist, 'b')
                    plt.title('citation dishonest')
                    plt.show()
                    return (num_blue, num_red)
            if change == 0:
                print(num_blue, num_red)
                x = np.arange(0, round)
                plt.plot(x, redlist, 'r')
                plt.plot(x, bluelist, 'b')
                plt.title("citation dishonest")
                plt.show()
                return (num_blue, num_red)


def graph_initialization(our_graph, elite_percentage):
    """

    :param arbitrary_mode: boolean: indicating whether an arbitrary subset
    of nodes is taken as the elite set
    :return: nx.graph object G_tot
    """
    elite_nodes = [i for i in range(0, int(elite_percentage*n))]
    non_elite_nodes = [i for i in range(int(elite_percentage*n), n)]
    non_elite_size = n - elite_percentage*n
    nodes = [i for i in range(n)]
    G = nx.complete_graph(elite_percentage*n)
    G.add_nodes_from(non_elite_nodes)

    for v in elite_nodes:
        G.nodes[v]['vote'] = 1
        num_neighs_v= random.randint(0,non_elite_size)
        sampled_list = random.sample(non_elite_nodes,num_neighs_v)
        for i in sampled_list:
            G.add_edge(v,i)

    total = sum(j for i,j in list(G.degree(nodes)))
    av_deg = total/len(nodes)
    if av_deg > math.log(n):
        G_er = nx.gnp_random_graph(n, (20*av_deg)/(n-1))
        G_tot = nx.compose(G, G_er)
        return G_tot
    if av_deg <= math.log(n):
        G_dreg = nx.random_regular_graph(d=20*av_deg, n=n)
        G_tot = nx.compose(G, G_dreg)
        return G_tot

def graph_initialization_1(our_graph, elite_percentage):
    num_nodes = len(our_graph.nodes)
    total = sum(j for i, j in list(our_graph.degree(our_graph.nodes)))
    av_deg = total / num_nodes

    G_dreg = nx.random_regular_graph(d=20*av_deg, n=num_nodes)
    G_tot = nx.compose(G,G_dreg)
    return G_tot




def counter_measure(n, elite_percentage):

    our_graph = graph_initialization(n, elite_percentage)

    # update step
    change = 2
    while change != 0:
        change = 0
        num_blue = 0
        num_red = 0
        for i in range(len(our_graph.nodes)):
            total_vote = 0
            for j in our_graph.adj[i]:
                total_vote = our_graph.nodes[j]['vote'] + total_vote
                if total_vote == 0:
                    ratio = 0
                else:
                    ratio = total_vote / len(our_graph.adj[i])
            if ratio < 0.5:
                if our_graph.nodes[i]['vote'] != 0 and our_graph.nodes[i]['elite'] == 0:
                    change = 1 + change
                our_graph.nodes[i]['vote'] = 0
            else:
                if our_graph.nodes[i]['vote'] != 1 and our_graph.nodes[i]['elite'] == 0:
                    change = 1 + change
                our_graph.nodes[i]['vote'] = 1

            if our_graph.nodes[i]['elite'] == 1:
                our_graph.nodes[i]['vote'] = 1
        print("number of changed opinions", change)

        if change == 0:
            return





#hg = nk.generators.HyperbolicGenerator(1000000,16,7)
#hgG = hg.generate()
#print(hgG.numberOfNodes(), hgG.numberOfEdges())
#nxG = nk.nxadapter.nk2nx(hgG)
#G_yt = nx.read_edgelist("networks/com-youtube.ungraph.txt",create_using= nx.Graph(), nodetype=int)
#G_slashdot = nx.read_edgelist('networks/soc-Slashdot0902.txt', create_using=nx.Graph(), nodetype=int)
#G_twitter = nx.read_edgelist('networks/twitter_combined.txt', create_using=nx.Graph(), nodetype=int)
#G_fb = nx.read_edgelist('networks/facebook-links2.txt', create_using=nx.Graph(), nodetype=int)
#G_orkut = nx.read_edgelist('networks/com-orkut.ungraph.txt', create_using=nx.Graph(), nodetype=int)
#percentage = pow(len(G_orkut.edges), 0.5)/len(G_orkut.nodes)
#G_yt2 = nx.read_edgelist('networks/youtube-links2.txt', create_using=nx.Graph(), nodetype=int)
#G_flickr = nx.read_edgelist('networks/flickr-links2.txt', create_using=nx.Graph(), nodetype=int)
#G_gowalla = nx.read_edgelist('networks/loc-gowalla_edges.txt', create_using=nx.Graph(), nodetype=int)
#G_BK = nx.read_edgelist('networks/loc-brightkite_edges.txt', create_using=nx.Graph(), nodetype=int)
G_citation = nx.read_edgelist('networks/cit-HepPh.txt', create_using=nx.Graph(), nodetype=int)

elite_experiment(our_graph=G_citation, elite_percentage=0.0188, influence_factor=1.67, honest=False, counter_measure=False)


