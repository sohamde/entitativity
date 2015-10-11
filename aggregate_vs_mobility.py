## For each average results file (i.e., files ending with *avg.txt) for a range of mobility specified by 'mp',
## aggregates the last row of each file into a new file, with one entry corresponding to each mobility value.
##
## Saves in a file, which contains a row for each mobility value
##
## New file name is *allm.txt, where * is specified by the *avg.txt files used to aggregate the values
##
## authors: soham de, patrick roos
## emails: (sohamde, roos) at cs umd edu

# specify total number of iterations the simulations were run for
total_iterations = 30000

# = 1 means choose last row from each file. If the number is x, it averages over the last x rows for each column
average_length = 1.0

# range of mobility over which to aggregate
mp = [x/100.0 for x in range(0, 9)]

# Path of results files
#path = 'results/reported_results/'
path = 'results/init234_mu005/'

# prefixes of files
prefixes = ['coeff', 'inStratCounts', 'indivStratCounts', 'outStratCounts', 'results', 'tagCounts', 'alive', 'diff_games']

# concatenating path with prefixes
path_prefix = [path+i for i in prefixes]

# beginning and ending string for each results file name
beginning_str = '_PD_b0.03c0.01_g4_i1_m'
ending_str = '_mr50_numneighs4_init4_pairallneighs_'

# for each file in prefixes
for type in range(len(prefixes)):

	# save output file name
	output_file_name = path_prefix[type] + beginning_str + ending_str + "allm.txt"
	f_out = open(output_file_name, "wb")
	first_file = 1

	# for each mobility value
	for mp_i in mp:

		# in reported results, for mobility value 0, the total generations used were 20000 instead of 30000
		if 'reported_results' in path and mp_i == 0.0:
			total_generations = 20000
		else:
			total_generations = total_iterations

		# creating input file name and opening file
		input_file_name = path_prefix[type] + beginning_str + str(mp_i) + ending_str + "avg.txt"
		f_in = open(input_file_name, "rb")

		# traverse through rows in a file
		row_count = 0
		for r in f_in:
			value_str = r.rstrip()

			# save header information if first row of the file
			if row_count == 0:
				headers = value_str
				if first_file == 1:
					f_out.write(headers+"\n")
					first_file = 0
				row_count += 1
				continue

			# if last row or last few rows, average the values together (just picks last row if average_length = 1)
			if row_count > total_generations - average_length:
				value_str_list = value_str.split(',')
				value_list = [float(i) for i in value_str_list]
				if row_count == total_generations - average_length + 1:
					values = value_list
				else:
					values = [values[i]+value_list[i] for i in range(len(values))]
			row_count += 1
		f_in.close()

		# calculates average of last few rows
		values = [values[i]/average_length for i in range(len(values))]
		val_str = [str(i) for i in values]

		# writes into file
		f_out.write(",".join(val_str)+"\n")
	f_out.close()
