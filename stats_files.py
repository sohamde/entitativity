## Keep track of population statistics
## authors: soham de, patrick roos
## emails: (sohamde, roos) at cs umd edu


class Stats:
	"""
	Class to keep track of population statistics and output the results into different files
	"""

	def __init__(self, tags, runID="x", results_folder='./results/'):
		"""
		initialize output files and variables to store statistics
		"""

		self.tags = tags

		# will hold the latest (current) val of all the following, so that we can plot it:
		self.inGrpDefPerc = 0
		self.outGrpDefPerc = 0
		self.cProp_curr = 0 				# cooperation rate
		self.outGroupIntPerc_curr = 0	# out-group interaction rate
		self.collProp_curr = 0 			# % of collectivists
		self.indProp_curr = 0			# % of individualists
		self.avgP_curr = self.avgQ_curr = self.avgI_curr = 0 		# population pqi averages
		self.avgInP_curr = self.avgInQ_curr = self.avgInI_curr = 0	# collectivist's in-group pqi averages
		self.avgOutP_curr = self.avgOutQ_curr = self.avgOutI_curr = 0 # collectivist's out-group pqi averages

		# 'results' file contains statistics such as percentage of cooperation, defection, in-group and out-group cooperation, etc
		self.resultFile = open(results_folder+"results_"+str(runID)+".txt",'wb')
		self.resultFile.write("inGrpDefPerc,outGrpDefPerc,coopProp,outGrpIntProp,collProp,indProp,avgP,avgQ,avgI,avgInP,avgInQ,avgInI,avgOutP,avgOutQ,avgOutI\n")		
		self.tagCountFile = open(results_folder+"tagCounts_"+str(runID)+".txt",'wb')
		for tag in tags:
			if tag == tags[-1]:
				self.tagCountFile.write(str(tag)+"\n")
			else:
				self.tagCountFile.write(str(tag)+",")

		# types of strategies used; first bit: action if in-group/out-group/individual cooperated on last move
		# second bit: action if in-group/out-group/individual defected on last move; 0: cooperate, 1: defect
		self.stratTypes = ["00","01","10","11"]

		# 'indivStratCounts' file contains percentage of 'stratTypes' for individual-entitative agents
		self.indivStratCountFile = open(results_folder+"indivStratCounts_"+str(runID)+".txt",'wb')
		for strat in self.stratTypes:
			if strat == self.stratTypes[-1]:
				self.indivStratCountFile.write(strat+"\n")
			else:
				self.indivStratCountFile.write(strat+",")

		# 'inStratCounts' file contains percentage of 'stratTypes' for group-entitative agents against in-groups
		self.inStratCountFile = open(results_folder+"inStratCounts_"+str(runID)+".txt",'wb')
		for strat in self.stratTypes:
			if strat == self.stratTypes[-1]:
				self.inStratCountFile.write(strat+"\n")
			else:
				self.inStratCountFile.write(strat+",")

		# 'inStratCounts' file contains percentage of 'stratTypes' for group-entitative agents against out-groups
		self.outStratCountFile = open(results_folder+"outStratCounts_"+str(runID)+".txt",'wb')
		for strat in self.stratTypes:
			if strat == self.stratTypes[-1]:
				self.outStratCountFile.write(strat+"\n")
			else:
				self.outStratCountFile.write(strat+",")

		# 'alive' file contains percentage of nodes in the grid populated by agents
		self.alive_file = open(results_folder+"alive_"+str(runID)+".txt","wb")
		self.alive_file.write("alive_proportion\n")

		# 'coeff' file contains value of the modified clustering coefficient in the graph
		self.coeff_file = open(results_folder+"coeff_"+str(runID)+".txt",'wb')
		self.coeff_file.write("clustering_coefficient\n")

		# 'diff_games' contains the average number of unique opponents each agent encounters, and the average number of games played against each of them
		self.diff_games_file = open(results_folder+"diff_games_"+str(runID)+".txt","wb")
		self.diff_games_file.write("no_unique_games,no_games_same_agent,no_games_same_agent_gt_1\n")

	def step(self, agents, inCoops, inDefects, outCoops, outDefects, outGroupIntPerc, alive_proportion, clustering_coeff, diff_games_list):
		""" Records everything for this time step. """
			
		n = len(agents)

		# tag counts
		counts = self.getCounts(agents)
		for tag in self.tags:
			if tag == self.tags[-1]:
				self.tagCountFile.write(str(counts[tag])+"\n") 
			else:
				self.tagCountFile.write(str(counts[tag])+",") 

		# split agents by group-entitative or individual-entitative trait
		collAgents = []
		indAgents = []
		for a in agents:
			if a.CorI == "ent":
				collAgents.append(a)
			else:
				indAgents.append(a)

		# calculate group-entitative and individual-entitative population proportion
		nColl = len(collAgents)
		nInd = len(indAgents)
		if n > 0:
			collProp = nColl/float(n)
			indProp = nInd/float(n)
		else:
			collProp = indProp = 0
			
		# get strategy proportions for individual-entitative, group-entitative in-group and out-group agents
		pCount, qCount, iCount = self.getInPandQCounts(collAgents)
		if nColl > 0:
			avgInP = pCount/float(nColl)
			avgInQ = qCount/float(nColl)
			avgInI = iCount/float(nColl)
		else:
			avgInP = avgInQ = avgInI = 0
		pCount, qCount, iCount = self.getOutPandQCounts(collAgents)
		if nColl > 0:
			avgOutP = pCount/float(nColl)
			avgOutQ = qCount/float(nColl)
			avgOutI = iCount/float(nColl)
		else:
			avgOutP = avgOutQ = avgOutI = 0
	
		pCount, qCount, iCount = self.getPQICounts(indAgents)
		if nInd > 0:
			avgP = pCount/float(nInd)
			avgQ = qCount/float(nInd)
			avgI = iCount/float(nInd)
		else:
			avgP = avgQ = avgI = 0

		defects = inDefects+outDefects
		coops = inCoops+outCoops
		cProp = 0 if ((defects+coops) == 0) else float(coops)/(defects+coops)

		if float(inCoops+inDefects) > 0:
			self.inGrpDefPerc = inDefects/float(inCoops+inDefects)
		else:
			self.inGrpDefPerc = 0

		if float(outCoops+outDefects) > 0:
			self.outGrpDefPerc = outDefects/float(outCoops+outDefects)
		else:
			self.outGrpDefPerc = 0

	
		self.cProp_curr = cProp
		self.outGroupIntPerc_curr = outGroupIntPerc
		self.collProp_curr = collProp
		self.indProp_curr = indProp
		self.avgP_curr = avgP
		self.avgQ_curr = avgQ
		self.avgI_curr = avgI
		self.avgInP_curr = avgInP 
		self.avgInQ_curr = avgInQ
		self.avgInI_curr = avgInI
		self.avgOutP_curr = avgOutP
		self.avgOutQ_curr = avgOutQ
		self.avgOutI_curr = avgOutI

		resultstr = str(self.inGrpDefPerc)+","+str(self.outGrpDefPerc)+","+str(cProp)+","+str(outGroupIntPerc)+","+str(collProp)+","+str(indProp)+ \
						","+str(avgP)+","+str(avgQ)+","+str(avgI)+","+str(avgInP)+","+str(avgInQ)+","+str(avgInI)+ \
						","+str(avgOutP)+","+str(avgOutQ)+","+str(avgOutI)+"\n"
		self.resultFile.write(resultstr)
		
		# individual-entitative strategy type counts
		props = self.countIndivStrategyTypes(indAgents)		
		for strat in self.stratTypes:
			if strat == self.stratTypes[-1]:
				self.indivStratCountFile.write(str(props[strat])+"\n")			
			else:			
				self.indivStratCountFile.write(str(props[strat])+",")

		# group-entitative in-group strategy type counts
		props = self.countInStrategyTypes(collAgents)		
		for strat in self.stratTypes:
			if strat == self.stratTypes[-1]:
				self.inStratCountFile.write(str(props[strat])+"\n")			
			else:			
				self.inStratCountFile.write(str(props[strat])+",")

		# group-entitative out-group strategy type counts
		props = self.countOutStrategyTypes(collAgents)		
		for strat in self.stratTypes:
			if strat == self.stratTypes[-1]:
				self.outStratCountFile.write(str(props[strat])+"\n")			
			else:			
				self.outStratCountFile.write(str(props[strat])+",")

		self.alive_file.write(str(alive_proportion)+"\n")
		self.coeff_file.write(str(clustering_coeff)+"\n")
		self.diff_games_file.write(str(diff_games_list[0])+","+str(diff_games_list[1])+","+str(diff_games_list[2])+"\n")

		return counts


	def getCounts(self, agents):
		""" Get counts of agents of each type of tag """

		counts = {}
		for tag in self.tags:
			counts[tag] = 0

		for agent in agents:
			counts[agent.tag] +=1
			
		return counts 
	
	def getInPandQCounts(self, agents):
		""" Counts of p, q and i for group-entitative in-group """

		countP = 0
		countQ = 0
		countI = 0
		for agent in agents:
			countP += agent.inP
			countQ += agent.inQ
			countI += agent.inI

		return countP, countQ, countI

	def getOutPandQCounts(self, agents):
		""" Counts of p, q and i for group-entitative out-group """

		countP = 0
		countQ = 0
		countI = 0
		for agent in agents:
			countP += agent.outP
			countQ += agent.outQ
			countI += agent.outI

		return countP, countQ, countI
	
	def getPQICounts(self, agents):
		""" Counts of p, q and i for individual-entitative """
		
		countP = 0
		countQ = 0
		countI = 0
		for agent in agents:
			countP += agent.p
			countQ += agent.q
			countI += agent.i

		return countP, countQ, countI


	def countIndivStrategyTypes(self, agents):
		""" Counts total number of "00","01","10","11" strategies and returns proportion dict."""
		
		proportions = {}
		for strat in self.stratTypes:
			proportions[strat]=0
		for agent in agents:
			proportions[str(agent.p)+str(agent.q)] += 1 
				
		for k in proportions.keys():
			if float(len(agents)) == 0:
				proportions[k] = 0
			else:
				proportions[k] = proportions[k]/float(len(agents))

		return proportions

	def countInStrategyTypes(self, agents):
		""" Counts total number of "00","01","10","11" strategies and returns proportion dict."""
		
		proportions = {}
		for strat in self.stratTypes:
			proportions[strat]=0
		for agent in agents:
			proportions[str(agent.inP)+str(agent.inQ)] += 1 
				
		for k in proportions.keys():
			if float(len(agents)) == 0:
				proportions[k] = 0
			else:
				proportions[k] = proportions[k]/float(len(agents))

		return proportions

	def countOutStrategyTypes(self, agents):
		""" Counts total number of "00","01","10","11" strategies and returns proportion dict."""
		
		proportions = {}
		for strat in self.stratTypes:
			proportions[strat]=0
		for agent in agents:
			proportions[str(agent.outP)+str(agent.outQ)] += 1 
				
		for k in proportions.keys():
			if float(len(agents)) == 0:
				proportions[k] = 0
			else:
				proportions[k] = proportions[k]/float(len(agents))

		return proportions

	def close_files(self):
		""" close output files """

		self.resultFile.close()
		self.indivStratCountFile.close()
		self.inStratCountFile.close()
		self.outStratCountFile.close()
		self.tagCountFile.close()
		self.alive_file.close()
		self.coeff_file.close()
		self.diff_games_file.close()
