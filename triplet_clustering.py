"""
code for calculating a modified clustering coefficient from a grid network
author: soham de, university of maryland
"""


def empty_ignore(agents, grid):
	"""considers only triplets where all 3 spots are filled"""
	triplets = grid.get_all_triplets()
	total_triplets = len(triplets)
	same_triplet = 0.0
	for triplet in triplets:
		if triplet[0].tag == triplet[1].tag and triplet[0].tag == triplet[2].tag:
		#if triplet[0].tag == triplet[1].tag:
			same_triplet += 1.0
	if total_triplets == 0:
		return 0.0
	return same_triplet/total_triplets