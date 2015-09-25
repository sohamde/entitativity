## Agent for group conflict model
## These agents have a group-entitative/individual-entitative trait that determines whether they
## see others as individuals or group members.
## authors: soham de, patrick roos
## emails: (sohamde, roos) at cs umd edu

import random as rnd
from ordered_dict import *
import sys


class EntAgent:
	"""
	Group-entitative agent class
	"""

	def __init__(self, tag, inP, inQ, inI, outP, outQ, outI, gridloc=None):
		"""
		@param tag: the group tag of this agent
		@param gridloc: (x,y) tuple that gives location of this agent on grid
		@param 
					- p is the pure strategy if the opponent group cooperated in the last move against me
					- q is the pure strategy if the opponent group defected in the last move against me
					- i is the pure strategy to use the first time a new group is encountered (no history available)
					- since only pure strategies, p, q and i are either 0 (cooperate) or 1 (defect)
		"""
		self.tag = tag
		self.CorI = "ent"
	
		self.ptr = 0
		self.gridlocation = gridloc

		# strategy against in-group agents
		self.inP = inP
		self.inQ = inQ
		self.inI = inI

		# strategy against out-group agents
		self.outP = outP
		self.outQ = outQ
		self.outI = outI

		self.memory = {}    # will hold last move of group against agent {tag -> move}
		self.movesThisGen = list()
		self.reset()	 	# sets self.games_played to empty list
			
	def move(self, game, neighbors):
		"""Returns move in game (0 is cooperate, 1 is defect)."""

		opponent = game.opponents[self]

		rnd.shuffle(neighbors)
		# first see if opponent defected against any neighbors that are my tag
		for neigh in neighbors:
			if neigh.tag == self.tag:
				if opponent.tag in neigh.memory.keys():
					if neigh.memory[opponent.tag] == 1:
						if opponent.tag == self.tag:				
							return self.inQ
						else:
							return self.outQ

		# check if agent has encountered agent from opponent's group before
		if opponent.tag in self.memory.keys():
			if self.memory[opponent.tag] == 0:
				if opponent.tag == self.tag:
					return self.inP
				else:
					return self.outP 	
			else:
				if opponent.tag == self.tag:
					return self.inQ
				else:
					return self.outQ
		else:   # else return default action when no history is available
			if opponent.tag == self.tag:
				return self.inI
			else:
				return self.outI
		
	def clone(self, tags, mu):
		""" mutation phase """

		newTag = self.tag
		if rnd.random() < mu:
			newTag = rnd.choice(tags)
	
		newInP = self.inP
		if rnd.random() < mu:
			newInP = rnd.randint(0,1)

		newInQ = self.inQ
		if rnd.random() < mu:
			newInQ = rnd.randint(0,1)

		if rnd.random() < mu:
			newInI = rnd.randint(0,1)
		else:
			newInI = self.inI

		newOutP = self.outP
		if rnd.random() < mu:
			newOutP = rnd.randint(0,1)

		newOutQ = self.outQ
		if rnd.random() < mu:
			newOutQ = rnd.randint(0,1)

		if rnd.random() < mu:
			newOutI = rnd.randint(0,1)
		else:
			newOutI = self.outI
		
		return EntAgent(newTag, newInP, newInQ, newInI, newOutP, newOutQ, newOutI)	

	def record(self, game):
		"""Records the game played to history (games_played) and update memory."""

		opp = game.opponents[self]
		self.memory[opp.tag] = game.get_last_move(opp)
		self.movesThisGen.append(game.get_last_move(self))
		self.games_played += 1

	def reset(self):
		"""Resets history to empty."""

		self.games_played = 0
		self.memory = {}
		self.movesThisGen = list()
		

class IndAgent:
	"""
	Individual-entitative agent class
	"""

	def __init__(self, tag, p, q, i, gridloc=None):
		"""
		@param tag: the group tag of this agent
		@param gridloc: (x,y) tuple that gives location of this agent on grid
		@param 
					- p is the pure strategy if the opponent cooperated in the last move against me
					- q is the pure strategy if the opponent defected in the last move against me
					- i is the pure strategy to use the first time a new individual is encountered (no history available)
					- since only pure strategies, p and q are either 0 (cooperate) or 1 (defect)
		"""

		self.tag = tag
		self.CorI = "ind"

		self.ptr = 0
		self.gridlocation = gridloc

		# strategy bits
		self.p = p
		self.q = q
		self.i = i
	
		self.memory = OrderedDict()     # will hold last move of agent elf {agent -> move}
		self.movesThisGen = list()
		self.reset()	 			    # sets self.games_played to empty list
			
	def move(self, game, neighbors):
		"""Returns move in game (0 is cooperate, 1 is defect)."""

		opponent = game.opponents[self]

		# check if opponent encountered before
		if opponent in self.memory.keys():
			if self.memory[opponent] == 0:
				return self.p
			else:
				return self.q
		else:   # else return default action
			return self.i
			
	def clone(self, tags, mu):
		""" mutation phase """

		newTag = self.tag
		if rnd.random() < mu:
			newTag = rnd.choice(tags)
	
		newP = self.p
		if rnd.random() < mu:
			newP = rnd.randint(0,1)

		newQ = self.q
		if rnd.random() < mu:
			newQ = rnd.randint(0,1)

		if rnd.random() < mu:
			newI = rnd.randint(0,1)
		else:
			newI = self.i
		
		return IndAgent(newTag, newP, newQ, newI)	

	def record(self, game):
		"""Records the game played to history (games_played) and update memory."""

		opp = game.opponents[self]
		self.memory[opp] = game.get_last_move(opp)
		self.movesThisGen.append(game.get_last_move(self))
		if len(self.memory.keys()) > 10:
			self.memory.popitem()
		self.games_played += 1

	def reset(self):
		"""Resets history to empty."""

		self.games_played = 0
		self.memory = {}
		self.movesThisGen = list()


def spawnRandomAgent(tags, onlyEnt = False):
	""" Creates an agent with random attributes. """

	if onlyEnt:
		return EntAgent(rnd.choice(tags), rnd.randint(0,1), rnd.randint(0,1),\
				 rnd.randint(0,1), rnd.randint(0,1), rnd.randint(0,1), rnd.randint(0,1))
	else:		
		if rnd.random() < 0.5:
			return EntAgent(rnd.choice(tags), rnd.randint(0,1), rnd.randint(0,1),\
				 rnd.randint(0,1), rnd.randint(0,1), rnd.randint(0,1), rnd.randint(0,1))
		else:
			return IndAgent(rnd.choice(tags), rnd.randint(0,1), rnd.randint(0,1), rnd.randint(0,1))


def spawnGroupEntAgent(tag, onlyEnt = False):
	""" Creates a group-entitative agent of a specific tag, playing C for in-group and D for out-group agents"""
	return EntAgent(tag, 0, 0, 0, 1, 1, 1)


def spawnGroupTFTAgent(tag, onlyEnt = False):
	""" Creates an group-entitative agent of specific tag and playing C with in-group and TFT with out-group. """
	return EntAgent(tag, 0, 0, 0, 0, 1, 1)


def spawnIndTFTAgent(tag, onlyEnt = False):
	""" Creates an individual-entitative agent of specific tag and playing TFT. """
	if onlyEnt:
		print "spawnIndEntAgent not possible with onlyEnt set to True"
		sys.exit(0)
	else:
		return IndAgent(tag, 0, 1, 0)
