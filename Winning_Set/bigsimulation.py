from Winning_Set.simulation import elite_experiment
import networkx as nx
import networkit as nk
import os
abs_path = os.path.abspath(os.path.dirname(__file__))


def bigsimulation(graph_loc, counter_measure, type_graph, def_ratio, mult):
    """
    :param graph_loc: A string representing the location of the social network that we are considering.
    These locations are all written in the init file of this packages
    :param counter_measure: Boolean, True if we consider counter measure 1. Should only be combined with
    graph type = 'Reg'
    :param type_graph: String representing the graph type with comparable parameters to the Social Network we are considering
    i.e. "ER", "BA", "Hyp"
    :param centrality_measure:
    :param def_ratio: float between 0 and 1 representing the "stubbornness" of the nodes
    :param mult: integer, multiplication factor for the counter measure
    :return: List with the required elite sizes
    """
    print("graph_loc:", graph_loc)
    temp_graph = nx.read_edgelist(os.path.join(abs_path, graph_loc),create_using=nx.Graph(), nodetype=int)
    #relabel the node such that the countermeasure 1 works properly
    mapping = dict(zip(temp_graph, range(0, temp_graph.number_of_nodes() - 1)))
    temp_graph = nx.relabel_nodes(temp_graph, mapping)
    print("num nodes", temp_graph.number_of_nodes())
    print('num edges', temp_graph.number_of_edges())
    print("countermeasure:", counter_measure)
    total = sum(j for i, j in list(temp_graph.degree(temp_graph.nodes)))
    av_deg = total / temp_graph.number_of_nodes()
    p = total / (temp_graph.number_of_nodes() * (temp_graph.number_of_nodes() - 1))
    #check which graph type we are working with and change our_graph based on temp_graph accordingly
    if type_graph == 'ER':
        print("ER graph")
        our_graph = nx.fast_gnp_random_graph(n=temp_graph.number_of_nodes(), p=p)
    if type_graph == 'BA':
        print("BA graph")
        our_graph = nx.barabasi_albert_graph(n=temp_graph.number_of_nodes(), m=int(av_deg))
    if type_graph == 'Hyp':
        print("Hyp graph")
        hg = nk.generators.HyperbolicGenerator(n=temp_graph.number_of_nodes(), k=av_deg, gamma=2.5, T=0.6)
        hgG = hg.generate()
        our_graph = nk.nxadapter.nk2nx(hgG)
    if type_graph == 'Reg':
        print("Regular Graph")
        our_graph = temp_graph

    #loop over the influence factors
    elite_size_list = []
    if not counter_measure:
        for elite_inf_factor in [1,2,4,8,16,32,64,128,256,512,1024,2048]:
            #loop over the elite sizes
            for elite_size in [0.05, 0.1,0.15,0.20,0.25,0.30,0.35,0.40,0.45,0.50,0.55,0.60,0.65,0.70,0.75,0.80,0.85,0.90,0.95]:
                winner = elite_experiment(our_graph=our_graph, our_elite_size=elite_size,
                                          influence_factor=elite_inf_factor, def_ratio=def_ratio)
                if winner == 'red':
                    elite_size_list.append(elite_size)
                    print("break leave the loop")
                    break
                if winner == 'blue':
                    continue

    if counter_measure:
        for elite_inf_factor in [1, 2, 4, 8, 16]:
            #determine d
            our_graph = nx.read_edgelist(os.path.join(abs_path, graph_loc),create_using=nx.Graph(), nodetype=int)
            total = sum(j for i, j in list(our_graph.degree(our_graph.nodes)))
            av_deg = total / our_graph.number_of_nodes()
            print("av_deg", av_deg)
            edge_constant_mult = mult * elite_inf_factor
            d = int(edge_constant_mult * av_deg)
            print('d', d)
            if ((d * our_graph.number_of_nodes()) % 2 != 0):
                d = d + 1
            else:
                d = d
            #generate the d-regular random graph
            G_dreg = nx.random_regular_graph(d=d, n=our_graph.number_of_nodes())
            #add the d-regular random graph on top of the original graph
            our_graph = nx.compose(our_graph, G_dreg)
            #loop over the elite sizes
            for elite_size in [0.70,0.75,0.80,0.85,0.90,0.95]:
                winner = elite_experiment(our_graph=our_graph,our_elite_size=elite_size, influence_factor=elite_inf_factor,
                                          def_ratio=def_ratio)
                if winner == 'red':
                    elite_size_list.append(elite_size)
                    print("break leave the loop")
                    break
                if winner == 'blue':
                    continue
    print("elite size list", elite_size_list)






