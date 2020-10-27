import networkx as nx
from bigsimulation import bigsimulation

#defing the graphs

#hyperbolic graph generator
#hg = nk.generators.HyperbolicGenerator(n=1000000,k=100, gamma=2.5, T=0)
#hgG = hg.generate()
#nxG = nk.nxadapter.nk2nx(hgG)

#RMAT generator
#scale = math.log(1000000,2)
#rmat = nk.generators.RmatGenerator(scale, 2.627, 0.4, 0.1, 0.1, 0.4)
#rmatG = rmat.generate()
#print(rmatG.numberOfNodes(), rmatG.numberOfEdges())
#nxRmat = nk.nxadapter.nk2nx(rmatG)

#G_yt = nx.read_edgelist("networks/com-youtube.ungraph.txt",create_using= nx.Graph(), nodetype=int)
#G_slashdot = nx.read_edgelist('networks/soc-Slashdot0902.txt', create_using=nx.Graph(), nodetype=int)
#G_twitter = nx.read_edgelist('networks/twitter_combined.txt', create_using=nx.Graph(), nodetype=int)
#G_fb = nx.read_edgelist('networks/facebook-links2.txt', create_using=nx.Graph(), nodetype=int)
#G_orkut = nx.read_edgelist('networks/com-orkut.ungraph.txt', create_using=nx.Graph(), nodetype=int)
#percentage = pow(len(G_orkut.edges), 0.5)/len(G_orkut.nodes)
#G_yt2 = nx.read_edgelist('networks/youtube-links2.txt', create_using=nx.Graph(), nodetype=int)
#G_flickr = nx.read_edgelist('networks/flickr-links2.txt', create_using=nx.Graph(), nodetype=int)
#G_gowalla = nx.read_edgelist('networks/loc-gowalla_edges.txt', create_using=nx.Graph(), nodetype=int)
#G_BK = nx.read_edgelist('networks/loc-brightkite_edges.txt', create_using=nx.Graph(), nodetype=int)
#G_citation = nx.read_edgelist('networks/cit-HepPh.txt', create_using=nx.Graph(), noetype=int)


Gnm_yt = nx.gnm_random_graph(n=1138499, m=2990444)




if __name__ == "__main__":
    bigsimulation(our_graph=Gnm_yt, countermeasure=False)
