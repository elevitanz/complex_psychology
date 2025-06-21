import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import os

# Closeness.Centrality
# Betweenness.Centrality
# Degree
# In.Degree
# Out.Degree
new_folder_fusion = '/Users/ele/Desktop/codici_finali/pcmci+/results_fusion/'
new_folder = '/Users/ele/Desktop/codici_finali/network_metrics/results/'
var_names = ['Felt.energetic', 'Felt.enthusiastic', 'Felt.content', 'Felt.irritable',
        'Felt.restless', 'Felt.worried', 'Felt.worthless.or.guilty',
        'Felt.frightened.or.afraid',
        'Experienced.loss.of.interest.or.pleasure', 'Felt.angry', 
        'Felt.hopeless', 'Felt.down.or.depressed',
        'Felt.positive', 'Felt.fatigued', 'Experienced.muscle.tension', 
        'Had.difficulty.concentrating',
        'Felt.accepted.or.supported', 'Felt.threatened..judged..or.intimidated',
        'Dwelled.on.the.past', 'Procrastinated',
        'Avoided.people', 'Avoided.activities']

diaglist = ['GAD','MDD', 'GAD_MDD']
for diag in diaglist:
	dir_filename ='0y1_count_dir'+diag+'.csv'
	undir_filename ='0y1_count_undir'+diag+'.csv'
	dir_df = pd.read_csv(os.path.join(new_folder_fusion,dir_filename))
	dir_df.drop(columns=['Unnamed: 0'], inplace = True)
	undir_df = pd.read_csv(os.path.join(new_folder_fusion,undir_filename))
	undir_df.drop(columns=['Unnamed: 0'], inplace = True)
	dir_df.columns = var_names
	dir_df.index = var_names
	undir_df.columns = var_names
	undir_df.index = var_names
	G_dir = nx.from_pandas_adjacency(dir_df, create_using=nx.DiGraph)
	G_undir = nx.from_pandas_adjacency(undir_df, create_using=nx.Graph)
	# Calcola le misure
	in_deg = dict(G_dir.in_degree())
	out_deg = dict(G_dir.out_degree())
	sorted_in_deg = dict(sorted(in_deg.items()))
	sorted_out_deg = dict(sorted(out_deg.items()))
	degree_undir = dict(G_undir.degree())

	# Degree sommato: In + Out + Undir
	degree_sum = {
		node: in_deg.get(node, 0) + out_deg.get(node, 0) + degree_undir.get(node, 0)
		for node in set(G_dir.nodes())
	}
	sorted_degree_sum = dict(sorted(degree_sum.items()))

	# Closeness sommato
	closeness_dir = nx.closeness_centrality(G_dir)
	closeness_undir = nx.closeness_centrality(G_undir)
	closeness_sum = {
		node: closeness_dir.get(node, 0) + closeness_undir.get(node, 0)
		for node in set(G_dir.nodes())
	}
	sorted_closeness_sum = dict(sorted(closeness_sum.items()))

	# Betweenness sommato
	betweenness_dir = nx.betweenness_centrality(G_dir)
	betweenness_undir = nx.betweenness_centrality(G_undir)
	betweenness_sum = {
		node: betweenness_dir.get(node, 0) + betweenness_undir.get(node, 0)
		for node in set(G_dir.nodes())
	}
	sorted_betweenness_sum = dict(sorted(betweenness_sum.items()))

	# DataFrame finale
	results_df = pd.DataFrame({
		'In_Degree': pd.Series(sorted_in_deg),
		'Out_Degree': pd.Series(sorted_out_deg),
		'Degree_SUM': pd.Series(sorted_degree_sum),
		'Closeness_SUM': pd.Series(sorted_closeness_sum),
		'Betweenness_SUM': pd.Series(sorted_betweenness_sum),
	})
	# results_df.to_csv(os.path.join(new_folder,f'network_measures_{diag}.csv', index=False))
	results_df.to_csv(os.path.join(new_folder,f'network_measures_{diag}.csv'))