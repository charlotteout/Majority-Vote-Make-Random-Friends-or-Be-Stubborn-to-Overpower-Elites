from central_limit.Gnp_gen import our_gnp_fixed_assignment
from central_limit.simulation_centrallim import sim_centrallim

def bigsim(n, reps):
    num_red_win = 0
    num_blue_win = 0
    for rep in range(reps):
        winner = sim_centrallim(n=n, def_ratio=0.5)
        if winner == 'blue':
            num_blue_win = num_blue_win + 1
        if winner == 'red':
            num_red_win = num_red_win + 1
    print("num red:",num_red_win)
    print("num blue:", num_blue_win)