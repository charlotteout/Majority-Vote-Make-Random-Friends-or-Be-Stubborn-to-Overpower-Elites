import networkx as nx
import matplotlib.pyplot as plt
import random
import pandas as pd
import numpy as np
import networkit as nk
import math


def elite_experiment(our_graph, our_elite_size, honest, influence_factor, counter_measure, centrality_measure):
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
    elite_size = int(pow(num_nodes, our_elite_size))


    if centrality_measure == 1:
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

    if centrality_measure == 2:
        centrality = nx.eigenvector_centrality_numpy(our_graph)
        threshold = sorted(list(centrality.values()),reverse=True)[:elite_size][-1]

        for (node, EVC) in centrality.items():
            if EVC > threshold - 1:
                our_graph.nodes[node]['vote'] = 1
                our_graph.nodes[node]['influence'] = influence_factor
                our_graph.nodes[node]['elite'] = 1
            if EVC < threshold:
                our_graph.nodes[node]['vote'] = 0
                our_graph.nodes[node]['influence'] = 1
                our_graph.nodes[node]['elite'] = 0


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
        our_graph = nx.compose(our_graph, G_dreg)

    if honest:
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

    if not honest:

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

                if our_graph.nodes[i]['elite'] == 0:
                    if ratio < 0.5:
                        if our_graph.nodes[i]['vote'] != 0:
                            change = 1 + change
                        cur_num_blue = cur_num_blue + 1
                        our_graph.nodes[i]['pseudo_vote'] = 0
                    if ratio >= 0.5:
                        if our_graph.nodes[i]['vote'] != 1:
                            change = 1 + change
                        our_graph.nodes[i]['pseudo_vote'] = 1
                        cur_num_red = cur_num_red + 1

                if our_graph.nodes[i]['elite'] == 1:
                    our_graph.nodes[i]['vote'] = 1
                    cur_num_red = cur_num_red + 1

            round = round + 1
            #create the pseudovotes into actual votes.
            for i in our_graph.nodes:
                if our_graph.nodes[i]['elite'] == 0:
                    if our_graph.nodes[i]['pseudo_vote'] == 0:
                        our_graph.nodes[i]['vote'] = 0
                    if our_graph.nodes[i]['pseudo_vote'] == 1:
                        our_graph.nodes[i]['vote'] = 1
                else:
                    continue
            round = round + 1
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








#here we will try the countermeasure experiments


#geometric graphs

#hyperbolic graph generator
#hg = nk.generators.HyperbolicGenerator(n=1000000,k=100, gamma=2.5, T=0)
#hgG = hg.generate()
#print(hgG.numberOfNodes(), hgG.numberOfEdges())
#gamma is usually in range between 2 or 3
#nxG = nk.nxadapter.nk2nx(hgG)

#RMAT generator
#scale = math.log(1000000,2)
#rmat = nk.generators.RmatGenerator(scale, 2.627, 0.4, 0.1, 0.1, 0.4)
#rmatG = rmat.generate()
#print(rmatG.numberOfNodes(), rmatG.numberOfEdges())
#nxRmat = nk.nxadapter.nk2nx(rmatG)

#MONCK GENERATOR
#mg = nk.generators.MocnikGenerator(3, 1000000, 1)
#mgG = mg.generate()
#print(mgG.numberOfNodes(), mgG.numberOfEdges())
#nxMG = nk.nxadapter.nk2nx(mgG)

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
#G_citation = nx.read_edgelist('networks/cit-HepPh.txt', create_using=nx.Graph(), noetype=int)




#percentage = pow(hgG.numberOfEdges(), 0.5)/hgG.numberOfNodes()
#print(percentage)
#try RMAT again.
#elite_experiment(our_graph=nxRmat, elite_percentage=0.0015, influence_factor=1000, honest=True, counter_measure=False)