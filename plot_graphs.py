import matplotlib.pyplot as plt
import matplotlib.cm as cmx
import csv
import sys
import matplotlib.colors

choose = 1 # 1 for mobility, 0 for individual coefficients

#settings = '_coord_a0.2b0.18l0.05rho0.1mob0.0mu0.02death0.1im1grid_50_50_switch2000_run1.txt'
if choose == 0:
	settings = '_PD_b0.03c0.01_g4_i1_m0.5_mr50_numneighs4_pairallneighs_1_10_avg.txt'
elif choose == 1:
	settings = '_0.0_0.1_0.5.txt'
#settings = sys.argv[1]

colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', '0.3']
markers = ['o', 's', '*', 'v', '^', '+', 'x', '>', '<']

#prefixes = ['allProps', 'contProps', 'punProps', 'stats']

if choose == 0:
	prefixes = ['coeff']
elif choose == 1:
	prefixes = ['mobility']

lstyle = ['-','--']
jet = cm = plt.get_cmap('jet')
cNorm  = matplotlib.colors.Normalize(vmin=0, vmax=10000)
scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=jet)
headers2 = ['Mobility Prob 0.0', 'Mobility Prob 0.1', 'Mobility Prob 0.5']
for i in range(len(prefixes)):
	
	#f_name = 'stats/'+prefixes[i]+settings
	f_name = 'results/'+prefixes[i]+settings
	
	print f_name
	f = open(f_name, 'rb')
	reader = csv.reader(f)
	row_num = 0
	val_num = 0
	headers = []
	for row in reader:
		if row_num == 0:
			row_num += 1
			headers = row
			values = []
			continue
		for j in range(len(row)):
			if val_num < len(row):
				values.append([float(row[j])])
			else:
				values[j].append(float(row[j]))
			val_num += 1
	for j in range(len(markers)):
		for k in range(len(colors)):
			if j*len(colors)+k < len(values):
				if prefixes[i] == 'stats' and j == 0 and k == 0:
					plt.plot(values[j*len(colors)+k][0::10], marker=markers[j], linestyle='-', color=colors[k])
					plt.xlabel('time')
					plt.ylabel('total population payoff')
					plt.title('total population payoff')
					plt.show()
				else:
					colorVal = scalarMap.to_rgba(k)
					val_temp = values[j*len(colors)+k][0:10000]
					print len(val_temp)
					plt.plot(val_temp[0::5], linestyle= lstyle[k%2], color=colors[k],linewidth=1,
							label=headers2[j*len(colors)+k], markevery=100)
	plt.xlabel('Time').set_size(12)
	plt.ylabel('Modified Clustering Coefficient').set_size(12)
	if choose == 0:
		plt.title('Mobility Probability 0.5')
	elif choose == 1:
		plt.title('Clustering Coefficient With Different Degrees Of Mobility')
	if choose == 1:
		plt.legend()
	plt.show()
	f.close()

