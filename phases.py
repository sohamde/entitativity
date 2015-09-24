import agent as ag
from torus import *
import sys
import random as rnd
rnd.seed()
from two_player_game import *
from utils import *


def init(opt):
	"""
	Creates and initializes agents and grid. Empty grid is initialized.
	"""

	agents = []     # initialize list of agents
	grid = Torus(g.n, g.n, g.neighborhood, g.reproduction_neighborhood)
	counts = g.stats.getCounts(agents)
	if opt == 0:
		return agents, grid, counts
	# populating grid with random agents at every spot
	emptySites = list(grid.get_empty_sites())   # getting empty spots in the grid
	tag = rnd.choice(g.tags)          # randomly choosing a specific tag (relevant for opt = 2,3,4
	for loc in emptySites:
		if opt == 1:    # random agent on each node of the grid
			immigrant = ag.spawnRandomAgent(g.tags, g.onlyEnt)
		elif opt == 2:  # group-entitative agent on each node of the grid, playing C with in-group and D with out-group
			immigrant = ag.spawnGroupEntAgent(tag, g.onlyEnt)
		elif opt == 3:  # group-entitative agent on each node of the grid, playing C with in-group and TFT with out-group
			immigrant = ag.spawnGroupTFTAgent(tag, g.onlyEnt)
		elif opt == 4:  # individual-entitative agent on each node of the grid, playing TFT
			immigrant = ag.spawnIndTFTAgent(tag, g.onlyEnt)
		else:
			print("invalid opt option")
			sys.exit(0)
		grid.place_agent(immigrant, loc)    # placing agent on grid location
		agents.append(immigrant)            # adding new agent to agent list
		g.agent_opponents[immigrant] = []     # adding new agent to agent_opponents dictionary
		g.no_games[immigrant] = 0.0           # adding new agent to no_games dictionary
	counts = g.stats.getCounts(agents)        # counting agents of different types and tags
	return agents, grid, counts


def immigration(agents, grid):
	##### immigration --- place immigrants with random traits on random site.
	emptySites = list(grid.get_empty_sites())
	randEmptySitesToPopulate = rnd.sample(emptySites,min(g.imRate,len(emptySites)))
	for loc in randEmptySitesToPopulate:
		immigrant = ag.spawnRandomAgent(g.tags, g.onlyEnt)
		grid.place_agent(immigrant, loc)
		agents.append(immigrant)
		g.agent_opponents[immigrant] = []
		g.no_games[immigrant] = 0.0
	return agents, grid


def interaction(agents, grid):
	##### interaction
	totalOutgroupInteractions = inCoops = inDefects = outCoops = outDefects = 0
	resetPTR(agents) # reset PTR of all agents to basePTR
	pairs = list()
	numInteractions = 0

	if g.PAIRALLNEIGHS == True:
		pairs = grid.get_all_neigh_agent_pairs()
		for agent1, agent2 in pairs:
			game = TwoPlayerGame(agent1, agent2, grid.get_neighbors(agent1), grid.get_neighbors(agent2), g.GAMEMATRIX)
			game.run(g.fullEnt,g.numIts)
			# update potential to reproduce
			agent1.ptr += game.get_payoffs()[agent1]
			agent2.ptr += game.get_payoffs()[agent2]

			# update dictionary keeping track of unique opponents of each agent
			if agent2 not in g.agent_opponents[agent1]:
				g.agent_opponents[agent1].append(agent2)
				g.agent_opponents[agent2].append(agent1)
			g.no_games[agent1] += 1.0
			g.no_games[agent2] += 1.0

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
		for agent in agents:
			# pick neighbor
			neighbors = grid.get_neighbors(agent)
			elligibleneighbors = [n for n in neighbors if n.games_played < g.numActs]
			while agent.games_played < g.numActs and elligibleneighbors:
				neighbor = rnd.choice(elligibleneighbors)
				#print "playing"
				game = TwoPlayerGame(agent, neighbor, grid.get_neighbors(agent),grid.get_neighbors(neighbor),g.GAMEMATRIX)
				game.run(g.fullEnt,g.numIts)
				numInteractions+=1
				# update potential to reproduce
				agent.ptr += game.get_payoffs()[agent]
				neighbor.ptr += game.get_payoffs()[neighbor]

				# update dictionary keeping track of unique opponents of each agent
				if neighbor not in g.agent_opponents[agent]:
					g.agent_opponents[agent].append(neighbor)
					g.agent_opponents[neighbor].append(agent)
				g.no_games[agent] += 1.0
				g.no_games[neighbor] += 1.0

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

			elligibleneighbors = [n for n in elligibleneighbors if n.games_played < g.numActs]

	for a in agents:
		a.games_played = 0

	return agents, grid, pairs, numInteractions, inCoops, inDefects, outCoops, outDefects, totalOutgroupInteractions


def reproduction(agents, grid, counts):
	##### reproduction
	rnd.shuffle(agents)

	agentsAdded = list()
	for agent in agents:
		# give agent chance (ptr) to clone into a random open adjacent spot, if it exists
		emptyAdjacent = [loc for loc in grid.reproductionneighborLocs[agent.gridlocation] if grid.agentMatrix[loc[0]][loc[1]] == None]
		if emptyAdjacent:
			if rnd.random() < normalizePtr(agent.ptr,g.minPosPay,g.maxPosPay):
				if g.keepGroupsEqual:
					if counts[agent.tag] < g.maxGroupSize:
						newAgent = agent.clone(g.tags, g.mu)
						grid.place_agent(newAgent, rnd.choice(emptyAdjacent))
						agentsAdded.append(newAgent)
						g.agent_opponents[newAgent] = []
						g.no_games[newAgent] = 0.0
				else:
					newAgent = agent.clone(g.tags, g.mu)
					grid.place_agent(newAgent, rnd.choice(emptyAdjacent))
					agentsAdded.append(newAgent)
					g.agent_opponents[newAgent] = []
					g.no_games[newAgent] = 0.0
	agents.extend(agentsAdded)

	return agents, grid, counts


def death(agents, grid):
	##### death
	for agent in agents:
		if rnd.random() < g.deathrate:
			agents.remove(agent)
			grid.remove_agent(agent) #******

			# updating dictionary and average number of unique opponents each agent plays
			g.avg_diff_agents = g.avg_diff_agents*(g.cnt_dead/(g.cnt_dead+1.0))+len(g.agent_opponents[agent])/(g.cnt_dead+1.0)
			if len(g.agent_opponents[agent]) > 0:
				g.avg_same = g.avg_same*(g.cnt_dead/(g.cnt_dead+1.0)) + (g.no_games[agent]/len(g.agent_opponents[agent]))/(g.cnt_dead+1.0)
				g.avg_same_gt_1 = g.avg_same_gt_1*(g.cnt_len_gt_0/(g.cnt_len_gt_0+1.0)) + (g.no_games[agent]/len(g.agent_opponents[agent]))/(g.cnt_len_gt_0+1.0)
				g.cnt_len_gt_0 += 1.0
			else:
				g.avg_same = g.avg_same*(g.cnt_dead/(g.cnt_dead+1.0))
			g.cnt_dead += 1.0
			del g.agent_opponents[agent]
			del g.no_games[agent]

	return agents, grid


def mobility(agents, grid):
	##### mobility
	if g.mobility:
		for agent in agents:
			if rnd.random() < g.mobility:

				bestEmptyLoc = agent.gridlocation
				bestNumSameTag = 0
				neighs = grid.get_neighbors(agent)
				for neigh in neighs:
					if neigh.tag == agent.tag:
						bestNumSameTag += 1

				if g.moveTowardOwn:

					if g.moveRange >= grid.nrows:
						locations = grid.get_empty_sites()
					else:
						locations = grid.get_empty_locs_in_range(agent.gridlocation, g.moveRange)
					rnd.shuffle(locations)
					for location in locations:
						neighsOfEmptySite = grid.get_neighbors_of_loc(location)
						if neighsOfEmptySite:
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
					if g.moveRange >= grid.nrows:
						posslocs = grid.get_empty_sites()
					else:
						posslocs = grid.get_empty_locs_in_range(agent.gridlocation, g.moveRange)
					if posslocs:
						moveToLoc = rnd.choice(posslocs)
						grid.move_agent(agent, moveToLoc)

	return agents, grid