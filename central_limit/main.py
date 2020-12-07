import sys
import os
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(ROOT_DIR)
from SP_IMP.bigsimulation import bigsimulation
from SP_IMP import slashdot_loc, twitter_loc, fb_loc, orkut_loc, yt_loc, flickr_loc, gowalla_loc, BK_loc, citation_loc
from central_limit.bigsim_centrallim import bigsim
from central_limit.Gnp_gen import our_gnp_fixed_assignment




if __name__ == "__main__":
    bigsim(n=10000, reps=20)
