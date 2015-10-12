Source code in Python for running simulations of model showing the effect of mobility on group-entitative and individual-entitative behavior.

This README goes through the functionalities of each file in the source code. The code has been tested with Python version 2.7.8. It requires the NumPy package and the matplotlib library.

==================================

To run the main simulation, use:

	python main.py {run_number} {mobility_probability} {graph_initialization}
	
*run_number*: indicates a unique identifier for that particular run (start numbering the runs from 1, 2, ...). In our paper, we run 100 identical runs of the same settings and then average the results together (i.e., *run_number* going from 1 to 100).

*mobility_probability*: probability of an agent to move to a random empty spot on the grid. In our paper, we use mobility probabilities from 0.0 to 0.08 in steps of 0.01 for our experiments (reasons for choosing this particular range is provided in the supplemental material).

*graph_initialization*: indicates how to initialize agents on the grid network. It can take values 0, 1, 2, 3, 4, where each of them are defined as follows:

- 0: start with empty grid (no agents on any of the nodes). This is the same setting as used in Hammod & Axelrod, 2006.
- 1: each node on the grid is initialized with an agent with random traits.
- 2: each node on the grid is initialized with group-entitative agents of the same tag, playing Cooperate with in-group agents, and Defect with out-group agents.
- 3: each node on the grid is initialized with group-entitative agents of the same tag, playing Cooperate with in-group agents, and TFT with out-group agents.
- 4: each node on the grid is initialized with individual-entitative agents playing TFT against other agents.

Thus, an example run, with mobility probability 0.05 and initializing the graph using option 1, would look like the following:

	python main.py 1 0.05 0

==================================

Each run outputs 8 files in the results folder. This section contains description of each type of output file. The results folder is specified in *globals.py* using the variable name *results_folder*.

- *alive_\**: proportion of nodes which have agents on them
- *coeff_\**: clustering coefficient of the grid (calculated as described in the paper)
- *diff_games_\**: 
- *inStratCounts_\**:
- *indivStratCounts_\**:
- *outStratCounts_\**:
- *results_\**:
- *tagCounts_\**:

----------------------------------


==================================
==================================
==================================



