from conjecture_testing.simulation_CT import simulation_conj
import networkx as nx
import networkit as nk
import os
abs_path = os.path.abspath(os.path.dirname(__file__))


def loop_p(reps,n,p):
    """
    Simply a function that allows us to repeat this process a number of times as this is a random
    process and we would like to take an average
    :param reps: integer, the number of repretitions
    :param n: number of nodes in the Erdös-Rènyi graph
    :param p: density in the Erdös-Rènyi graph
    :return: a list of tuples
    """
    replist = []
    for i in range(reps):
        rep = simulation_conj(n=n, p=p)
        replist.append(rep)
    print(replist)
    return(replist)

