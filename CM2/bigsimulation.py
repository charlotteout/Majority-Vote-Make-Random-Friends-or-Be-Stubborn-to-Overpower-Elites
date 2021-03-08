from CM2.simulation import elite_experiment
import networkx as nx
import networkit as nk
import os
abs_path = os.path.abspath(os.path.dirname(__file__))


def bigsimulation(graph_loc, mult):
    """
    :param graph_loc: location of the graph dataset we are loading (saved in Winning_Set init)
    :return: a list of the elite sizes required to win for different influence factors
    """
    our_graph = nx.read_edgelist(os.path.join(abs_path, graph_loc),create_using=nx.Graph(), nodetype=int)


    elite_size_list = []
    #loop over the influence factors
    for elite_inf_factor in [1,2,4,8,16]:
        #loop over the elite sizes in the form of y such that n^y is the elite size
        for elite_size in [0.70,0.75,0.80,0.85,0.90,0.95]:
            #define the "stubbornness" of all the nodes
            def_ratio_CM = (1 - 1/(mult*elite_inf_factor))
            winner = elite_experiment(our_graph=our_graph,our_elite_size=elite_size, influence_factor=elite_inf_factor,
                                      def_ratio_CM=def_ratio_CM)
            if winner == 'red':
                elite_size_list.append(elite_size)
                #leave the loop, and append this elite size, as we know that this size is sufficient
                #for the elites to win
                break
            if winner == 'blue':
                continue
    print("elite size list", elite_size_list)
    return elite_size_list