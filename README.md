# The Inevitability of Ethnocentrism Revisited: Ethnocentrism Diminishes as Mobility Increases
by Soham De, Michele J Gelfand, Dana S Nau, and Patrick Roos (University of Maryland)

Source code in Python for running simulations of model showing the effect of mobility on group-entitative and individual-entitative behavior. For the original paper published in Nature Scientific Reports, please see [here](http://www.nature.com/articles/srep17963).

This README goes through the functionalities of each file in the source code. The code has been tested with Python version 2.7.8. It requires the NumPy package and the matplotlib library.

-------------------------------------------------------------------

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

-------------------------------------------------------------------

Each run outputs 8 files in the results folder. This section contains description of each type of output file. The results folder is specified in *globals.py* using the variable name *results_folder*.

- *alive_\**: proportion of nodes which have agents on them.
- *coeff_\**: clustering coefficient of the grid (calculated as described in the paper).
- *diff_games_\**: average number of unique agents each agents plays a game against, and average number of games each agent plays against the same agent during its lifetime.
- *inStratCounts_\**: proportion of group-entitative agents playing C, TFT, OTFT, D against in-group agents.
- *indivStratCounts_\**: proportion of individual-entitative agents playing C, TFT, OTFT, D against other agents.
- *outStratCounts_\**: proportion of group-entitative agents playing C, TFT, OTFT, D against out-group agents.
- *results_\**: the columns which are of interest to us are as follows. *inGrpDefPerc*: proportion of total defections against in-group agents. *outGrpDefPerc*: proportion of total defections against out-group agents. *coopProp*: proportion of total cooperations. *collProp*: proportion of group-entitative agents. *indProp*: proportion of individual-entitative agents.
- *tagCounts_\**: number of agents of each group-tag.

-------------------------------------------------------------------

Typically, each particular setting of mobility probability and graph initialization will be run multiple times (say for run numbers from 1 to 100). To average the values over these 100 runs, use the following:

	python aggregate_runs.py
	
It will take all the runs of each type of output file, and output an extra results file containing the average of the values at each step. Taking in files like *{file_name}\_{run_number}.txt*, it outputs a single file *{file_name}\_avg.txt* which averages the values over all the different runs.

The total number of runs, range of mobility and graph initialization parameters can be set inside *aggregate_runs.py*. The path to the results folder also has to be set appropriately inside *aggregate_runs.py*.

-------------------------------------------------------------------

For creating plots to show how different values vary by change in mobility, the average results files (created using *aggregate_runs.py*) need to be aggregated for each value of mobility. This can be done by:

	python aggregate_vs_mobility.py

For each average results file (i.e., files ending with *\*avg.txt*) for a range of mobility specified by *mp* inside the python file, *aggregate_vs_mobility.py* aggregates the last row of each file into a new file, with one entry corresponding to each mobility value. The new results file name is *\*\_m\_\*_allm.txt*, where the average results file for each mobility value were specified by *\*\_m{mobility_probability}\_\*avg.txt*, with *{mobility_probability}* denoting the probability of mobility.

-------------------------------------------------------------------

For plots showing how different values vary by change in mobility, use:

	python plot_vs_mobility.py {graph_initialization} {type_of_plot}

where *{graph_initiliazation}* can take values from 0 to 4 as explained above, and *{type_of_plot}* takes values from 1 to 9 and creates different plots, some of which have been presented in the paper. The type of plots created for each option is explained in *plot_vs_mobility.py*.

For plotting a single simulation run (this could be an average run or a specific run number), use:

	python plot_run.py  {run_number} {mobility_probability} {graph_initialization} {type_of_plot}
	
where *{run_number}* can be set to avg if plotting average simulation run, and the rest of the command line arguments are the same as described above. An example of plotting a graph for the proportion of group-entitative vs. individual-entitative agents for mobility probability 0.05 for the average file where the graph is initialized to be empty is:

	python plot_run.py avg 0.05 0 1


-------------------------------------------------------------------

This section contains the functions of the other files in the source code that *main.py* uses while running a simulation.

- *globals.py*: initializes global variables for the simulation run. Can be used to set values such as the total iterations to run, the size of the grid, the payoffs in the game matrix, etc.
- *agent.py*: defines the agent type class. Agents can be either group-entitative or individual-entitative.
- *phases.py*: defines methods for each step in the evolutionary game-theoretic model, i.e., the immigration phase, game phase or interaction phase, reproduction phase, death phase, mobility phase.
- *torus.py*: defines Torus class which builds and maintains the torus grid network on which the agents reside.
- *two_player_game.py*: defines a TwoPlayerGame class which implements a two player game between two adjacent agents on the grid.
- *stats_files.py*: aggregates and saves the different statistics of each iteration in the output files.
- *utils.py*: contains some small helper functions which are used by the main program.

-------------------------------------------------------------------
