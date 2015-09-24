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

import random as rnd
rnd.seed()
import sys
import agent as ag
import stats_files as st
from torus import *
from two_player_game import *
from triplet_clustering import empty_ignore


######################### MAIN ENVIRONMENT PARAMETERS ######################### 
nTags = 4				# number of tags in environment
tags = xrange(nTags)    # list of tags (1,2,..., nTags-1)
n = 50      # grid is nxn
maxTime = 30000 # end after maxTime timesteps
numIts = 1		# number of game iterations to play in each pairing

# agent can interact and reproduce into only the top, left, right and bottom spots on the grid
reproduction_neighborhood = [(-1,0), (0,-1), (0,+1), (+1,0)]
neighborhood = [(-1,0),	(0,-1), (0,+1), (+1,0)]

# to calculate average number of different agents an agent meets during it's lifetime
cnt_dead = 0.0  # count of the number of agents that have died
cnt_len_gt_0 = 0.0  # count of the number of agents that have died playing at least one game
avg_diff_agents = 0.0  # average number of different agents each agent meets
agent_opponents = {}  # for each agent, list of unique agents it has played a game against
avg_same = 0.0  # average number of games an agent plays with the same agent
avg_same_gt_1 = 0.0  # considering only agents which have played at least one game
no_games = {}  # number of games each agent plays

PAIRALLNEIGHS = True    # whether to pair all neighbors or do sampling scheme
numActs = 4				# number of interactions to strive for (and max limit) if sampling scheme is used
basePTR = 0.12	        # base potential to reproduce (same as in Hammond and Axelrod, 2006)

cluster = 0     # 1 if running on Deepthought2 cluster, 0 otherwise
if cluster == 0:
	results_folder = './results/'
else:
	results_folder = '/lustre/sohamde/Entitativity/src/results/'

# game to play
hawkdove = False
if hawkdove:
	b = 0.04
	c = 0.06
	GAMEMATRIX = [ [ ( b/2.0, b/2.0 ), (0, b) ] , [ (b, 0), ( (b-c)/2.0, (b-c)/2.0 )] ]
	maxPosPay = b/2.0*numActs
	minPosPay = 0
else:
	b = 0.03        # benefit of cooperation (same as in Hammond and Axelrod, 2006)
	c = 0.01        # cost of cooperation (same as in Hammond and Axelrod, 2006)
	GAMEMATRIX = [ [(b-c,b-c),(-c,b)] , [(b,-c),(0,0)] ]
	maxPosPay = basePTR+b*numActs*2     # highest possible payoff
	minPosPay = basePTR-c*numActs*2     # lowest possible payoff

# probability of an agent moving to a random empty spot in the grid
mobility = float(sys.argv[2])

imRate = 1		    # immigration rate - how many immigrants to add each step (same as in Hammond and Axelrod, 2006)
mu = 0.05		    # mutation rate (same as in Hammond and Axelrod, 2006)
deathrate = 0.10    # probability of death (same as in Hammond and Axelrod, 2006)

onlyEnt = False     # whether to only use group-entitative agents
keepGroupsEqual = False     # whether to set a max limit on group size at equal percentage of population
maxGroupSize = n*n/nTags    # only relevant if keepGroupsEqual is set to True
fullEnt = False             # whether to have group-entitative agents be fully so (harm on neighbor is harm on self)
normPtr = False
moveTowardOwn = False
moveRange = n

# specify grid initialization; 0: empty, 1: filled random agents, 2: group ent, C with in-group, D with out-group
# 3: group ent, C with in-group and TFT with out-group, 4: individual-entitative, TFT
grid_initialization = 4     # Hammond and Axelrod initialized with empty grid, ie grid_initialization = 0

# saving run ID
if hawkdove:
	runId = "HD_v"+str(b)+"c"+str(c)+"_g"+str(nTags)+"_i"+str(numIts)+"_m"+str(mobility)+"_mr"+str(moveRange)+"_numneighs"+str(len(neighborhood))+"_"
else:
	runId = "PD_b"+str(b)+"c"+str(c)+"_g"+str(nTags)+"_i"+str(numIts)+"_m"+str(mobility)+"_mr"+str(moveRange)+"_numneighs"+str(len(neighborhood))+"_init"+str(grid_initialization)+"_"
if PAIRALLNEIGHS:
	runId+="pairallneighs_"
else:
	runId += "samplePair"+str(numActs)+"_"
if onlyEnt:
	runId += "onlyEnt_"
if keepGroupsEqual:
	runId += "keepGroupsEq"+str(maxGroupSize)+"_"
if fullEnt:
	runId += "fullEnt_"
if normPtr:
	runId += "normPtr_"
if moveTowardOwn:
	runId += "moveTowardOwn_"
runId += str(sys.argv[1])

stats = st.Stats(tags, runId, results_folder) # to record statistics, e.g. counts over time


# ~~~~~ MAIN FUNCTIONS: INIT, DRAW, STEP ~~~~~
def init(opt):
	"""
	Creates and initializes agents and grid. Empty grid is initialized.
	"""
	global agent_opponents, no_games
	agents = []     # initialize list of agents
	grid = Torus(n, n, neighborhood, reproduction_neighborhood)
	counts = stats.getCounts(agents)
	if opt == 0:
		return agents, grid, counts
	# populating grid with random agents at every spot
	emptySites = list(grid.get_empty_sites())   # getting empty spots in the grid
	tag = rnd.choice(tags)          # randomly choosing a specific tag (relevant for opt = 2,3,4
	for loc in emptySites:
		if opt == 1:    # random agent on each node of the grid
			immigrant = ag.spawnRandomAgent(tags, onlyEnt)
		elif opt == 2:  # group-entitative agent on each node of the grid, playing C with in-group and D with out-group
			immigrant = ag.spawnGroupEntAgent(tag, onlyEnt)
		elif opt == 3:  # group-entitative agent on each node of the grid, playing C with in-group and TFT with out-group
			immigrant = ag.spawnGroupTFTAgent(tag, onlyEnt)
		elif opt == 4:  # individual-entitative agent on each node of the grid, playing TFT
			immigrant = ag.spawnIndTFTAgent(tag, onlyEnt)
		else:
			print("invalid opt option")
			sys.exit(0)
		grid.place_agent(immigrant, loc)    # placing agent on grid location
		agents.append(immigrant)            # adding new agent to agent list
		agent_opponents[immigrant] = []     # adding new agent to agent_opponents dictionary
		no_games[immigrant] = 0.0           # adding new agent to no_games dictionary
	counts = stats.getCounts(agents)        # counting agents of different types and tags
	return agents, grid, counts


def step(agents, grid, counts):
	"""
	Steps through time period stages by Hammond and Axelrod (2006):
	- immigration, interaction, reproduction, death, mobility
	"""

	global agent_opponents, cnt_dead, avg_diff_agents, avg_same, no_games, cnt_len_gt_0, avg_same_gt_1

	##### immigration --- place immigrants with random traits on random site.
	emptySites = list(grid.get_empty_sites())
	randEmptySitesToPopulate = rnd.sample(emptySites,min(imRate,len(emptySites)))
	for loc in randEmptySitesToPopulate:
		immigrant = ag.spawnRandomAgent(tags, onlyEnt)
		grid.place_agent(immigrant, loc)
		agents.append(immigrant)
		agent_opponents[immigrant] = []
		no_games[immigrant] = 0.0

	##### interaction
	totalOutgroupInteractions = inCoops = inDefects = outCoops = outDefects = 0
	resetPTR(agents) # reset PTR of all agents to basePTR

	if PAIRALLNEIGHS == True:
		pairs = grid.get_all_neigh_agent_pairs()
		#print "pairs:",pairs
		for agent1, agent2 in pairs:
			game = TwoPlayerGame(agent1, agent2, grid.get_neighbors(agent1), grid.get_neighbors(agent2), GAMEMATRIX)
			game.run(fullEnt,numIts)
			# update potential to reproduce
			agent1.ptr += game.get_payoffs()[agent1]
			agent2.ptr += game.get_payoffs()[agent2]

			# update dictionary keeping track of unique opponents of each agent
			if agent2 not in agent_opponents[agent1]:
				agent_opponents[agent1].append(agent2)
				agent_opponents[agent2].append(agent1)
			no_games[agent1] += 1.0
			no_games[agent2] += 1.0

			coops, defects = game.get_coops_defects(agent1)
			coops2, defects2 = game.get_coops_defects(agent2)
			if agent1.tag == agent2.tag:
				totalOutgroupInteractions += 1
				inCoops += coops
				inDefects += defects
				inCoops += coops2
				inDefects += defects2
			else:
				outCoops += coops
				outDefects += defects
				outCoops += coops2
				outDefects += defects2


	else:
		numInteractions = 0
		for agent in agents:
			# pick nieghbor
			neighbors = grid.get_neighbors(agent)
			elligibleneighbors = [n for n in neighbors if n.games_played < numActs]
			while agent.games_played < numActs and elligibleneighbors:
				neighbor = rnd.choice(elligibleneighbors)
				#print "playing"
				game = TwoPlayerGame(agent, neighbor, grid.get_neighbors(agent),grid.get_neighbors(neighbor),GAMEMATRIX)
				game.run(fullEnt,numIts)
				numInteractions+=1
				# update potential to reproduce
				agent.ptr += game.get_payoffs()[agent]
				neighbor.ptr += game.get_payoffs()[neighbor]

				# update dictionary keeping track of unique opponents of each agent
				if neighbor not in agent_opponents[agent]:
					agent_opponents[agent].append(neighbor)
					agent_opponents[neighbor].append(agent)
				no_games[agent] += 1.0
				no_games[neighbor] += 1.0

				coops, defects = game.get_coops_defects(agent)
				coops2, defects2 = game.get_coops_defects(neighbor)
				if agent.tag == neighbor.tag:
					totalOutgroupInteractions += 1
					inCoops += coops
					inDefects += defects
					inCoops += coops2
					inDefects += defects2
				else:
					outCoops += coops
					outDefects += defects
					outCoops += coops2
					outDefects += defects2

			elligibleneighbors = [n for n in elligibleneighbors if n.games_played < numActs]

	for a in agents:
		#print "neighbors:",len(grid.get_neighbors(a))
		#print "played:",a.games_played
		a.games_played = 0
		#print "ptr:",a.ptr

	##### reproduction
	rnd.shuffle(agents)

	agentsAdded = list()
	for agent in agents:
		# give agent chance (ptr) to clone into a random open adjacent spot, if it exists
		emptyAdjacent = [loc for loc in grid.reproductionneighborLocs[agent.gridlocation] if grid.agentMatrix[loc[0]][loc[1]] == None]
		if emptyAdjacent:
			#print "agent ptr: ",agent.ptr
			#print "agent norm ptr: ", normalizePtr(agent.ptr,minPosPay,maxPosPay)
			if rnd.random() < normalizePtr(agent.ptr,minPosPay,maxPosPay):
				if keepGroupsEqual:
					if counts[agent.tag] < maxGroupSize:
						newAgent = agent.clone(tags, mu)
						grid.place_agent(newAgent, rnd.choice(emptyAdjacent))
						agentsAdded.append(newAgent)
						agent_opponents[newAgent] = []
						no_games[newAgent] = 0.0
				else:
					newAgent = agent.clone(tags, mu)
					grid.place_agent(newAgent, rnd.choice(emptyAdjacent))
					agentsAdded.append(newAgent)
					agent_opponents[newAgent] = []
					no_games[newAgent] = 0.0
	agents.extend(agentsAdded)

	##### death
	for agent in agents:
		if rnd.random() < deathrate:
			agents.remove(agent)
			grid.remove_agent(agent) #******

			# updating dictionary and average number of unique opponents each agent plays
			avg_diff_agents = avg_diff_agents*(cnt_dead/(cnt_dead+1.0))+len(agent_opponents[agent])/(cnt_dead+1.0)
			if len(agent_opponents[agent]) > 0:
				avg_same = avg_same*(cnt_dead/(cnt_dead+1.0)) + (no_games[agent]/len(agent_opponents[agent]))/(cnt_dead+1.0)
				avg_same_gt_1 = avg_same_gt_1*(cnt_len_gt_0/(cnt_len_gt_0+1.0)) + (no_games[agent]/len(agent_opponents[agent]))/(cnt_len_gt_0+1.0)
				cnt_len_gt_0 += 1.0
			else:
				avg_same = avg_same*(cnt_dead/(cnt_dead+1.0))
			cnt_dead += 1.0
			del agent_opponents[agent]
			del no_games[agent]

	##### mobility
	if mobility:
		for agent in agents:
			if rnd.random() < mobility:

				bestEmptyLoc = agent.gridlocation
				bestNumSameTag = 0
				neighs = grid.get_neighbors(agent)
				for neigh in neighs:
					if neigh.tag == agent.tag:
						bestNumSameTag += 1

				if moveTowardOwn:

					if moveRange >= grid.nrows:
						locations = grid.get_empty_sites()
					else:
						locations = grid.get_empty_locs_in_range(agent.gridlocation, moveRange)
					rnd.shuffle(locations)
					for location in locations:
						neighsOfEmptySite = grid.get_neighbors_of_loc(location)
						if neighsOfEmptySite:
							#print "neighsOfEmptySite:",neighsOfEmptySite
							numSameTag = 0
							for neigh in neighsOfEmptySite:
								if neigh.tag == agent.tag:
									numSameTag += 1
							if bestNumSameTag < numSameTag:
								bestNumSameTag = numSameTag
								bestEmptyLoc = location
					grid.move_agent(agent, bestEmptyLoc)
				else:
					# move to random open spot
					if moveRange >= grid.nrows:
						posslocs = grid.get_empty_sites()
					else:
						posslocs = grid.get_empty_locs_in_range(agent.gridlocation, moveRange)
					if posslocs:
						moveToLoc = rnd.choice(posslocs)
						grid.move_agent(agent, moveToLoc)

	totalOutgroupInteractionPerc = 0
	if PAIRALLNEIGHS == True:
		if len(pairs) > 0:
			totalOutgroupInteractionPerc = totalOutgroupInteractions/float(len(pairs))
	else:
		if numInteractions > 0:
			totalOutgroupInteractionPerc = totalOutgroupInteractions/float(numInteractions)

	counts = stats.step(agents, inCoops, inDefects, outCoops, outDefects, totalOutgroupInteractionPerc)

	clustering_coeff = empty_ignore(agents,grid)
	coeff_file.write(str(clustering_coeff)+"\n")

	alive_proportion = float((grid.nrows*grid.ncols) - len(grid.emptySites))/float(grid.nrows*grid.ncols)
	alive_file.write(str(alive_proportion)+"\n")
	diff_games_file.write(str(avg_diff_agents)+","+str(avg_same)+","+str(avg_same_gt_1)+"\n")

	return agents, grid, counts


# ~~~~~ HELPER FUNCTIONS ~~~~~
def normalizePtr(ptr,minPosPay,maxPosPay):
	# Normalizes ptr so that the possible range is [0,1].

	if normPtr:
		return (float(ptr) - minPosPay)/float((maxPosPay - minPosPay))
	else:
		return ptr

def resetPTR(agents):
	for agent in agents:
		agent.ptr = basePTR

def setTagMatrix(population,M):
	for agent in population:
		(x,y) = agent.gridlocation
		M[x][y] = agent.tag


########################################################################################################
def main():

	try:
		time = 0
		agents, grid, counts = init(grid_initialization)
		print "initialized."
		while time < maxTime:
			agents, grid, counts = step(agents, grid, counts)
			if time%10 == 0:
				print "time:", time
			time += 1
	finally:
		stats.close_files()
		coeff_file.close()
		alive_file.close()
		diff_games_file.close()

# run simulation using pyxcsimulator
coeff_file = open(results_folder+"coeff_"+str(runId)+".txt",'wb')
coeff_file.write("clustering_coefficient\n")
alive_file = open(results_folder+"alive_"+str(runId)+".txt","wb")
alive_file.write("alive_proportion\n")
diff_games_file = open(results_folder+"diff_games__"+str(runId)+".txt","wb")
diff_games_file.write("no_unique_games,no_games_same_agent,no_games_same_agent_gt_1\n")
main()



