"""
Plot values vs mobility
Author: Soham De
"""

import matplotlib.pyplot as plt
import numpy as np
import sys

# for mobility settings
total_generations = 30000

# input file to plot
mobility_prob = float(sys.argv[2])
actual_mobility_prob = mobility_prob

init = 2

graph_opt = int(sys.argv[1])
if graph_opt == 1:
	# plot of group-entitative agents vs individual-entitative agents
	columns_to_ignore = [0,1,2,3]+(range(6,15))
	custom_legend = ['Group-Entitative Agents', 'Individual-Entitative Agents']
	file_name = 'results'
elif graph_opt == 2:
	# plot of percentage of cooperators, in-group defectors and out-group defectors
	columns_to_ignore = list(set(range(15)) - {0,1,2})
	custom_legend = ['In-Group Defection', 'Out-Group Defection', 'Cooperative Actions']
	file_name = 'results'
elif graph_opt == 3:
	# percentage of different types of in-group strategies for group-entitative agents
	columns_to_ignore = []
	custom_legend = ['AllC', 'TFT', 'OTFT', 'AllD']
	file_name = 'inStratCounts'
elif graph_opt == 4:
	# percentage of different types of out-group strategies for group-entitative agents
	columns_to_ignore = []
	custom_legend = ['AllC', 'TFT', 'OTFT', 'AllD']
	file_name = 'outStratCounts'
elif graph_opt == 5:
	# percentage of different types of strategies for individual-entitative agents
	columns_to_ignore = []
	custom_legend = ['AllC', 'TFT', 'OTFT', 'AllD']
	file_name = 'indivStratCounts'
elif graph_opt == 6:
	# clustering coefficient
	columns_to_ignore = []
	custom_legend = ['Clustering Coefficient']
	file_name = 'coeff'
elif graph_opt == 7:
	# number of cooperations (x) vs number of defections (1 - x)
	columns_to_ignore = list(set(range(15)) - {2}) # the other one is 1 - x
	custom_legend = ['Cooperative Actions', 'Defections']
	file_name = 'results'
elif graph_opt == 8:
	# number of cooperations (x) vs number of defections (1 - x)
	columns_to_ignore = [1]
	custom_legend = ['Unique Opponents', 'Games With Same Opponent']
	file_name = 'diff_games'
elif graph_opt == 9:
	# proportion of agents alive
	columns_to_ignore = []
	custom_legend = ['Alive Proportion']
	file_name = 'alive'
else:
	# specify columns_to_ignore and custom_legend manually
	columns_to_ignore = [0,1,2,3]+(range(6,15))
	custom_legend = ['Group-Entitative Agents', 'Individual-Entitative Agents']
	file_name = 'results'

file_to_plot = 'results/init234_mu005/'+file_name+'_PD_b0.03c0.01_g4_i1_m'+str(mobility_prob)+'_mr50_numneighs4_init'+str(init)+'_pairallneighs_avg.txt'
#file_to_plot = 'results/only_ent_results/tagCounts_PD_b0.03c0.01_g4_i1_m0.0_mr50_numneighs4_pairallneighs_avg.txt'
f_in = open(file_to_plot, "rb")

# specify which columns to not plot
#columns_to_ignore = [0,1,3]+(range(6,15))
#columns_to_ignore = [0,1,2,3]+(range(6,15))
#columns_to_ignore = [1]
#columns_to_ignore = [0,2]
#columns_to_ignore = []
#columns_to_ignore = list(set(range(15)) - {0,1,2})

#custom_legend = ['Cooperative Actions', 'Group-Entitative Agents', 'Individualistic Agents']
#custom_legend = ['Group-Entitative Agents', 'Individual-Entitative Agents']
#custom_legend = ['Unique Opponents', 'Games With Same Opponent']
#custom_legend = ['clustering coefficient']
#custom_legend = ['Always Cooperate', 'Tit-for-Tat', 'Opp of Tit-for-Tat', 'Always Defect']
#custom_legend = ['AllC', 'TFT', 'OTFT', 'AllD']
#custom_legend = ['Tit-for-Tat', 'Always Defect']
#custom_legend = ['In-Group Defection', 'Out-Group Defection']
#custom_legend = ['In-Group Defection', 'Out-Group Defection', 'Cooperative Actions']

colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', '0.3']
linestyles=['-', '--']
markers = ['o', 's', '*', 'v', '^', '+', 'x', '>', '<']

#x_values = list()
y_values = list()

first_row = 1
idx = 0
for r in f_in:
	if first_row == 1:
		header_str = r.rstrip()
		header_str_list = header_str.split(',')
		header_list = [header_str_list[i] for i in range(len(header_str_list)) if i not in columns_to_ignore]
		first_row = 0
		continue
	#x_values.append(s.mp[idx])
	value_str = r.rstrip()
	value_str_list = value_str.split(',')
	value_list = [float(value_str_list[i]) for i in range(len(value_str_list)) if i not in columns_to_ignore]
	y_values.append(value_list)
	idx += 1
y_values = map(list, zip(*y_values))

#y_values[0] = [1-x for x in y_values[0]]
#y_values[1] = [1-x for x in y_values[1]]

for i in range(len(y_values)):
	temp_list = list(y_values[i])
	temp_list.append(y_values[i][total_generations-1])
	plt.plot(range(0, total_generations+1, 100), temp_list[0::100], linestyle=linestyles[i/len(colors)], color=colors[i%len(colors)], linewidth=3.0)
plt.xlim(0., total_generations)
plt.xlabel('Time').set_size(18)
plt.ylabel('Population %').set_size(18)
if 'diff_games' not in file_to_plot:
	plt.yticks(np.arange(0,1.1,0.1))
plt.tick_params(axis='both', which='major', labelsize=14)
#leg = plt.legend(header_list, prop={'size':18})
#leg = plt.legend(custom_legend, prop={'size':18})
leg = plt.legend(custom_legend, bbox_to_anchor=(0.9, 0.6),bbox_transform=plt.gcf().transFigure, prop={'size':18})
for leg_obj in leg.legendHandles:
	leg_obj.set_linewidth(5.0)
plt.grid(b=True, which='both', color='0.65',linestyle='-')
#plt.title('Group-Entitative Out-Group Strategy Proportions', fontsize = 18)
#plt.title('Individualistic Strategy Proportions', fontsize = 18)
#plt.title(str('Group-Entitative Out-Group Strategies (Mobility '+str(actual_mobility_prob)+')'), fontsize = 18)
#plt.title(str('Individual-Entitative Strategies (Mobility '+str(actual_mobility_prob)+')'), fontsize = 18)
plt.title(str('Group-Entitative vs. Individual-Entitative (Mobility '+str(actual_mobility_prob)+')'), fontsize = 18)
plt.show()
