"""
Puts clustering coefficients for the different mobilities into the same file
Author: sohamde at cs umd edu
"""

import csv

f1_mobility = 'results/coeff_PD_b0.03c0.01_g4_i1_m0.0_mr50_numneighs4_pairallneighs_1_10_avg.txt'
f2_mobility = 'results/coeff_PD_b0.03c0.01_g4_i1_m0.1_mr50_numneighs4_pairallneighs_1_10_avg.txt'
f3_mobility = 'results/coeff_PD_b0.03c0.01_g4_i1_m0.5_mr50_numneighs4_pairallneighs_1_10_avg.txt'
output_file = 'results/mobility_0.0_0.1_0.5.txt'
out_header = 'mobility_0.0, mobility_0.1, mobility_0.5'

f1 = open(f1_mobility, 'rb')
f2 = open(f2_mobility, 'rb')
f3 = open(f3_mobility, 'rb')

number_of_files = 3
generations = 10000
c1 = [0]*generations
c2 = [0]*generations
c3 = [0]*generations
#coefficients = [[0]*number_of_files]*generations

row_number = -1
reader1 = csv.reader(f1)
for row in reader1:
	if row_number == -1:
		header = row[0]
	else:
		c1[row_number] = float(row[0])
	row_number += 1
print row_number

#print coefficients[651][0], coefficients[651][1], coefficients[651][2]

row_number = -1
reader2 = csv.reader(f2)
for row in reader2:
	if row_number == -1:
		header = row[0]
	else:
		c2[row_number] = float(row[0])
	row_number += 1
print row_number

#print coefficients[651][0], coefficients[651][1], coefficients[651][2]

row_number = -1
reader3 = csv.reader(f3)
for row in reader3:
	if row_number == -1:
		header = row[0]
	else:
		c3[row_number] = float(row[0])
	row_number += 1
print row_number

#print coefficients[651][0], coefficients[651][1], coefficients[651][2]

out_file = open(output_file, 'wb')
out_file.write(out_header+'\n')
for i in range(generations):
	out_file.write(str(c1[i])+', '+str(c2[i])+', '+str(c3[i])+'\n')
