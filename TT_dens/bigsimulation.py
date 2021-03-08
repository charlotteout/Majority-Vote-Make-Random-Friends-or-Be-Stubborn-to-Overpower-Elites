from TT_dens.simulation import simulation_dens_TT
import networkx as nx
import networkit as nk
import os
abs_path = os.path.abspath(os.path.dirname(__file__))

def bigsimulation_dens_TT(graph_loc, type_graph, edge_constant_mult,stubrat_blue, stubrat_red):
    """
    :param graph_loc: A string indicating the location of the graph
    :param type_graph: a string indicating which graph type we are considering i.e. "ER", "BA" etc
    :param edge_constant_mult:
    :param stubrat_blue: stubborness factor assigned to the nodes of color blue
    :param stubrat_red: stubbornness factor assigned to the nodes of color red
    :param n_ERHD: number of nodes for the generation of a high density ER graph
    :param p_ERHD: density for the generation of a high density ER graph
    :return: a list of final densities after the psi_1,psi_2 majority model process for different
    initial densities.
    """

    temp_graph = nx.read_edgelist(os.path.join(abs_path, graph_loc), create_using=nx.Graph(), nodetype=int)
    #relabel the nodes such that the counter measure works properly
    mapping = dict(zip(temp_graph, range(0, temp_graph.number_of_nodes() - 1)))
    temp_graph = nx.relabel_nodes(temp_graph, mapping)
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
        our_graph = nx.random_regular_graph(d=d, n=temp_graph.number_of_nodes())
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
    final_dens_list = []
    for init_dens in [0.1,0.15, 0.2,0.25, 0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9]:
        final_dens = simulation_dens_TT(our_graph=our_graph, initial_prob_dens=init_dens, stubrat_blue=stubrat_blue,
                                        stubrat_red=stubrat_red)
        final_dens_list.append(final_dens)
    print(final_dens_list)
    return(final_dens_list)