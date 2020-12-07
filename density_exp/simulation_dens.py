import random
import networkx
import networkit

def simulation_dens(our_graph, honest, initial_prob_dens, def_ratio):

    #print("----------------------------")
    #print("init prob dens", initial_prob_dens)

    for node in our_graph.nodes:
        if (random.random() < initial_prob_dens):
            our_graph.nodes[node]['vote'] = 1
        else:
            our_graph.nodes[node]['vote'] = 0


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
                #print("num neighs our graph", len(list(our_graph.adj[i])))
                #print("num neighs cm graph", len(list(cm_graph.adj[i])))
                total_vote = 0
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
                    if cur_rat > def_ratio:
                        our_graph.nodes[i]['pseudo_vote'] = 1
                        change = change + 1
                    else:
                        our_graph.nodes[i]['pseudo_vote'] = 0
                if personal_vote == 1:
                    if cur_rat < (1 - def_ratio):
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
                    #print("blink 1", prev_num_blue, prev_num_red)
                    #print("blink 2", cur_num_blue, cur_num_red)
                    redsum = prev_num_red + cur_num_red
                    bluesum = prev_num_blue + cur_num_blue
                    #print("red density: ", redsum / (redsum + bluesum))
                    return (redsum / (redsum + bluesum))


            if change == 0:
                #print(cur_num_blue, cur_num_red)
                #print(cur_num_red /(cur_num_red + cur_num_blue))
                return(cur_num_red /(cur_num_red + cur_num_blue))

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
                    #print("blink 1", prev_num_blue, prev_num_red)
                    #print("blink 2", cur_num_blue, cur_num_red)
                    redsum = prev_num_red + cur_num_red
                    bluesum = prev_num_blue + cur_num_blue
                    #print("red density: ",redsum / (redsum + bluesum))
                    return (redsum / (redsum + bluesum))

            if change == 0:
                #print(cur_num_blue, cur_num_red)
                #print("red density:", cur_num_red / (cur_num_blue + cur_num_red))
                return (cur_num_red / (cur_num_blue + cur_num_red))