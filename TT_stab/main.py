import sys
import os
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(ROOT_DIR)
from TT_stab.loop import loopgraphtypes
from Winning_Set import slashdot_loc, twitter_loc, fb_loc, yt_loc


if __name__ == "__main__":
    loopgraphtypes(graph_loc=twitter_loc, reps=1, type_graphs=['BA', 'ER'], edge_constant_mult=1,
                   stubrat_blue=0.8, stubrat_red=0.7)