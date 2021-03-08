****
## Explenation on the project 

In this project, we look at opinion diffusion on graphs. Here, a graph G represents a social network. We assume that initially each node is colored either black or white, which corresponds to a positive or negative opinion regarding a consumer product or a technolog- ical innovation.

To model the influence that the people around you (your neighbors in the social network), several update rules have been proposed. A well known example of such an update rule is the "majority model", in which  each round all nodes simultaneously update their color to the most frequent color among their connections.

In this project we investigate the majority model and a related model called the (psi1,psi2)-majority model both theoretically as well as experimentally on social networks. The code used for the experimental part can be found in this repository. The exact structure and fuction of the code is explained later in this readme (under code structure). 

The paper we wrote including the theoretical results and the figures of the experimental results is also included in this repo, which contains more information on what exactly we investigated

## Dependencies and Data
To run the code, please make sure to download the datasets
from the following sites:

Facebook: http://socialnetworks.mpi-sws.org/data-wosn2009.html \
Twitter: http://snap.stanford.edu/data/ego-Twitter.html \
Slashdot: http://snap.stanford.edu/data/soc-Slashdot0902.html \
Youtube: http://socialnetworks.mpi-sws.org/data-imc2007.html

All the datasets are already provided in the folder "networks" inside the code directory
The local paths are set in the init of the module "Winning_Set". 

To use this code, one should install the dependencies that you find
listed in the file _requirements.txt._ file in the code directory.

It would be easy if these would be installed in a virtual environment

```angular2
#install pipenv if you don't have this
pip install --user pipenv
pipenv install
```


To update the requirements file:
```angular2
pipenv lock -r > requirements.txt
```

However, if you don't want to set up a virtual environment you can 
still download the requirements as follows
```angular2
#make sure to run this command in the code directory 
pip install -r requirements.txt
```

The code in particular heavily depends on 
```angular2
networkit==5.0.1
networkx==2.3
```
## Code Structure
The code is split up in 7 small modules. 

The modules we implemented are
- Winning_Set: Compute the minimum size of a winning set of nodes for a given influence factor.
In addition countermeasure 1 is implemented here
- CM2: Compute the minimum size of a winning set when countermeasure 2 is applied to the graph
- MM_dens: Compute the final fraction of black (red) nodes for a given initial probability with 
which nodes are colored black in the majority model
- MM_stab: Compute the stabilization time in rounds for a given initial probability with 
which nodes are colored black in the majority model
- TT_dens: Compute the final fraction of black (red) nodes for a given initial probability with 
which nodes are colored black in the (psi1,psi2)-majority model
- TT_stab: Compute the stabilization time in rounds for a given n initial probability of black (red) nodes for a given initial probability with 
which nodes are colored black in the (psi1,psi2)-majority model
- conjecture testing: the number of nodes that are black and white (red and blue) in the final configuration
of the majority model on an Erdös-Renyi graph

Each module except for the module "conjecture testing"
consistst of 4 files
- main: from which the code is run 
- simulation: the implementation of the current variant of the majority model 
- bigsimulation: a function that generates the correct graph structure based on the social network considered
and implements coutermeasure 1. In addition, it loops over some parameters of the simulation function and
calls the simulation function
- loop: a file with dummy functions to loop over several graph types or in the case that the
experiment involves randomness repeat the experiment several times

## How to run the experiments
- To obtain the results in **Figure 1 (left)** 
run the function in main in module Winning_Set with parameters 
```angular2
graph_locs = yt_loc
graph_types = ['BA', 'Hyp','Reg']
counter_measure= False
mult = 2 
def_ratio = 0.5 
```
For Figures 5a, 5b and 5c in Appendix F.1, change graph_locs into  slashdot_loc,
fb_loc and twitter_loc respectively.

- To obtain the results in **Figure 1 (right)** for the graph of CM1 run 
the function in main in the module Winning_Set with parameters 
```angular2
graph_locs = fb_loc
graph_types = ['Reg']
counter_measure= True 
mult = 2 
def_ratio = 0.5 
```

and to obtain the graph of CM2 run the function in main in the module CM2
with parameters
```angular2
graph_locs = [fb_loc]
mult = 2 
```
The graph of SN can be reused from Figure 1(left). For the Figures 6a,6b and 6c in
Appendix F.2, change graph_locs into [slashdot_loc],
[fb_loc] and [twitter_loc respectively].

- To obtain the results in **Figure 2 (left)** run the function in main in
the module MM_dens for the parameters 

```angular2
graph_locs=slashdot_loc 
reps=8 
edge_constant_mult=1
smalll = False
graph_types = ['ER', 'BA', 'Hyp', 'Reg', 'DReg', 'CM']
```
The Figures 7a, 7b and 7c in Appendix F.3 one should change the graph_locs into 
fb_loc, twitter_loc and yt_loc respectively. Note that the reps=8 and all these
graph types could take a long time to compute all at once. Alternatively, one could split up this computation
by considering the graph types ['ER', 'BA', 'Hyp'] first and then ['Reg','DReg','CM'], or lower the number of reps (repetitions).

- To obtain the results in **Figure 2(right)** run the function in main in the
module TT_dens for the parameters 
```angular2
graph_locs = twitter_loc
reps = 8
type_graphs = ['BA', 'Hyp', 'Reg', 'DReg]
stubrat_blue = 0.8
stubrat_red = 0.7
```
To obtain the data for Figures 8a, 8b and 8c in Appendix F.4 one should change
the graph_locs into fb_loc, slashdot_loc and yt_loc respectively.

- To obtain the results in **Figure 3 (left)** run function in main in the module
MM_stab for the parameters 
```angular2
graph_locs=slashdot_loc
reps=8
edge_constant_mult=1
smalll = False
graph_types = ['ER', 'BA', 'Hyp', 'Reg', DReg', 'CM']
```
to obtain the data for Figures 9a, 9b and 9c in Appendix F.5 one should change the graph locs
into fb_loc, twitter_loc and yt_loc respectively.

- To obtain the results in **Figure 3 (right)** run the function in main in 
TT_stab for the parameters 
```angular2
graph_locs = twitter_loc
reps = 8
type_graphs = ['BA', 'Hyp', 'Reg', 'DReg']
stubrat_blue = 0.8
stubrat_red = 0.7
```
To obtain the data for Figures 10a, 10b and 10c in Appendix F.6 one should change
the graph_locs into fb_loc, slashdot_loc and yt_loc respectively.

For the experiments that contain randomness, we take the average of the results for the
x repetitions using the averages helper function in averages.py

To generate the figures in the main body of the text, the helper file plots_text.py
was used. To generate the figures in the appendix of the test, the helper file
plots_appendix was used. 








 


 
