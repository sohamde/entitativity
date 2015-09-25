## Initializes global variables
## authors: soham de, patrick roos
## emails: (sohamde, roos) at cs umd edu


import sys
import stats_files as st

# number of tags (different groups) in environment (4 in Hammond & Axelrod 2006)
nTags = 4

# list of tags (1,2,..., nTags-1)
tags = xrange(nTags)

# grid size parameter; grid is nxn (50x50 grid in Hammond & Axelrod 2006)
n = 50

# end after maxTime timesteps
maxTime = 30000

# number of game iterations to play in each pairing (1 in Hammond & Axelrod 2006)
numIts = 1

# agent can interact and reproduce into only the top, left, right and bottom spots on the grid
reproduction_neighborhood = [(-1, 0), (0, -1), (0, +1), (+1, 0)]
neighborhood = [(-1, 0), (0, -1), (0, +1), (+1, 0)]

# if true: pair all neighbors, otherwise do sampling scheme (True in Hammond & Axelrod 2006)
PAIRALLNEIGHS = True

# number of interactions to aim for (and max limit) if sampling scheme is used (not relevant if PAIRALLNEIGHS is True)
numActs = 4

# base potential to reproduce (0.12 in Hammond and Axelrod, 2006)
basePTR = 0.12

# immigration rate - how many agents to add each step (1 in Hammond and Axelrod, 2006)
imRate = 1

# mutation rate (0.05 in Hammond and Axelrod, 2006)
mu = 0.05

# probability of death (0.10 in Hammond and Axelrod, 2006)
deathrate = 0.10

# Two player game matrix to use (hawkdove has to be false to use game matrix used in Hammond & Axelrod 2006)
hawkdove = False
if hawkdove:
	b = 0.04
	c = 0.06
	GAMEMATRIX = [[(b/2.0, b/2.0), (0, b)], [(b, 0), ((b-c)/2.0, (b-c)/2.0)]]
	maxPosPay = b/2.0*numActs
	minPosPay = 0
else:   # used in Hammond & Axelrod 2006
	b = 0.03        # benefit of cooperation (0.03 in Hammond and Axelrod, 2006)
	c = 0.01        # cost of cooperation (0.01 in Hammond and Axelrod, 2006)
	GAMEMATRIX = [[(b-c, b-c), (-c, b)], [(b, -c), (0, 0)]]
	maxPosPay = basePTR+b*numActs*2     # highest possible payoff
	minPosPay = basePTR-c*numActs*2     # lowest possible payoff

# probability of an agent moving to a random empty spot in the grid
mobility = float(sys.argv[2])

# grid initialization; 0: empty (setting in Hammond & Axelrod 2006), 1,2,3,4: start with grid filled with agents
# 1: random agents, 2: group-ent, C in-group, D out-group, 3: group-ent, C in-group, TFT out-group, 4: individual-ent TFT
grid_initialization = int(sys.argv[3])

# ADDITIONAL CONTROL VARIABLES
onlyEnt = False             # whether to only use group-entitative agents
keepGroupsEqual = False     # whether to set a max limit on group size at equal percentage of population
maxGroupSize = n*n/nTags    # only relevant if keepGroupsEqual is set to True
fullEnt = False             # whether to have group-entitative agents be fully so (harm on neighbor is harm on self)
normPtr = False             # whether to normalize potential to reproduce
moveTowardOwn = False       # whether mobility should be towards agents with same group tag
moveRange = n               # range of mobility

# set path to folder where output files will be saved
cluster = 0     # 1 if running on DeepThought2 cluster, 0 otherwise and set appropriate results folder path
if cluster == 0:
	results_folder = './results/'
else:
	results_folder = '/lustre/sohamde/Entitativity/src/results/'

# variables to calculate different statistics
cnt_dead = 0.0              # count of the number of agents that have died
cnt_len_gt_0 = 0.0          # count of the number of agents that have died playing at least one game
avg_diff_agents = 0.0       # average number of unique agents each agent plays a game against
agent_opponents = {}        # for each agent, list of unique agents it has played a game against
avg_same = 0.0              # average number of games an agent plays with the same agent
avg_same_gt_1 = 0.0         # considering only agents which have played at least one game
no_games = {}               # number of games each agent plays

# saving run ID
if hawkdove:
	runId = "HD_v"+str(b)+"c"+str(c)+"_g"+str(nTags)+"_i"+str(numIts)+"_m"+str(mobility)+"_mr"+str(moveRange)+"_numneighs"+str(len(neighborhood))+"_"
else:
	runId = "PD_b"+str(b)+"c"+str(c)+"_g"+str(nTags)+"_i"+str(numIts)+"_m"+str(mobility)+"_mr"+str(moveRange)+"_numneighs"+str(len(neighborhood))+"_init"+str(grid_initialization)+"_"
if PAIRALLNEIGHS:
	runId += "pairallneighs_"
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

# initializing stats class object to record statistics
stats = st.Stats(tags, runId, results_folder)
