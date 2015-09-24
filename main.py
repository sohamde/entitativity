# ###############################
# main.py
#
# *** Group-Entitativity vs Individual-Entitativity simulator. ***
#
# USAGE:	
# - use main() to run simulation
# - or pass init(), draw(), and step() to the pycx simulator GUI and run the simulation in GUI
#
# @author: Soham De, Patrick Roos
# @version: sep-2015
# ###############################

from triplet_clustering import empty_ignore
from phases import *


def step(agents, grid, counts):
	"""
	Steps through time period stages by Hammond and Axelrod (2006):
	- immigration, interaction, reproduction, death, mobility
	"""

	agents, grid = immigration(agents, grid)

	agents, grid, pairs, numInteractions, inCoops, inDefects, outCoops, outDefects, totalOutgroupInteractions = interaction(agents, grid)

	agents, grid, counts = reproduction(agents, grid, counts)

	agents, grid = death(agents, grid)

	agents, grid = mobility(agents, grid)

	totalOutgroupInteractionPerc = 0
	if g.PAIRALLNEIGHS == True:
		if len(pairs) > 0:
			totalOutgroupInteractionPerc = totalOutgroupInteractions/float(len(pairs))
	else:
		if numInteractions > 0:
			totalOutgroupInteractionPerc = totalOutgroupInteractions/float(numInteractions)

	counts = g.stats.step(agents, inCoops, inDefects, outCoops, outDefects, totalOutgroupInteractionPerc)

	clustering_coeff = empty_ignore(agents,grid)
	coeff_file.write(str(clustering_coeff)+"\n")

	alive_proportion = float((grid.nrows*grid.ncols) - len(grid.emptySites))/float(grid.nrows*grid.ncols)
	alive_file.write(str(alive_proportion)+"\n")
	diff_games_file.write(str(g.avg_diff_agents)+","+str(g.avg_same)+","+str(g.avg_same_gt_1)+"\n")

	return agents, grid, counts


########################################################################################################
def main():

	try:
		time = 0
		agents, grid, counts = init(g.grid_initialization)
		print "initialized."
		while time < g.maxTime:
			agents, grid, counts = step(agents, grid, counts)
			if time%10 == 0:
				print "time:", time
			time += 1
	finally:
		g.stats.close_files()
		coeff_file.close()
		alive_file.close()
		diff_games_file.close()

# run simulation using pyxcsimulator
coeff_file = open(g.results_folder+"coeff_"+str(g.runId)+".txt",'wb')
coeff_file.write("clustering_coefficient\n")
alive_file = open(g.results_folder+"alive_"+str(g.runId)+".txt","wb")
alive_file.write("alive_proportion\n")
diff_games_file = open(g.results_folder+"diff_games__"+str(g.runId)+".txt","wb")
diff_games_file.write("no_unique_games,no_games_same_agent,no_games_same_agent_gt_1\n")
main()

