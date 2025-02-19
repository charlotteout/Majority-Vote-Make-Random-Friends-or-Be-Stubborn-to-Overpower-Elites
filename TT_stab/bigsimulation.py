from TT_stab.simulation import simulation_TT_stab
import networkx as nx
import networkit as nk
import os
abs_path = os.path.abspath(os.path.dirname(__file__))

def bigsimulation_stab_TT(graph_loc, type_graph, stubrat_blue, stubrat_red, edge_constant_mult):
    print("graph_loc:", graph_loc)
    temp_graph = nx.read_edgelist(os.path.join(abs_path, graph_loc), create_using=nx.Graph(), nodetype=int)
    mapping = dict(zip(temp_graph, range(0, temp_graph.number_of_nodes() - 1)))
    temp_graph = nx.relabel_nodes(temp_graph, mapping)
    total = sum(j for i, j in list(temp_graph.degree(temp_graph.nodes)))
    av_deg = total / temp_graph.number_of_nodes()
    p = total / (temp_graph.number_of_nodes()*(temp_graph.number_of_nodes()-1))
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
    if type_graph == 'DReg':
        print("D-Regular graph")
        d = int(av_deg)
        if ((d * temp_graph.number_of_nodes()) % 2 != 0):
            d = d + 1
        else:
            d = d
        print(temp_graph.number_of_nodes())
        our_graph = nx.random_regular_graph(d=d, n=temp_graph.number_of_nodes())
        print("our graph num nodes",our_graph.number_of_nodes())
    if type_graph == 'CM':
        print("CM graph, original + dreg random graph added to it")
        d = int(edge_constant_mult * av_deg)
        if ((d * temp_graph.number_of_nodes()) % 2 != 0):
            d = d + 1
        else:
            d = d
        G_dreg = nx.random_regular_graph(d=d, n=temp_graph.number_of_nodes())
        print("done generating the d-regular random graph")
        our_graph = nx.compose(temp_graph, G_dreg)
    if type_graph == 'Reg':
        print("Regular Graph")
        our_graph = temp_graph
    final_rounds_list = []
    for init_dens in [0.1,0.15, 0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9]:
        final_dens = simulation_TT_stab(our_graph=our_graph, initial_prob_dens=init_dens,
                                        stubrat_blue=stubrat_blue, stubrat_red=stubrat_red)
        final_rounds_list.append(final_dens)
    return final_rounds_list