import globals as g
import agent as ag
from torus import *
import sys
import random as rnd
rnd.seed()


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
