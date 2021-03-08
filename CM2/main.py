import sys
import os
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(ROOT_DIR)
from CM2.loop import looptypegraph
from Winning_Set import slashdot_loc, twitter_loc, fb_loc, yt_loc


if __name__ == "__main__":
    looptypegraph(graph_locs=[twitter_loc, fb_loc], mult=2)