from stabilization_time_exp.bigsim_stab import bigsimulation_stab
import networkx as nx
import networkit as nk
import os
abs_path = os.path.abspath(os.path.dirname(__file__))




def loopratio_bigsim(graph_loc, type_graph):
    big_ratiolist = []
    for def_ratio in [0.6,0.7,0.8,0.9]:
        rprat_list = bigsimulation_stab(graph_loc=graph_loc, type_graph=type_graph, def_ratio=def_ratio)
        big_ratiolist.append((def_ratio, rprat_list))
    print(big_ratiolist)
    return big_ratiolist

