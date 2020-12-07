import sys
import os
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(ROOT_DIR)
from conjecture_testing.loopdens import loop_p



if __name__ == "__main__":
    loop_p(reps=5, n=1000000, p=11/1000000)