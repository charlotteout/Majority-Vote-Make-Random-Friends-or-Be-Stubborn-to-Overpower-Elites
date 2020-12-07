from density_exp.bigsimulation_dens import bigsimulation_dens
import networkx as nx
import networkit as nk
import os
abs_path = os.path.abspath(os.path.dirname(__file__))

def loopgraphtypes(graph_loc, reps, edge_constant_mult, small, graph_types):
    graph_dict = {}
    if small==True:
        for GT in graph_types:
            newreplist = repetitions(graph_loc=graph_loc, type_graph=GT, reps=reps, edge_constant_mult=edge_constant_mult,small=small)
            graph_dict[GT] = newreplist

    else:
        for GT in graph_types:
            newreplist = repetitions(graph_loc=graph_loc, type_graph=GT, reps=reps, edge_constant_mult=edge_constant_mult,small=small)
            graph_dict[GT] = newreplist

    print(graph_dict)
    return graph_dict


def repetitions(graph_loc, type_graph, reps, edge_constant_mult, small):
    replist = []
    for rep in range(reps):
        simlist = bigsimulation_dens(graph_loc=graph_loc, type_graph=type_graph, def_ratio=0.5,
                                     edge_constant_mult=edge_constant_mult, small=small)
        replist.append(simlist)
    #print(replist)
    return replist
