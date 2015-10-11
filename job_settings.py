# Job settings used by create_jobs.py and aggregate_runs.py

# Mobility probability
mp = [x/100.0 for x in range(0, 9)]
#mp = [x/100.0 for x in range(0, 11)]+[x/50.0 for x in range(6,11)] 

# Number of runs for each setting
runs = 50   # 75

# Initial grid initialization
init = [1, 2, 3, 4]

# Total number of runs
total = len(mp)*runs*len(init)
print "Number of jobs: "+str(total)
