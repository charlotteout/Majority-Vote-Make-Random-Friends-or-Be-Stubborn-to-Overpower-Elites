import sys
import os
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(ROOT_DIR)
from SP_IMP.bigsimulation import bigsimulation
from SP_IMP import slashdot_loc, twitter_loc, fb_loc, orkut_loc, yt_loc, flickr_loc, gowalla_loc, BK_loc, citation_loc


if __name__ == "__main__":
    bigsimulation(graph_loc=fb_loc, counter_measure=True, type_graph='Reg', centrality_measure=1, def_ratio=0.5, mult=1)
