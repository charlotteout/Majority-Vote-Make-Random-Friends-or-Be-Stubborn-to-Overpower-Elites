from CM2.bigsim_CM2 import bigsimulation
import networkx as nx
import networkit as nk
import os
abs_path = os.path.abspath(os.path.dirname(__file__))
from SP_IMP import slashdot_loc, twitter_loc, fb_loc, orkut_loc, yt_loc, flickr_loc, gowalla_loc, BK_loc, citation_loc


def looptypegraph(mult, range_mult):
    if range_mult:
        multlist = []
        for cur_mult in range(mult):
            graph_dict = {}
            for graph_loc in [fb_loc, slashdot_loc,twitter_loc]:
            #for graph_loc in [fb_loc]:
                elite_size_list = bigsimulation(graph_loc=graph_loc, mult=cur_mult+1, type_graph='Reg')
                graph_dict[yt_loc] = elite_size_list
                multlist.append(graph_dict)
        print(multlist)
        return(multlist)
    else:
        graph_dict = {}
        for graph_loc in [fb_loc, slashdot_loc,twitter_loc]:
            elite_size_list = bigsimulation(graph_loc=graph_loc, mult=mult, type_graph='Reg')
            graph_dict[yt_loc] = elite_size_list
        print(graph_dict)
        return(graph_dict)


