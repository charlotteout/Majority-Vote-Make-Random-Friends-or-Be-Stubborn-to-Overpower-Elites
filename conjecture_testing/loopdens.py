from conjecture_testing.simulation_CT import simulation_conj
import networkx as nx
import networkit as nk
import os
abs_path = os.path.abspath(os.path.dirname(__file__))


def loop_p(reps,n,p):
    replist = []
    for i in range(reps):
        rep = simulation_conj(n=n, p=p)
        replist.append(rep)
    print(replist)
    return(replist)

