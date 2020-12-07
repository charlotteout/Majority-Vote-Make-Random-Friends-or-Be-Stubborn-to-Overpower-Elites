from SP_IMP.simulations import elite_experiment
import networkx as nx
import networkit as nk
import os
abs_path = os.path.abspath(os.path.dirname(__file__))


def bigsimulation(graph_loc, counter_measure, type_graph, centrality_measure, def_ratio, mult):
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
    print("countermeasure:", counter_measure)
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
    if not counter_measure:
        for elite_inf_factor in [1,2,4,8,16,32,64,128,256,512,1024,2048]:
            print("elite_factor",elite_inf_factor)
            for elite_size in [0.05, 0.1,0.15,0.20,0.25,0.30,0.35,0.40,0.45,0.50,0.55,0.60,0.65,0.70,0.75,0.80,0.85,0.90,0.95]:
                print("elite size", elite_size)
                winner = elite_experiment(our_graph=our_graph, our_elite_size=elite_size,
                                          influence_factor=elite_inf_factor, honest=True, centrality_measure=centrality_measure,
                                          counter_measure=False, def_ratio=def_ratio)
                if winner == 'red':
                    elite_size_list.append(elite_size)
                    print("break leave the loop")
                    break
                if winner == 'blue':
                    continue

    if counter_measure:
        for elite_inf_factor in [1, 2, 4, 8, 16]:
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

            G_dreg = nx.random_regular_graph(d=d, n=our_graph.number_of_nodes())
            print("done generating the d-regular random graph")
            our_graph = nx.compose(our_graph, G_dreg)
            print("done composing the graphs")
            for elite_size in [0.70,0.75,0.80,0.85,0.90,0.95]:
                print("elite size", elite_size)
                winner = elite_experiment(our_graph=our_graph,our_elite_size=elite_size, influence_factor=elite_inf_factor, honest=True,
                                          centrality_measure=centrality_measure, counter_measure=True, def_ratio=def_ratio)
                if winner == 'red':
                    elite_size_list.append(elite_size)
                    print("break leave the loop")
                    break
                if winner == 'blue':
                    continue
    print("elite size list", elite_size_list)






