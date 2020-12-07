import random
import networkx
import networkit

def simulation_stab_TT(our_graph, honest, initial_prob_dens, stubrat_blue, stubrat_red):

    #print("---------------------")
    #print("initial prob dens", initial_prob_dens)

    for node in our_graph.nodes:
        if (random.random() < (1-initial_prob_dens)):
            our_graph.nodes[node]['vote'] = 0
        else:
            our_graph.nodes[node]['vote'] = 1


    if honest:
        change = 2
        round = 1
        cur_num_blue = 0
        cur_num_red = 0
        prev_num_blue = 0
        prev_num_red = 0
        while change != 0:
            change_prev = change
            change = 0
            prevprev_num_blue = prev_num_blue
            prevprev_num_red = prev_num_red
            prev_num_blue = cur_num_blue
            prev_num_red = cur_num_red
            cur_num_blue = 0
            cur_num_red = 0
            for i in our_graph.nodes:
                personal_vote = our_graph.nodes[i]['vote']
                # print("num neighs our graph", len(list(our_graph.adj[i])))
                # print("num neighs cm graph", len(list(cm_graph.adj[i])))
                total_vote = 0
                if our_graph.adj[i] == {}:
                    our_graph.nodes[i]['pseudo_vote'] = our_graph.nodes[i]['vote']
                else:
                    for j in our_graph.adj[i]:
                        total_vote = our_graph.nodes[j]['vote'] + total_vote


                    if total_vote == 0:
                        cur_rat = 0
                    else:
                        denominator = 0
                        for j in our_graph.adj[i]:
                            denominator = denominator + 1

                        cur_rat = total_vote / denominator

                    if personal_vote == 0:
                        if cur_rat > stubrat_blue:
                            our_graph.nodes[i]['pseudo_vote'] = 1
                            change = change + 1
                        else:
                            our_graph.nodes[i]['pseudo_vote'] = 0
                    if personal_vote == 1:
                        if cur_rat < (1 - stubrat_red):
                            our_graph.nodes[i]['pseudo_vote'] = 0
                            change = change + 1
                        else:
                            our_graph.nodes[i]['pseudo_vote'] = 1

            #create the pseudovodes into actual votes.
            for i in our_graph.nodes:
                if our_graph.nodes[i]['pseudo_vote'] == 0:
                    our_graph.nodes[i]['vote'] = 0
                    cur_num_blue = cur_num_blue + 1
                if our_graph.nodes[i]['pseudo_vote'] == 1:
                    our_graph.nodes[i]['vote'] = 1
                    cur_num_red = cur_num_red + 1

            round = round + 1
            # plot the network
            if change_prev == change:
                if cur_num_blue == prevprev_num_blue and cur_num_red == prevprev_num_red:
                    #print("rounds: ", round)
                    return round


            if change == 0:
                #print('rounds: ', round)
                return(round)

    if not honest:

        change = 2
        round = 1
        cur_num_blue = 0
        cur_num_red = 0
        prev_num_blue = 0
        prev_num_red = 0
        while change != 0:
            change_prev = change
            change = 0
            prevprev_num_blue = prev_num_blue
            prevprev_num_red = prev_num_red
            prev_num_blue = cur_num_blue
            prev_num_red = cur_num_red
            cur_num_blue = 0
            cur_num_red = 0
            for i in our_graph.nodes:
                total_vote = 0
                for j in our_graph.adj[i]:
                    total_vote = our_graph.nodes[j]['vote'] + total_vote

                if total_vote == 0:
                    ratio = 0
                else:
                    denominator = 0
                    for j in our_graph.adj[i]:
                        denominator = denominator + 1

                    ratio = total_vote / denominator

                if our_graph.nodes[i]['elite'] == 0:
                    if ratio < 0.5:
                        if our_graph.nodes[i]['vote'] != 0:
                            change = 1 + change
                        cur_num_blue = cur_num_blue + 1
                        our_graph.nodes[i]['pseudo_vote'] = 0
                    if ratio >= 0.5:
                        if our_graph.nodes[i]['vote'] != 1:
                            change = 1 + change
                        our_graph.nodes[i]['pseudo_vote'] = 1
                        cur_num_red = cur_num_red + 1

                if our_graph.nodes[i]['elite'] == 1:
                    our_graph.nodes[i]['vote'] = 1
                    cur_num_red = cur_num_red + 1


            #create the pseudovotes into actual votes.
            for i in our_graph.nodes:
                if our_graph.nodes[i]['elite'] == 0:
                    if our_graph.nodes[i]['pseudo_vote'] == 0:
                        our_graph.nodes[i]['vote'] = 0
                    if our_graph.nodes[i]['pseudo_vote'] == 1:
                        our_graph.nodes[i]['vote'] = 1
                else:
                    continue
            round = round + 1
            if change_prev == change:
                if cur_num_blue == prevprev_num_blue and cur_num_red == prevprev_num_red:
                    #print("rounds: ", round)
                    return (round)

            if change == 0:
                #print('rounds:',round)
                return (round)