import sys
import os
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(ROOT_DIR)
from stabilization_time_exp.bigsim_stab import bigsimulation_stab
from stabilization_time_exp.loopratio_bigsim import loopratio_bigsim
from stabilization_time_exp.repetitions import repetitions, loopgraphtypes
from SP_IMP import slashdot_loc, twitter_loc, fb_loc, orkut_loc, yt_loc, flickr_loc, gowalla_loc, BK_loc, citation_loc


if __name__ == "__main__":
    loopgraphtypes(graph_loc=twitter_loc, reps=8, edge_constant_mult=1, type_graphs=['DReg'])
    #repetitions(graph_loc=fb_loc, type_graph="ER", reps=8, edge_constant_mult=1)
    #loopratio_bigsim(graph_loc=gowalla_loc, type_graph='Reg')
    #bigsimulation_stab(graph_loc=fb_loc, type_graph="ER", def_ratio=0.5)