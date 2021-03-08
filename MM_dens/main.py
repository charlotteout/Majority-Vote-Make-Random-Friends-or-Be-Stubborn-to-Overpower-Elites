import sys
import os
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(ROOT_DIR)
from MM_dens.loop import repetitions, loopgraphtypes
from Winning_Set import slashdot_loc, twitter_loc, fb_loc,yt_loc


if __name__ == "__main__":
    loopgraphtypes(graph_loc=twitter_loc, reps=1, edge_constant_mult=1, small=False, graph_types=['CM', 'ER'])