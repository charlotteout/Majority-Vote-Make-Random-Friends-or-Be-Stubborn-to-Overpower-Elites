import networkx as nx
import matplotlib.pyplot as plt
import random
import pandas as pd
import numpy as np
import networkit as nk
import math



def elite_experiment_peleg(our_graph, elite_percentage, honest, influence_factor, counter_measure):
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

    if counter_measure:
        total = sum(j for i, j in list(our_graph.degree(our_graph.nodes)))
        av_deg = total / num_nodes
        print("av_deg", av_deg)

        d = int(20*av_deg)
        if ((d*num_nodes)%2 != 0):
            d = d + 1
        else:
            d = d

        G_dreg = nx.random_regular_graph(d=d, n=num_nodes)
        print("generated the d-regular graph")
        our_graph = nx.compose(our_graph, G_dreg)
        print('finished composing our graph')
        ###################end countermeasure

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
                    plt.title('twitter honest countermeasure')
                    plt.show()
                    return (num_blue, num_red)

            if change == 0:
                print(num_blue,num_red)
                x = np.arange(0,round)
                plt.plot(x, redlist, 'r')
                plt.plot(x, bluelist, 'b')
                plt.title('twitter honest countermeasure')
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
                    plt.title('twitter honest countermeasure')
                    plt.show()
                    return (num_blue, num_red)
            if change == 0:
                print(num_blue, num_red)
                x = np.arange(0, round)
                plt.plot(x, redlist, 'r')
                plt.plot(x, bluelist, 'b')
                plt.title("twitter honest countermeasure")
                plt.show()
                return (num_blue, num_red)




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
#G_citation = nx.read_edgelist('networks/cit-HepPh.txt', create_using=nx.Graph(), nodetype=int)
#G_LFR_yt = LFR_benchmark_graph(n=1138499, tau1=2.5, tau2=1.5, mu=0.1,average_degree=5.25)



#elite_experiment(our_graph=G_LFR_yt, elite_percentage=0.0015, influence_factor=6.79, honest=True, counter_measure=False)
