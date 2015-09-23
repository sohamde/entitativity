# ##########################
#
#  *** To keep track of population statistics. ****
#   
#
# @author: roos@cs.umd.edu
# @version: aug-2013
# ##########################

import pickle as pkl

class Stats:

	def __init__(self, tags, runID="x"):

		self.tags = tags

		# will hold the latest (current) val of all the following, so that we can plot it:
		inGrpDefPerc = 0
		outGrpDefPerc = 0
		cProp_curr = 0 				# cooperation rate
		outGroupIntPerc_curr = 0	# out-group interaction rate
		collProp_curr = 0 			# % of collectivists
		indProp_curr = 0			# % of individualists
		avgP_curr = avgQ_curr = avgI_curr = 0 		# population pqi averages
		avgInP_curr = avgInQ_curr = avgInI_curr = 0	# collectivist's in-group pqi averages
		avgOutP_curr = avgOutQ_curr = avgOutI_curr = 0 # collectivist's out-group pqi averages

		self.resultFile = open("/lustre/sohamde/Entitativity/src/results/results_"+str(runID)+".txt",'wb')
		self.resultFile.write("inGrpDefPerc,outGrpDefPerc,coopProp,outGrpIntProp,collProp,indProp,avgP,avgQ,avgI,avgInP,avgInQ,avgInI,avgOutP,avgOutQ,avgOutI\n")		
		self.tagCountFile = open("/lustre/sohamde/Entitativity/src/results/tagCounts_"+str(runID)+".txt",'wb')
		for tag in tags:
			if tag == tags[-1]:
				self.tagCountFile.write(str(tag)+"\n")
			else:
				self.tagCountFile.write(str(tag)+",")

		self.stratTypes = ["00","01","10","11"]

		self.indivStratCountFile = open("/lustre/sohamde/Entitativity/src/results/indivStratCounts_"+str(runID)+".txt",'wb')
		for strat in self.stratTypes:
			if strat == self.stratTypes[-1]:
				self.indivStratCountFile.write(strat+"\n")
			else:
				self.indivStratCountFile.write(strat+",")

		self.inStratCountFile = open("/lustre/sohamde/Entitativity/src/results/inStratCounts_"+str(runID)+".txt",'wb')
		for strat in self.stratTypes:
			if strat == self.stratTypes[-1]:
				self.inStratCountFile.write(strat+"\n")
			else:
				self.inStratCountFile.write(strat+",")

		self.outStratCountFile = open("/lustre/sohamde/Entitativity/src/results/outStratCounts_"+str(runID)+".txt",'wb')
		for strat in self.stratTypes:
			if strat == self.stratTypes[-1]:
				self.outStratCountFile.write(strat+"\n")
			else:
				self.outStratCountFile.write(strat+",")

	
	def step(self, agents, inCoops, inDefects, outCoops, outDefects, outGroupIntPerc):
		""" Records everything for this time step. """
			
		n = len(agents)

		# tag counts
		counts = self.getCounts(agents)
		for tag in self.tags:
			if tag == self.tags[-1]:
				self.tagCountFile.write(str(counts[tag])+"\n") 
			else:
				self.tagCountFile.write(str(counts[tag])+",") 

		# split agents by Coll vs Ind trait
		collAgents = []
		indAgents = []
		for a in agents:
			if a.CorI == "ent":
				collAgents.append(a)
			else:
				indAgents.append(a)

		# calc col and ind pop proportion
		nColl = len(collAgents)
		nInd = len(indAgents)
		if n > 0:
			collProp = nColl/float(n)
			indProp = nInd/float(n)
		else:
			collProp = indProp = 0
			
		# get in out and ind pqi
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
		#print resultstr
		self.resultFile.write(resultstr)		
		
		# individualist strategy type counts
		props = self.countIndivStrategyTypes(indAgents)		
		for strat in self.stratTypes:
			if strat == self.stratTypes[-1]:
				self.indivStratCountFile.write(str(props[strat])+"\n")			
			else:			
				self.indivStratCountFile.write(str(props[strat])+",")

		# coll in strategy type counts
		props = self.countInStrategyTypes(collAgents)		
		for strat in self.stratTypes:
			if strat == self.stratTypes[-1]:
				self.inStratCountFile.write(str(props[strat])+"\n")			
			else:			
				self.inStratCountFile.write(str(props[strat])+",")

		# coll out strategy type counts
		props = self.countOutStrategyTypes(collAgents)		
		for strat in self.stratTypes:
			if strat == self.stratTypes[-1]:
				self.outStratCountFile.write(str(props[strat])+"\n")			
			else:			
				self.outStratCountFile.write(str(props[strat])+",")

		return counts


	def getCounts(self, agents):
		""" Gets counts, averag i, and avg in and out-group strategy p and q in a relationsMatrix"""

		counts = {}
		for tag in self.tags:
			counts[tag] = 0

		for agent in agents:
			counts[agent.tag] +=1
			
		return counts 
	
	def getInPandQCounts(self, agents):
		countP = 0
		countQ = 0
		countI = 0
		for agent in agents:
			countP += agent.inP
			countQ += agent.inQ
			countI += agent.inI

		return countP, countQ, countI

	def getOutPandQCounts(self, agents):
		countP = 0
		countQ = 0
		countI = 0
		for agent in agents:
			countP += agent.outP
			countQ += agent.outQ
			countI += agent.outI

		return countP, countQ, countI
	
	def getPQICounts(self, agents):
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
		self.resultFile.close()
		self.indivStratCountFile.close()
		self.inStratCountFile.close()
		self.outStratCountFile.close()
		self.tagCountFile.close()

