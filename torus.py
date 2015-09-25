## Torus class to facilitate a grid environment on which agents interact.
## authors: soham de, patrick roos
## emails: (sohamde, roos) at cs umd edu


class Torus:
	"""
	Torus class to facilitate a grid environment on which agents interact.
	"""
	def __init__(self, nrows, ncols, neighborhood, reproductionneighborhood):
		"""
		Creates a grid torus specifying grid neighborhoods and reproduction neighborhoods for each location
		"""
		self.nrows, self.ncols = nrows, ncols
		self.neighborhood = neighborhood # list of tuples of x,y-offsets (relative to any grid location).
		self.reproductionneighborhood = reproductionneighborhood # list of tuples of x,y-offsets (relative to any grid location).
		self.agentMatrix = [[None]*ncols for i in range(nrows)] # ncols x nrows matrix that has agent or None at each location
		
		self.emptySites = [(i,j) for i in range(nrows) for j in range(ncols)]
		self.allSites = [(i,j) for i in range(nrows) for j in range(ncols)]

		# for each location (x,y) key will hold neighboring locations as list
		self.neighborLocs = {}
		for i in range(self.nrows):
			for j in range(self.ncols):
				neighLocs = list()
				for offset in self.neighborhood:
					dc, dr = offset		 #note: x,y neighborhood
					r = (i + dr) % nrows
					c = (j + dc) % ncols
					neighLocs.append((r,c))
				self.neighborLocs[(i,j)] = neighLocs

		# for each location (x,y) key will hold reproduction neighborhoods as list
		self.reproductionneighborLocs = {}
		for i in range(self.nrows):
			for j in range(self.ncols):
				neighLocs = list()
				for offset in self.neighborhood:
					dc, dr = offset		 #note: x,y neighborhood
					r = (i + dr) % nrows
					c = (j + dc) % ncols
					neighLocs.append((r,c))
				self.reproductionneighborLocs[(i,j)] = neighLocs

	def place_agent(self, agent, (x,y)):
		""" Places agent on grid at (x,y). """
		agent.gridlocation = (x,y)
		self.agentMatrix[x][y] = agent
		self.emptySites.remove((x,y))

	def remove_agent(self, agent):
		""" Removes agent from grid. """
		self.agentMatrix[agent.gridlocation[0]][agent.gridlocation[1]] = None
		self.emptySites.append(agent.gridlocation)

	def move_agent(self, agent, loc):
		""" Moves agent to loc. """
		self.agentMatrix[agent.gridlocation[0]][agent.gridlocation[1]] = None
		self.emptySites.append(agent.gridlocation)		
		
		self.agentMatrix[loc[0]][loc[1]] = agent
		self.emptySites.remove(loc)
		agent.gridlocation = loc
		
	def switch_agents(self, agent1, agent2):
		""" Switches locations of agent1 and agent2. """
		self.agentMatrix[agent1.gridlocation[0]][agent1.gridlocation[1]] = agent2
		self.agentMatrix[agent2.gridlocation[0]][agent2.gridlocation[1]] = agent1

		temploc = agent1.gridlocation
		agent1.gridlocation = agent2.gridlocation
		agent2.gridlocation = temploc
	
	def get_all_neigh_agent_pairs(self):
		""" Returns list of all pairs of neighboring locations that have agents in them. """
		pairs = set()
		for origLoc in self.neighborLocs.keys():
			if self.agentMatrix[origLoc[0]][origLoc[1]] != None: # there is an agent here
				for loc in self.neighborLocs[origLoc]:
					if self.agentMatrix[loc[0]][loc[1]] != None: # there is an agent at this neighboring loc
						if (self.agentMatrix[origLoc[0]][origLoc[1]],self.agentMatrix[loc[0]][loc[1]]) not in pairs and \
							(self.agentMatrix[loc[0]][loc[1]],self.agentMatrix[origLoc[0]][origLoc[1]]) not in pairs:
							pairs.add((self.agentMatrix[origLoc[0]][origLoc[1]],self.agentMatrix[loc[0]][loc[1]]))
		return list(pairs)

	def get_all_triplets(self):
		"""returns all list of triplets"""
		triplets = list()
		for origLoc in self.neighborLocs.keys():
			if self.agentMatrix[origLoc[0]][origLoc[1]] != None: # there is an agent here
				neighbors_agent = self.get_neighbors(self.agentMatrix[origLoc[0]][origLoc[1]])
				for i in range(len(neighbors_agent)):
					for j in range(i+1,len(neighbors_agent)):
						neighbors_i = self.get_neighbors(neighbors_agent[i])
						neighbors_j = self.get_neighbors(neighbors_agent[j])
						common_neighbors = [neigh for neigh in neighbors_i if neigh in neighbors_j]
						if len(common_neighbors) == 2:
							triplets.append([self.agentMatrix[origLoc[0]][origLoc[1]], neighbors_agent[i], neighbors_agent[j]])
		return triplets

	def get_empty_sites(self):
		""" Returns list of (x,y) tuples that are empty grid locations. """
		return self.emptySites

	def get_empty_locs_in_range(self,location, r):
		""" Return empty location within range r of location """
		locs_in_range = []
		for i in range(location[0] - r, location[0] + r):
			for j in range(location[1] - r, location[1] + r):
				locs_in_range.append( ( i%self.nrows, j%self.ncols) )
		return [loc for loc in locs_in_range if self.agentMatrix[loc[0]][loc[1]] == None]

	def get_all_sites(self):
		""" Returns list of (x,y) tuples that are grid locations. """
		return self.allSites

	def get_all_locs_in_range(self,location, r):
		""" Return all locations within range r of location """
		locs_in_range = []
		for i in range(location[0] - r, location[0] + r):
			for j in range(location[1] - r, location[1] + r):
				locs_in_range.append( ( i%self.nrows, j%self.ncols) )
		return [loc for loc in locs_in_range]

	def get_neighbors(self, agent):
		""" Return neighbors of agent. """
		neighbors = list()
		neighlocs = self.neighborLocs[agent.gridlocation]
		for loc in neighlocs:
			if self.agentMatrix[loc[0]][loc[1]] != None:
				neighbors.append(self.agentMatrix[loc[0]][loc[1]])
		return neighbors

	def get_neighbors_of_loc(self, loc):
		""" Return neighbors of agent. """
		neighbors = list()
		neighlocs = self.neighborLocs[loc]
		for loc in neighlocs:
			if self.agentMatrix[loc[0]][loc[1]] != None:
				neighbors.append(self.agentMatrix[loc[0]][loc[1]])
		return neighbors

	def place_all(self, agentsList):
		"""
		Fills grid with agents, in sequential order at (0,0), (0,1) ... (n,n).
		Assumes len(agents) is enough for every grid location.
		"""
		agents = iter(agentsList)
		# put a agent in each grid location (row, column)
		for row in range(self.nrows):
			for column in range(self.ncols):
				agent = agents.next()
				self.agentMatrix[row][column] = agent
				agent.gridlocation = (row, column)
				self.emptySites.remove((row, column))
