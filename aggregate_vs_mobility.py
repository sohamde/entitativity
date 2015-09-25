"""
For each avg file, takes last 1000 iterations and averages over each column
Saves in a file, which contains a row for each mobility value
Author: Soham De
"""

#total_generations = 20000
average_length = 1.0

# Prefixes of files
path = 'results/ind_vs_ent_results_new/' #'/lustre/sohamde/Entitativity/src/results/'
# example_file = 'coeff_PD_b0.03c0.01_g4_i1_m0.1_mr50_numneighs4_pairallneighs_avg.txt'
prefixes = ['coeff', 'inStratCounts', 'indivStratCounts', 'outStratCounts', 'results', 'tagCounts', 'alive', 'diff_games']
path_prefix = [path+i for i in prefixes]
beginning_str = '_PD_b0.03c0.01_g4_i1_m'
ending_str = '_mr50_numneighs4_pairallneighs_'

for type in range(len(prefixes)):
	output_file_name = path_prefix[type] + beginning_str + ending_str + "allm.txt"
	f_out = open(output_file_name, "wb")
	first_file = 1
	for mp_i in s.mp:
		if 0.01 <= mp_i <= 0.1:
			total_generations = 30000
		else:
			total_generations = 20000
		input_file_name = path_prefix[type] + beginning_str + str(mp_i) + ending_str + "avg.txt"
		f_in = open(input_file_name, "rb")
		row_count = 0
		for r in f_in:
			value_str = r.rstrip()
			if row_count == 0:
				headers = value_str
				if first_file == 1:
					f_out.write(headers+"\n")
					first_file = 0
				row_count += 1
				continue
			if row_count > total_generations - average_length:
				value_str_list = value_str.split(',')
				value_list = [float(i) for i in value_str_list]
				if row_count == total_generations - average_length + 1:
					values = value_list
				else:
					values = [values[i]+value_list[i] for i in range(len(values))]
			row_count += 1
		f_in.close()
		values = [values[i]/average_length for i in range(len(values))]
		val_str = [str(i) for i in values]
		f_out.write(",".join(val_str)+"\n")
	f_out.close()
