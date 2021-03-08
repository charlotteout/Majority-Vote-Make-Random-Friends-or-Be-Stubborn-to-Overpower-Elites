import sys
import os
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(ROOT_DIR)
from Winning_Set.loop import loopgraphtypes

from Winning_Set import slashdot_loc, twitter_loc, fb_loc, yt_loc


if __name__ == "__main__":
    loopgraphtypes(graph_loc=twitter_loc, graph_types=['ER'], counter_measure=True,
                   def_ratio=0.5, mult=2)
