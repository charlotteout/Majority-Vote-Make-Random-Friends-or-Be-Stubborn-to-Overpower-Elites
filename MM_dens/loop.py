from MM_dens.bigsimulation import bigsimulation_dens
import networkx as nx
import networkit as nk
import os
abs_path = os.path.abspath(os.path.dirname(__file__))

def loopgraphtypes(graph_loc, reps, edge_constant_mult, small, graph_types):
    """
    :param graph_locs: a list of locations of the graph indicating which social network we are considering
    :param reps: number of times we want to repeat this process
    :param edge_constant_mult: integer, multiplication factor with what we multiply the
    d-regular random graph in the counter measure
    :param small: Boolean, true if we only want to check values around 0.5
    :param graph_types: list of strings of graph types we are considering i.e. ["ER", "BA","Hyp"]
    :return: a dictionary in which the graph locations are the keys with as value a list of final
    densities after the majority model on a random configuration
    """

    graph_dict = {}
    for GT in graph_types:
        newreplist = repetitions(graph_loc=graph_loc, type_graph=GT, reps=reps, edge_constant_mult=edge_constant_mult,small=small)
        graph_dict[GT] = newreplist

    print(graph_dict)
    return graph_dict


def repetitions(graph_loc, type_graph, reps, edge_constant_mult, small):
    """
    Simply a function to allow us to repeat this process a couple of times
    """
    replist = []
    for rep in range(reps):
        simlist = bigsimulation_dens(graph_loc=graph_loc, type_graph=type_graph, def_ratio=0.5,
                                     edge_constant_mult=edge_constant_mult, small=small)
        replist.append(simlist)
    return replist
