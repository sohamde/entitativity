import sys
import stats_files as st

######################### MAIN ENVIRONMENT PARAMETERS #########################
nTags = 4				# number of tags in environment
tags = xrange(nTags)    # list of tags (1,2,..., nTags-1)
n = 50      # grid is nxn
maxTime = 30000 # end after maxTime timesteps
numIts = 1		# number of game iterations to play in each pairing

# agent can interact and reproduce into only the top, left, right and bottom spots on the grid
reproduction_neighborhood = [(-1,0), (0,-1), (0,+1), (+1,0)]
neighborhood = [(-1,0),	(0,-1), (0,+1), (+1,0)]

# to calculate average number of different agents an agent meets during it's lifetime
cnt_dead = 0.0  # count of the number of agents that have died
cnt_len_gt_0 = 0.0  # count of the number of agents that have died playing at least one game
avg_diff_agents = 0.0  # average number of different agents each agent meets
agent_opponents = {}  # for each agent, list of unique agents it has played a game against
avg_same = 0.0  # average number of games an agent plays with the same agent
avg_same_gt_1 = 0.0  # considering only agents which have played at least one game
no_games = {}  # number of games each agent plays

PAIRALLNEIGHS = True    # whether to pair all neighbors or do sampling scheme
numActs = 4				# number of interactions to strive for (and max limit) if sampling scheme is used
basePTR = 0.12	        # base potential to reproduce (same as in Hammond and Axelrod, 2006)

cluster = 0     # 1 if running on DeepThought2 cluster, 0 otherwise
if cluster == 0:
	results_folder = './results/'
else:
	results_folder = '/lustre/sohamde/Entitativity/src/results/'

# game to play
hawkdove = False
if hawkdove:
	b = 0.04
	c = 0.06
	GAMEMATRIX = [ [ ( b/2.0, b/2.0 ), (0, b) ] , [ (b, 0), ( (b-c)/2.0, (b-c)/2.0 )] ]
	maxPosPay = b/2.0*numActs
	minPosPay = 0
else:
	b = 0.03        # benefit of cooperation (same as in Hammond and Axelrod, 2006)
	c = 0.01        # cost of cooperation (same as in Hammond and Axelrod, 2006)
	GAMEMATRIX = [ [(b-c,b-c),(-c,b)] , [(b,-c),(0,0)] ]
	maxPosPay = basePTR+b*numActs*2     # highest possible payoff
	minPosPay = basePTR-c*numActs*2     # lowest possible payoff

# probability of an agent moving to a random empty spot in the grid
mobility = float(sys.argv[2])

imRate = 1		    # immigration rate - how many immigrants to add each step (same as in Hammond and Axelrod, 2006)
mu = 0.05		    # mutation rate (same as in Hammond and Axelrod, 2006)
deathrate = 0.10    # probability of death (same as in Hammond and Axelrod, 2006)

onlyEnt = False     # whether to only use group-entitative agents
keepGroupsEqual = False     # whether to set a max limit on group size at equal percentage of population
maxGroupSize = n*n/nTags    # only relevant if keepGroupsEqual is set to True
fullEnt = False             # whether to have group-entitative agents be fully so (harm on neighbor is harm on self)
normPtr = False
moveTowardOwn = False
moveRange = n

# specify grid initialization; 0: empty, 1: filled random agents, 2: group ent, C with in-group, D with out-group
# 3: group ent, C with in-group and TFT with out-group, 4: individual-entitative, TFT
grid_initialization = int(sys.argv[3])     # Hammond and Axelrod initialized with empty grid, ie grid_initialization = 0

# saving run ID
if hawkdove:
	runId = "HD_v"+str(b)+"c"+str(c)+"_g"+str(nTags)+"_i"+str(numIts)+"_m"+str(mobility)+"_mr"+str(moveRange)+"_numneighs"+str(len(neighborhood))+"_"
else:
	runId = "PD_b"+str(b)+"c"+str(c)+"_g"+str(nTags)+"_i"+str(numIts)+"_m"+str(mobility)+"_mr"+str(moveRange)+"_numneighs"+str(len(neighborhood))+"_init"+str(grid_initialization)+"_"
if PAIRALLNEIGHS:
	runId+="pairallneighs_"
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

stats = st.Stats(tags, runId, results_folder) # to record statistics, e.g. counts over time

coeff_file = open(results_folder+"coeff_"+str(runId)+".txt",'wb')
coeff_file.write("clustering_coefficient\n")
alive_file = open(results_folder+"alive_"+str(runId)+".txt","wb")
alive_file.write("alive_proportion\n")
diff_games_file = open(results_folder+"diff_games__"+str(runId)+".txt","wb")
diff_games_file.write("no_unique_games,no_games_same_agent,no_games_same_agent_gt_1\n")
