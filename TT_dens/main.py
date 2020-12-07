import sys
import os
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(ROOT_DIR)
from TT_dens.bigsim_TTDens import bigsimulation_dens_TT
from TT_dens.repetitions import loopgraphtypes
from SP_IMP import slashdot_loc, twitter_loc, fb_loc, orkut_loc, yt_loc, flickr_loc, gowalla_loc, BK_loc, citation_loc


if __name__ == "__main__":
    loopgraphtypes(graph_loc=fb_loc, reps=4, type_graphs=['ER'], edge_constant_mult=1, small=True, stubrat_blue=0.8, stubrat_red=0.7,
                   n_compgraph=20000, n_ERHD=10000, p_ERHD=0.05)