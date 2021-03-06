## plot values vs time iteration. used to plot a file of the type *avg.txt vs mobility.
##
## run as: python plot_run.py {run_number} {mobility_probability} {graph_initialization} {type_of_plot}
## set run_number to avg if plotting average simulation run.
## mobility_probability was varied from 0.0 to 0.08 in the paper
## graph_initialization can take values 0, 1, 2, 3, 4 (more details in globals.py)
## type_of_plot can be from 1, 2, ..., 9. more details of each type of graph is below.
##
## authors: soham de, patrick roos
## emails: (sohamde, roos) at cs umd edu

import matplotlib.pyplot as plt
import numpy as np
import sys

# input file to plot
mobility_prob = float(sys.argv[2])
actual_mobility_prob = mobility_prob

# path where file exists
path_to_results_folder = 'results/alternate_model/'

# graph initialization of file to plot
init = int(sys.argv[3])

# type of graph to plot
graph_opt = int(sys.argv[4])

# run number. 'avg' for average run
run = str(sys.argv[1])

# number of generations. for mobility 0 on the original runs, we kept generations as 20000. all other runs were 30000.
if 'reported_results' in path_to_results_folder and actual_mobility_prob == 0.0:
	total_generations = 20000
else:
	total_generations = 30000

# type of graph to plot. each option plots a different graph which was shown in the paper.
if graph_opt == 1:
	# plot of group-entitative agents vs individual-entitative agents
	columns_to_ignore = [0,1,2,3]+(range(6,15))
	custom_legend = ['Group-Entitative Agents', 'Individual-Entitative Agents']
	file_name = 'results'
	title_str = str('Group-Entitative vs. Individual-Entitative (Mobility '+str(actual_mobility_prob)+')')

elif graph_opt == 2:
	# plot of percentage of cooperators, in-group defectors and out-group defectors
	columns_to_ignore = list(set(range(15)) - {0,1,2})
	custom_legend = ['In-Group Defection', 'Out-Group Defection', 'Cooperative Actions']
	file_name = 'results'
	title_str = ''

elif graph_opt == 3:
	# percentage of different types of in-group strategies for group-entitative agents
	columns_to_ignore = []
	custom_legend = ['AllC', 'TFT', 'OTFT', 'AllD']
	file_name = 'inStratCounts'
	title_str = str('Group-Entitative In-Group Strategies (Mobility '+str(actual_mobility_prob)+')')

elif graph_opt == 4:
	# percentage of different types of out-group strategies for group-entitative agents
	columns_to_ignore = []
	custom_legend = ['AllC', 'TFT', 'OTFT', 'AllD']
	file_name = 'outStratCounts'
	title_str = str('Group-Entitative Out-Group Strategies (Mobility '+str(actual_mobility_prob)+')')

elif graph_opt == 5:
	# percentage of different types of strategies for individual-entitative agents
	columns_to_ignore = []
	custom_legend = ['AllC', 'TFT', 'OTFT', 'AllD']
	file_name = 'indivStratCounts'
	title_str = str('Individual-Entitative Strategies (Mobility '+str(actual_mobility_prob)+')')

elif graph_opt == 6:
	# clustering coefficient
	columns_to_ignore = []
	custom_legend = ['Clustering Coefficient']
	file_name = 'coeff'
	title_str = ''

elif graph_opt == 7:
	# number of cooperations (x) vs number of defections (1 - x)
	columns_to_ignore = list(set(range(15)) - {2}) # the other one is 1 - x
	custom_legend = ['Cooperations', 'Defections']
	file_name = 'results'
	title_str = ''

elif graph_opt == 8:
	# number of cooperations (x) vs number of defections (1 - x)
	columns_to_ignore = [1]
	custom_legend = ['Unique Opponents', 'Games With Same Opponent']
	file_name = 'diff_games'
	title_str = ''

elif graph_opt == 9:
	# proportion of agents alive
	columns_to_ignore = []
	custom_legend = ['Alive Proportion']
	file_name = 'alive'
	title_str = ''

else:
	# specify columns_to_ignore and custom_legend manually
	columns_to_ignore = [0,1,2,3]+(range(6,15))
	custom_legend = ['Group-Entitative Agents', 'Individual-Entitative Agents']
	file_name = 'results'
	title_str = ''

# building file name of file to plot
file_to_plot = path_to_results_folder+file_name+'_PD_b0.03c0.01_g4_i1_m'+str(mobility_prob)+'_mr50_numneighs4_init'+str(init)+'_pairallneighs_'+run+'.txt'
f_in = open(file_to_plot, "rb")

# colors and linestyles for plot
colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', '0.3']
linestyles=['-', '--']
markers = ['o', 's', '*', 'v', '^', '+', 'x', '>', '<']

# list to save values
y_values = list()

# looping over each row in the file
first_row = 1
idx = 0
for r in f_in:
	# save header if first row
	if first_row == 1:
		header_str = r.rstrip()
		header_str_list = header_str.split(',')
		header_list = [header_str_list[i] for i in range(len(header_str_list)) if i not in columns_to_ignore]
		first_row = 0
		continue

	# saving values in y_values
	value_str = r.rstrip()
	value_str_list = value_str.split(',')
	value_list = [float(value_str_list[i]) for i in range(len(value_str_list)) if i not in columns_to_ignore]
	y_values.append(value_list)
	idx += 1
y_values = map(list, zip(*y_values))

if graph_opt == 7:
	y_values.append([1-x for x in y_values[0]])

# plotting y_values
for i in range(len(y_values)):
	temp_list = list(y_values[i])
	temp_list.append(y_values[i][total_generations-1])
	plt.plot(range(0, total_generations+1, 100), temp_list[0::100], linestyle=linestyles[i/len(colors)], color=colors[i%len(colors)], linewidth=3.0)
plt.xlim(0., total_generations)
plt.xlabel('Time').set_size(18)
plt.ylabel('Population %').set_size(18)
if graph_opt != 8:
	plt.yticks(np.arange(0,1.1,0.1))
plt.tick_params(axis='both', which='major', labelsize=14)

if graph_opt in [3,4,6,8,9]:
	leg = plt.legend(custom_legend, prop={'size':18})
else:
	leg = plt.legend(custom_legend, bbox_to_anchor=(0.9, 0.6),bbox_transform=plt.gcf().transFigure, prop={'size':18})

for leg_obj in leg.legendHandles:
	leg_obj.set_linewidth(5.0)
plt.grid(b=True, which='both', color='0.65',linestyle='-')
plt.title(title_str, fontsize = 18)
plt.show()
