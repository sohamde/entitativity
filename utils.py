## utils.py
##
## Various helper methods.
##
## author: Patrick Roos (roos@cs.umd.edu)
## 


import random, math
from itertools import izip
import globals as g
# from collections import defaultdict


# ~~~~~ HELPER FUNCTIONS ~~~~~
def normalizePtr(ptr,minPosPay,maxPosPay):
	# Normalizes ptr so that the possible range is [0,1].

	if g.normPtr:
		return (float(ptr) - minPosPay)/float((maxPosPay - minPosPay))
	else:
		return ptr


def resetPTR(agents):
	for agent in agents:
		agent.ptr = g.basePTR


def setTagMatrix(population,M):
	for agent in population:
		(x,y) = agent.gridlocation
		M[x][y] = agent.tag


def scaleToFitness(unscaledList, w=0.5):
	"""
	scales unscaledList that holds payoffs to a range of fitnesses between 0 and 1 under selection pressure w.
	0 <= w <= 1, if w is 0 then there is no selection pressure based on unscaledList's values and the 
	returned list has all equal values. if w = 1 the payoffs are fitness, the lowest values 
	are all mapped to 0 (generally this is undesirable because any payoffs that are the min have 0 chance 
	of reproducing)
	"""

	minimum = min(unscaledList)
	maximum = max(unscaledList)

	#print "pay list:\n",unscaledList
	maxDiff = maximum - minimum
	#print "**************************** maxDiff",maxDiff
	if maxDiff != 0:
		scaledList = [(v - minimum)/(1.0*maxDiff) for v in unscaledList]
	else:
		scaledList = [0]*len(unscaledList)

	#print "scaled list:\n",scaledList
	fitnessList = [1 - w + w*p for p in scaledList]  # w = 0 neutral drift, w = 1 payoff = fitness

	#print "fitness list:\n",fitnessList
	return fitnessList

def choose_with_probabilities(choices, relLikelihoods, N=1):
	""" 
	Returns a list of values chosen from choices with certain likelihoods.
	
	@param choices		  - a list holding values to choose from
	@param relLikelihoods - a list holding the relative 'likelihoods'  with which each choice is chosen, 
							if one value is twice as much as another, it is chosen with twice as much probability.
	@param N			  - how many values to return from choices
	"""

	total = 0
	cumProbs = list()
	for p in relLikelihoods:
		total += p
		cumProbs.append(total)

# 	print "cumProbs",cumProbs
	toRtn = list()

	for j in range(N):
		cut = total*random.random()
		#print "cut",cut
		i = 0
		while cumProbs[i] < cut:
			i+=1
		# now i is index of choice to choose
		#print "i",i
		toRtn.append(choices[i])

	return toRtn

def transpose(seqseq):
	"""Return transpose of `seqseq`."""
	return zip(*seqseq)

def mean(seq):
	"""Return mean of values in `seq`."""
	n = len(seq)
	return sum(seq)/float(n)

def topscore_strategies(player):
	"""
	Return list of the best strategies (producing maximum payoff over player.games_played)
	out of all the strategies the player has encountered (self and list of players_played).
	"""
	best_types = [player.strategy]
	best_payoff = player.get_payoff()
	
	for opponent in player.players_played:
		payoff = opponent.get_payoff()
		if payoff > best_payoff:
			best_payoff = payoff
			best_types = [opponent.strategy]
		elif payoff == best_payoff:
			best_types.append(opponent.strategy)
	
	return best_types

def maxmin_playertypes(player):
	"""Return list of best (maxmin payoff) strategies."""
	# initialize mapping (strategy -> payoffs)
	pt2po = dict()
	# find minimum payoff for each encountered strategy
	pt2po[ player.playertype ] = player.get_payoff()
	for n in player.get_neighbors():
		pt, po = n.strategy, n.get_payoff()
		try:
			if pt2po[pt] > po:
				pt2po[pt] = po
		except KeyError:
			pt2po[pt] = po
	
	# find best playertype (max of minimum payoffs)
	maxmin = max( pt2po.itervalues() )
	best_strategies = [ pt for pt in pt2po if pt2po[pt]==maxmin ]
	
	return best_strategies

def random_pairs_of(players):
	"""Return all of players as random pairs."""
	# copy player list
	players = list( players )
	# shuffle the new player list in place
	random.shuffle(players)
	# yield the shuffled players, 2 at a time
	player_iter = iter(players)
	return izip(player_iter, player_iter)

def compute_neighbors(player, grid):
	"""Return neighbors of `player` on `grid`."""
	player_row, player_col = player.gridlocation
	nrows, ncols = grid.nrows, grid.ncols
	players2d = grid.players2d
	# initialize list of neighbors
	neighbors = list()
	# append all neighbors to list
	for offset in grid.neighborhood:
		dc, dr = offset		 #note: x,y neighborhood
		r = (player_row + dr) % nrows
		c = (player_col + dc) % ncols
		neighbor = players2d[r][c]
		neighbors.append(neighbor)
	return neighbors

def countTags(players):
	"""Return map (tag -> count) for `players`."""
	#Had to change for compatibility with condor
	tag_counts = {}
# 	tag_counts = defaultdict(int) #empty dictionary, default count is 0
	for player in players:
		if player.tag in tag_counts.keys():
			tag_counts[ player.tag ] += 1
		else:
			tag_counts[player.tag] = 1
	return tag_counts

##### FUNCTIONS FOR LOTTERIES  ######

def getLotteriesStats(lotteries):
	"""
	Returns a list of expected utilities (eu) and a list of variances for each lottery in lotteries, indeces correspond.
	E.g. utils[1] is the eu of the lottery at lotteries[1]
	"""

	# lets get the EUs and variance for all the lottery choices
	utils = list()
	vars = list()
	for lottery in lotteries:
		eu = getLotteryEU(lottery)
		utils.append(eu)
		vars.append(getLotteryVar(lottery, eu))

	return (utils, vars)
 

def getLotteryEU(lottery):
	"""
	Computes expected utility of given lottery.
	lottery = [(p1,O1), (p2,O2), ..., (pn,On)]
	"""
	util = 0
	for el in lottery:
		prob = el[0]
		outcom = el[1]
		util += prob*outcom

	return util

def getLotteryVar(lottery, eu):
	"""
	Computes variance of lottery. var = sum(p_i*(v_i-mu)^2)
	"""
	l = len(lottery)
	p = [lottery[i][0] for i in range(l)]
	v = [lottery[i][1] for i in range(l)]

	var = sum(p[i]*math.pow(v[i]-eu,2) for i in range(l))
		
	return var

def printAvgPmapOfTags(population, tags):
		for group in tags:
			groupMembers = filter(lambda a: a.tag==group, population)
			
			if len(groupMembers) > 0:
				print "Avg pMap of ",group,": "
				angerMap = getAvgAnger(groupMembers)
				s=""
				for k in angerMap:
					s+= " {0}: {1}".format(k, angerMap[k])			 
				print s
	
def getAvgAnger(agents):
	avgAngerMap = {}
	for tribe in agents[0].pMap.keys():
		avgAngerMap[tribe]=0

	for agent in agents:
		for tribe in agent.pMap.keys():
			avgAngerMap[tribe] = avgAngerMap[tribe]+agent.pMap[tribe]
	
	for tribe in agents[0].pMap.keys():
		avgAngerMap[tribe]=avgAngerMap[tribe]/len(agents)

	
	return avgAngerMap


### FUNCTIONS FOR POPULATIONS ###
def countAgentTypes(population):
	"""
	Return map (player.type -> frequency) for players in population.
	"""
	typeCounts = {}
# 	typeCounts = defaultdict(int) #empty dictionary, default count is 0
	for agent in population:
		if agent.type in typeCounts.keys():
			typeCounts[ agent.type ] += 1
		else:
			typeCounts[agent.type] = 1
		
	return typeCounts

def getPlayerTypePayoffs(players):
	"""Returns map (player_type -> total_payoff) for players. total_payoff is the sum of all payoffs received by all players of the corresponding player type."""
	
	playerTypePayoffs = {}
# 	playerTypePayoffs = defaultdict(int) #empty dictionary, default count is 0
	for player in players:
		
		#player.printGamesPlayedSummary()
		#print "games played: "+str(len(player.games_played))
		playerPayoff = player.total_payoff() # sum of payoffs of all games played for this player
		if player.type in playerTypePayoffs.keys():
			playerTypePayoffs[player.type] += playerPayoff # add to the corresponding player_type total payoff
		else:
			playerTypePayoffs[player.type] = playerPayoff
		
	return playerTypePayoffs   


def getPlayerTypeFitness(players):
	"""Returns map (player_type -> fitness) for players. fitness is player.fit"""
	
	playerTypePayoffs = {}	
# 	playerTypePayoffs = defaultdict(int) #empty dictionary, default count is 0
	for player in players:
		playerPayoff = player.fit
		if player.type in playerTypePayoffs.keys():
			playerTypePayoffs[player.type] += playerPayoff # add to the corresponding player_type total payoff
		else:
			playerTypePayoffs[player.type] = playerPayoff
	return playerTypePayoffs   



### PRINTING FUNCTIONS ###	
def printPopulationFreqs(pop_frequency_log):
	"""
	Prints population type counts (full history).
	"""
	playerTypes = pop_frequency_log[0].keys()
	print "\nPopulation:"
	for pt in playerTypes:
		print "%5s" %pt,
	print
	
	for i in range(len(pop_frequency_log)):
		for pt in playerTypes:
			print "%5d" %pop_frequency_log[i].get(pt, 0),
		print

def printCurrentPopulationFreqs(pop_frequency_log):
	frequencies = pop_frequency_log[-1] # get current (latest) freqs
	print "curr pop freqs:",
	for t in frequencies.keys():
		print "%s: %d" %(t, frequencies.get(t, 0)),

	print ""

def printPlayerTypeFitness(population):
	
	playerTypePayoffs = getPlayerTypeFitness(population)
	print "\n  Total Payoffs:"
	a = playerTypePayoffs.keys()
	for t in a:
		print "%10s" %t,
	print
	for t in a:
		print "%10d" %playerTypePayoffs.get(t, 0),
	print

	  
def printPlayerTypeTotalPayoffs(population):
	
	playerTypePayoffs = getPlayerTypePayoffs(population)
	print "\n  Total Payoffs:"
	a = playerTypePayoffs.keys()
	for t in a:
		print "%10s" %t,
	print
	for t in a:
		print "%10d" %playerTypePayoffs.get(t, 0),
	print

def printLotteries(lotteries):
	
	#pr('Lotteries created...\n')
	for lottery in lotteries:
		print "\t---\n\tlottery:"
		print '\t\tchoice 0: %s' %lottery[0]
		print '\t\tchoice 1: %s' %lottery[1]


def scaletriple(t):
		#scales triple t to sum to 1 
		s = sum(t)
		
		for n in range(0,len(t)):
			t[n] = t[n]/(s*1.0)
		return t
