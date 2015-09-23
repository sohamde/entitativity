"""
Aggregates clustering coefficient values from the different runs on the cluster
Author: sohamde at cs umd edu
"""

import csv

file_name_prefix = 'results/coeff_PD_b0.03c0.01_g4_i1_m0.5_mr50_numneighs4_pairallneighs_'
start = 1
end = 10
number_of_files = float(end - start + 1)
generations = 10000
coefficients = [0]*generations

for i in range(start,end+1):
	f_name = file_name_prefix + str(i) + '.txt'
	print f_name
	f = open(f_name, 'rb')
	reader = csv.reader(f)
	row_number = -1
	for row in reader:
		if row_number == -1:
			header = row[0]
		else:
			coefficients[row_number] += float(row[0])
		row_number += 1

avg_coefficients = [x/number_of_files for x in coefficients]

output_file_name = file_name_prefix + str(start) + '_' + str(end) + '_avg.txt'
out_file = open(output_file_name, 'wb')
out_file.write(header+'\n')
for x in avg_coefficients:
	out_file.write(str(x)+'\n')

