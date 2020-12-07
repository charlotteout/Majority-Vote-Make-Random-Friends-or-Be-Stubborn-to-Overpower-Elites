import sys
import os
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(ROOT_DIR)
from ratio_exp.bigsim_ratio import bigsimulation_ratio
from SP_IMP import slashdot_loc, twitter_loc, fb_loc, orkut_loc, yt_loc, flickr_loc, gowalla_loc, BK_loc, citation_loc


if __name__ == "__main__":
    bigsimulation_ratio(graph_loc=twitter_loc, counter_measure=False, type_graph='Reg', edge_constant_mult=20, centrality_measure=0)