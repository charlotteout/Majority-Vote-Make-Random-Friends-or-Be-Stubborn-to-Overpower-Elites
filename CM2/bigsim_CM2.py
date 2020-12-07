from CM2.simCM2 import elite_experiment
import networkx as nx
import networkit as nk
import os
abs_path = os.path.abspath(os.path.dirname(__file__))


def bigsimulation(graph_loc, type_graph, mult):
    """
    :param our_graph: networkx or networkit object
    :param countermeasure: boolean, if we perform the countermeasure experiment
    :return:
    """
    print("graph_loc:", graph_loc)
    temp_graph = nx.read_edgelist(os.path.join(abs_path, graph_loc),create_using=nx.Graph(), nodetype=int)
    print("directed:", nx.is_directed(G=temp_graph))
    print("num nodes", temp_graph.number_of_nodes())
    print('num edges', temp_graph.number_of_edges())

    total = sum(j for i, j in list(temp_graph.degree(temp_graph.nodes)))
    av_deg = total / temp_graph.number_of_nodes()
    p = total / (temp_graph.number_of_nodes() * (temp_graph.number_of_nodes() - 1))
    if type_graph == 'ER':
        print("ER graph")
        our_graph = nx.fast_gnp_random_graph(n=temp_graph.number_of_nodes(), p=p)
    if type_graph == 'BA':
        print("BA graph")
        our_graph = nx.barabasi_albert_graph(n=temp_graph.number_of_nodes(), m=int(av_deg))
    if type_graph == 'Hyp':
        print("Hyp graph")
        hg = nk.generators.HyperbolicGenerator(n=temp_graph.number_of_nodes(), k=av_deg, gamma=2.5, T=0.5)
        hgG = hg.generate()
        our_graph = nk.nxadapter.nk2nx(hgG)
    if type_graph == 'Reg':
        print("Regular Graph")
        our_graph = temp_graph


    elite_size_list = []
    for elite_inf_factor in [1,2,4,8,16,32,64,128,256,512,1024,2048]:
        for elite_size in [0.70,0.75,0.80,0.85,0.90,0.95]:
            #print("----------------------")
            #print("elite size", elite_size)
            def_ratio_CM = (1 - 1/(mult*elite_inf_factor))
            winner = elite_experiment(our_graph=our_graph,our_elite_size=elite_size, influence_factor=elite_inf_factor,
                                      def_ratio_CM=def_ratio_CM)
            if winner == 'red':
                elite_size_list.append(elite_size)
                #print("break leave the loop")
                break
            if winner == 'blue':
                continue
    #print("elite size list", elite_size_list)
    return elite_size_list