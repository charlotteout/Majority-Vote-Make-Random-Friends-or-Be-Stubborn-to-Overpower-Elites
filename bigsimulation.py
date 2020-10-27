import networkx as nx
from simulations import elite_experiment


def bigsimulation(our_graph, countermeasure):
    """
    :param our_graph: networkx or networkit object
    :param countermeasure: boolean, if we perform the countermeasure experiment
    :return:
    """
    for elite_inf_factor in [1,2,4,8,16,32,64,128,256,512,1024,2048]:
        print("elite_factor",elite_inf_factor)
        if not countermeasure:
            for elite_size in [0.05, 0.1,0.15,0.20,0.25,0.30,0.35,0.40,0.45,0.50,0.55,0.60,0.65,0.70,0.75,0.80,0.85,0.90,0.95]:
                print("elite size", elite_size)
                winner = elite_experiment(our_graph=our_graph, our_elite_size=elite_size,
                                          influence_factor=elite_inf_factor, honest=True, counter_measure=False, centrality_measure=1)
                if winner == 'red':
                    print("break leave the loop")
                    break
                if winner == 'blue':
                    continue

        if countermeasure:
            for elite_size in [0.80,0.825,0.85,0.875, 0.90,0.925,0.95, 0.985,1]:
                print("elite size", elite_size)
                winner = elite_experiment(our_graph=our_graph, our_elite_size=elite_size, influence_factor=elite_inf_factor)
                if winner == 'red':
                    print("break leave the loop")
                    break
                if winner == 'blue':
                    continue






#hyperbolic graph generator
#hg = nk.generators.HyperbolicGenerator(n=1138499,k=5.25, gamma=2.5, T=0.5)
#hgG = hg.generate()
#print(hgG.numberOfNodes(), hgG.numberOfEdges())
#gamma is usually in range between 2 or 3
#nxG = nk.nxadapter.nk2nx(hgG)
#G_ba = nx.barabasi_albert_graph(n=1138499, m=5)


#bigsimuation(G_ba)