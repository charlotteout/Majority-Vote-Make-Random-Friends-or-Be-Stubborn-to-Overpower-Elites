from Winning_Set.bigsimulation import bigsimulation

def loopgraphtypes(graph_loc, graph_types, counter_measure, def_ratio, mult):
    """ Simply a function to loop over multiple graph types """
    graph_dict = {}
    for GT in graph_types:
        newreplist = bigsimulation(graph_loc=graph_loc, type_graph=GT,counter_measure=counter_measure,
                                   def_ratio=def_ratio, mult=mult)
        graph_dict[GT] = newreplist

    print(graph_dict)
    return graph_dict