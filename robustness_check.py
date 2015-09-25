## Robustness check for Group-Entitativity & Individual-Entitativity vs Mobility simulator
## No birth, death or reproduction phase. Nodes always have agents on them. Agent updates action according to Fermi rule.
##
## USAGE: python main.py run_no mobility_probability
## where run_no is an integer and mobility_probability is a float between 0 and 1
##
## authors: soham de, patrick roos
## emails: (sohamde, roos) at cs umd edu

from phases import *


def step(agents, grid, counts):
	"""
	Steps through evolutionary phases using methods in phases.py: interaction, reproduction, mobility
	"""

	# interaction phase
	agents, grid, pairs, numInteractions, inCoops, inDefects, outCoops, outDefects, totalOutgroupInteractions = interaction(agents, grid)

	# reproduction phase
	agents, grid, counts = reproduction_fermi(agents, grid, counts)

	# mobility phase
	agents, grid = mobility_switch_positions(agents, grid)

	# calculate statistics for result files: percentage of interactions with out-group agents
	totalOutgroupInteractionPerc = 0
	if g.PAIRALLNEIGHS == True:
		if len(pairs) > 0:
			totalOutgroupInteractionPerc = totalOutgroupInteractions/float(len(pairs))
	else:
		if numInteractions > 0:
			totalOutgroupInteractionPerc = totalOutgroupInteractions/float(numInteractions)

	# calculate statistics for result files: percentage of agents alive, clustering coefficient, etc
	alive_proportion = float((grid.nrows*grid.ncols) - len(grid.emptySites))/float(grid.nrows*grid.ncols)
	clustering_coeff = empty_ignore(agents,grid)
	diff_games_list = [g.avg_diff_agents, g.avg_same, g.avg_same_gt_1]

	# calculating statistics and writing to output result files
	counts = g.stats.step(agents, inCoops, inDefects, outCoops, outDefects, totalOutgroupInteractionPerc, alive_proportion, clustering_coeff, diff_games_list)

	return agents, grid, counts


if __name__ == "__main__":

	try:
		time = 0
		# initialize grid
		agents_list, grid_object, stat_counts = init(g.grid_initialization)
		print "initialized."

		# for each iteration
		while time < g.maxTime:
			# run different evolutionary phases
			agents_list, grid_object, stat_counts = step(agents_list, grid_object, stat_counts)
			if time%10 == 0:
				print "time:", time

			# update iteration count
			time += 1

	finally:
		# close output result files
		g.stats.close_files()
