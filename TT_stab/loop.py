from TT_stab.bigsimulation import bigsimulation_stab_TT
import networkx as nx
import networkit as nk
import os
abs_path = os.path.abspath(os.path.dirname(__file__))

def loopgraphtypes(graph_loc, reps, edge_constant_mult, type_graphs, stubrat_blue, stubrat_red):
    graph_dict = {}
    for GT in type_graphs:
        newreplist = repetitions(graph_loc, type_graph=GT, reps=reps, edge_constant_mult=edge_constant_mult,
                                 stubrat_blue=stubrat_blue, stubrat_red=stubrat_red)
        graph_dict[GT] = newreplist

    print(graph_dict)
    return graph_dict



def repetitions(graph_loc, type_graph, reps, edge_constant_mult, stubrat_blue, stubrat_red):
    replist = []
    for rep in range(reps):
        simlist = bigsimulation_stab_TT(graph_loc=graph_loc, type_graph=type_graph, edge_constant_mult=edge_constant_mult,
                                        stubrat_blue=stubrat_blue, stubrat_red=stubrat_red)
        replist.append(simlist)
    return replist