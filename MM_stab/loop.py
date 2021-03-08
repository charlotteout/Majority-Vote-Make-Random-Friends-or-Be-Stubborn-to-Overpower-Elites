from MM_stab.bigsimulation import bigsimulation_stab
import networkx as nx
import networkit as nk
import os
abs_path = os.path.abspath(os.path.dirname(__file__))

def loopgraphtypes(graph_loc, reps, edge_constant_mult, type_graphs):
    """ Simply a function to loop over the different graph types """
    graph_dict = {}
    for GT in type_graphs:
        newreplist = repetitions(graph_loc, type_graph=GT, reps=reps, edge_constant_mult=edge_constant_mult)
        graph_dict[GT] = newreplist

    print(graph_dict)
    return graph_dict



def repetitions(graph_loc, type_graph, reps, edge_constant_mult):
    """ Simply a function that repeats the process a couple of times """
    replist = []
    for rep in range(reps):
        simlist = bigsimulation_stab(graph_loc=graph_loc, type_graph=type_graph, def_ratio=0.5, edge_constant_mult=edge_constant_mult)
        replist.append(simlist)
    return replist