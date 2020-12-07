from ratio_exp.simulation_ratio import elite_experiment
import networkx as nx
import networkit as nk
import os
abs_path = os.path.abspath(os.path.dirname(__file__))


def bigsimulation_ratio(graph_loc, counter_measure, type_graph, edge_constant_mult, centrality_measure):
    """
    :param our_graph: networkx or networkit object
    :param countermeasure: boolean, if we perform the countermeasure experiment
    :return:
    """
    print("graph_loc:", graph_loc)
    temp_graph = nx.read_edgelist(os.path.join(abs_path, graph_loc),create_using=nx.Graph(), nodetype=int)
    print("num nodes", temp_graph.number_of_nodes())
    print('num edges', temp_graph.number_of_edges())
    print("countermeasure:", counter_measure)
    print("mult factor countermeasure:", edge_constant_mult)
    total = sum(j for i, j in list(temp_graph.degree(temp_graph.nodes)))
    av_deg = total / temp_graph.number_of_nodes()
    p = total / (temp_graph.number_of_nodes() * (temp_graph.number_of_nodes() - 1))
    if type_graph == 'ER':
        print("ER graph")
        our_graph = nx.gnm_random_graph(n=temp_graph.number_of_nodes(), p=p)
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

    if counter_measure:
        total = sum(j for i, j in list(our_graph.degree(our_graph.nodes)))
        av_deg = total / our_graph.number_of_nodes()
        print("av_deg", av_deg)

        d = int(edge_constant_mult * av_deg)
        print('d',d)
        if ((d * our_graph.number_of_nodes()) % 2 != 0):
            d = d + 1
        else:
            d = d

        G_dreg = nx.random_regular_graph(d=d, n=our_graph.number_of_nodes())
        print("done generating the d-regular random graph")
        our_graph = nx.compose(our_graph, G_dreg)
        print("done composing the graphs")


    stubbornness_ratio_list = []
    for stubbornness_ratio in [0.5,0.55,0.60,0.65,0.70,0.75,0.80,0.85,0.90,0.95]:
        print("stubbornness_ratio", stubbornness_ratio)
        if not counter_measure:
            for stubborn_size in [0.10,0.15,0.20,0.25,0.30,0.35,0.40,0.45,0.50,0.55,0.60]:
                print("stubborn size", stubborn_size)
                winner = elite_experiment(our_graph=our_graph, our_stubborn_size=stubborn_size,
                                          stubbornness_ratio=stubbornness_ratio, def_ratio=0.5, centrality_measure=centrality_measure)
                if winner == 'red':
                    stubbornness_ratio_list.append(stubborn_size)
                    print("break leave the loop")
                    break
                if winner == 'blue':
                    continue

        if counter_measure:
            #call the graph init here
            for stubborn_size in [0.10,0.15,0.20,0.25,0.30,0.35,0.40,0.45,0.50,0.55,0.60]:
                print("stubborn size", stubborn_size)
                winner = elite_experiment(our_graph=our_graph,our_stubborn_size=stubborn_size,
                                          stubbornness_ratio=stubbornness_ratio, def_ratio=0.5, centrality_measure=centrality_measure)
                if winner == 'red':
                    stubbornness_ratio_list.append(stubborn_size)
                    print("break leave the loop")
                    break
                if winner == 'blue':
                    continue
    print("stubborn ratio size list", stubbornness_ratio_list)
