## Averages over different runs in results folder using settings defined in mp, runs, network_init
##
## Creates a file *_avg.txt for each set of runs with file names *_{run_number}.txt
##
## authors: soham de, patrick roos
## emails: (sohamde, roos) at cs umd edu

import os

# different mobilities. creates a different avg file for each mobility value
mp = [x/100.0 for x in range(0, 9)]

# number of runs. files names go from *_1.txt to *_{runs}.txt
runs = 50

# initialization of network used. check 'grid_initialization' parameter in globals.py for a list of different values this parameter can take.
network_init = 4

# set path to folder where output files will be saved; cluster = 1 if running on DeepThought2 cluster, 0 otherwise
if os.path.isdir("/lustre/sohamde/Entitativity"):
	path = '/lustre/sohamde/Entitativity/src/results/'
else:
	path = './results/'

# set prefixes of files
prefixes = ['coeff', 'inStratCounts', 'indivStratCounts', 'outStratCounts', 'results', 'tagCounts', 'alive', 'diff_games']

# concatenating path with prefixes
path_prefix = [path+i for i in prefixes]

# beginning and ending strings of the results files
beginning_str = '_PD_b0.03c0.01_g4_i1_m'
ending_str = '_mr50_numneighs4_init'+str(network_init)+'_pairallneighs_'

# for each mobility value
for mp_i in mp:

	# create run ID
	run_ID = beginning_str + str(mp_i) + ending_str

	# nested list for storing values and headers
	values = list()
	headers = list()

	# looping over runs
	first_run = 1
	for run in range(1,runs+1):

		# Creating file name
		input_file_names = [i+run_ID+str(run)+".txt" for i in path_prefix]

		# Opening each kind of results file
		for type in range(len(prefixes)):

			if first_run == 1:
				values.append(list())

			# Opening results files and updating values list
			f_in = open(input_file_names[type], "rb")
			first_row = 1
			row_count = 0
			for r in f_in:

				# save values
				value_str = r.rstrip()

				# save header
				if first_row == 1:
					if first_run == 1:
						headers.append(value_str)
					first_row = 0
					continue

				# save values
				value_str_list = value_str.split(',')
				value_list = [float(i) for i in value_str_list]
				if first_run == 1:
					values[type].append(value_list)
				else:
					values[type][row_count] = [sum(x) for x in zip(values[type][row_count], value_list)]

				row_count += 1
			f_in.close()

		first_run = 0

	# saving average file for this mobility setting
	output_file_names = [i+run_ID+"avg.txt" for i in path_prefix]
	for type in range(len(prefixes)):
		f_out = open(output_file_names[type], "wb")
		f_out.write(headers[type]+"\n")
		for l in values[type]:
			# averaging over runs for each row
			l_avg = [i/runs for i in l]
			l_str = [str(i) for i in l_avg]
			f_out.write(",".join(l_str)+"\n")
		f_out.close()

	print 'completed averaging over files with mobility:', mp_i
