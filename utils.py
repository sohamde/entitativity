## Various helper methods.
## authors: soham de, patrick roos
## emails: (sohamde, roos) at cs umd edu

import globals as g


def empty_ignore(agents, grid):
	"""
	Calculates a modified clustering coefficient from a grid torus network
	Considers only triplets where all 3 spots are filled
	"""
	triplets = grid.get_all_triplets()
	total_triplets = len(triplets)
	same_triplet = 0.0
	for triplet in triplets:
		if triplet[0].tag == triplet[1].tag and triplet[0].tag == triplet[2].tag:
			same_triplet += 1.0
	if total_triplets == 0:
		return 0.0
	return same_triplet/total_triplets


def normalizePtr(ptr,minPosPay,maxPosPay):
	""" Normalizes ptr so that the possible range is [0,1]."""
	if g.normPtr:
		return (float(ptr) - minPosPay)/float((maxPosPay - minPosPay))
	else:
		return ptr


def resetPTR(agents):
	""" Sets ptr to basePTR """
	for agent in agents:
		agent.ptr = g.basePTR


def transpose(seq):
	"""Return transpose of `seq`."""
	return zip(*seq)


def mean(seq):
	"""Return mean of values in `seq`."""
	n = len(seq)
	return sum(seq)/float(n)
