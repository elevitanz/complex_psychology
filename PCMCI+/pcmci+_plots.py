# Importante
# Import libraries
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import numpy as np
import os
from sklearn.preprocessing import StandardScaler
from matplotlib.colors import ListedColormap
from cdlib import algorithms

folder = '/Users/ele/Desktop/napoli_acc/dati/4_fisher/Fisher/'
new_folder = '/Users/ele/Desktop/codici_finali/pcmci+/results/'
new_folder_2 = '/Users/ele/Desktop/codici_finali/pcmci+/results_plot/'
new_folder_3 = '/Users/ele/Desktop/codici_finali/pcmci+/results_plot_2/'
subfolders = [f for f in os.listdir(folder) if os.path.isdir(os.path.join(folder, f))]
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

for subfolder in sorted(subfolders)[:45]:
    # adj_{nombre}_lag{i}_dir.csv
    file_name_0_dir = 'adj_'+ subfolder + '_lag0_dir.csv'
    file_name_1_dir = 'adj_'+ subfolder + '_lag1_dir.csv'
    file_name_0_weighted = 'adj_'+ subfolder + '_lag0_weighted.csv'
    file_name_1_weighted = 'adj_'+ subfolder + '_lag1_weighted.csv'
    adj_0_dir = pd.read_csv(os.path.join(new_folder,file_name_0_dir))
    adj_1_dir = pd.read_csv(os.path.join(new_folder,file_name_1_dir))
    adj_0_weighted = pd.read_csv(os.path.join(new_folder,file_name_0_weighted))
    adj_1_weighted = pd.read_csv(os.path.join(new_folder,file_name_1_weighted))
    adj_dir = adj_0_dir + adj_1_dir
    adj_weighted = adj_0_weighted + adj_1_weighted
    adj_dir.rename(columns={'# Felt.energetic': 'Felt.energetic'}, inplace=True)
    adj_0_dir.rename(columns={'# Felt.energetic': 'Felt.energetic'}, inplace=True)
    adj_1_dir.rename(columns={'# Felt.energetic': 'Felt.energetic'}, inplace=True)
    adj_weighted.rename(columns={'# Felt.energetic': 'Felt.energetic'}, inplace=True)
    if adj_dir.columns[-3:].tolist() == ['Avoided.activities', 'Procrastinated', 'Avoided.people']:
        new_order = ['Procrastinated','Avoided.people', 'Avoided.activities']
        cols_to_reverse = ['Avoided.activities', 'Procrastinated', 'Avoided.people']
        cols = list(adj_dir.columns)  
        idx = [cols.index(c) for c in cols_to_reverse] 
        cols[idx[0]:idx[-1]+1] = new_order
        adj_dir = adj_dir[cols]
        adj_dir.columns = var_names
        new_order = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,20,21,19]
        adj_dir = adj_dir.loc[new_order]
        adj_dir.reset_index(inplace=True)
        adj_dir = adj_dir.drop(columns = ['index'])
    if adj_weighted.columns[-3:].tolist() == ['Avoided.activities', 'Procrastinated', 'Avoided.people']:
        new_order = ['Procrastinated','Avoided.people', 'Avoided.activities']
        cols_to_reverse = ['Avoided.activities', 'Procrastinated', 'Avoided.people']
        cols = list(adj_weighted.columns)  
        idx = [cols.index(c) for c in cols_to_reverse] 
        cols[idx[0]:idx[-1]+1] = new_order
        adj_weighted = adj_weighted[cols]
        adj_weighted.columns = var_names
        new_order = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,20,21,19]
        adj_weighted = adj_weighted.loc[new_order]
        adj_weighted.reset_index(inplace=True)
        adj_weighted = adj_weighted.drop(columns = ['index'])
    adj_dir.to_csv(os.path.join(new_folder_3,'adj_'+ subfolder + '_lag0y1_dir.csv'))
    adj_weighted.to_csv(os.path.join(new_folder_3,'adj_'+ subfolder + '_lag0y1_weighted.csv'))
    #G = nx.DiGraph()
    G = nx.MultiDiGraph()
    for i, var in enumerate(var_names):
        G.add_node(i, label=var)
    for i in range(22):
        for col in var_names:
            j = np.where(np.array(var_names) == col)[0][0]
            if adj_weighted[col][i] != 0 and adj_dir[col][i] == 1 and adj_1_dir[col][i] != 0:
                G.add_edge(i, j, weight=adj_weighted[col][i], type = "directed", style = "solid") # da i a j
            elif adj_weighted[col][i] != 0 and adj_dir[col][i] == 2 and adj_1_dir[col][i] != 0:
                G.add_edge(i, j, weight=adj_weighted[col][i], type = "undirected", style = "solid") # indiretto
            elif adj_weighted[col][i] != 0 and adj_dir[col][i] == 1 and adj_0_dir[col][i] != 0:
                G.add_edge(i, j, weight=adj_weighted[col][i], type = "directed", style = "dashed") # da i a j
            elif adj_weighted[col][i] != 0 and adj_dir[col][i] == 2 and adj_0_dir[col][i] != 0:
                G.add_edge(i, j, weight=adj_weighted[col][i], type = "undirected", style = "dashed") # indiretto

    if G.number_of_edges() > 0:
        edges, weights = zip(*nx.get_edge_attributes(G, 'weight').items())
    G_undirected = G.to_undirected()
    communities = algorithms.walktrap(G_undirected)
    partition = communities.to_node_community_map()
    unique_communities = list(partition.values())
    color_map = ListedColormap(plt.cm.tab20.colors[:len(unique_communities)])
    node_colors = [unique_communities.index(partition[node]) for node in G.nodes]
    pos = nx.circular_layout(G)
    node1_to_adjust = 17
    label1_offset = (0.05, -0.07)
    node2_to_adjust = 16
    label2_offset = (-0.05, 0.0)
    node3_to_adjust = 5
    label3_offset = (0.05, -0.02)
    node4_to_adjust = 6
    label4_offset = (-0.05, 0.02)
    node5_to_adjust = 11
    label5_offset = (0.09, 0.0)
    labels_pos = {i: pos[i] for i in pos}
    labels_pos[node1_to_adjust] = (pos[node1_to_adjust][0] + label1_offset[0], 
        pos[node1_to_adjust][1] + label1_offset[1])
    labels_pos[node2_to_adjust] = (pos[node2_to_adjust][0] + label2_offset[0], 
        pos[node2_to_adjust][1] + label2_offset[1])
    labels_pos[node3_to_adjust] = (pos[node3_to_adjust][0] + label3_offset[0], 
        pos[node3_to_adjust][1] + label3_offset[1])
    labels_pos[node4_to_adjust] = (pos[node4_to_adjust][0] + label4_offset[0], 
        pos[node4_to_adjust][1] + label4_offset[1])
    labels_pos[node5_to_adjust] = (pos[node5_to_adjust][0] + label5_offset[0], 
        pos[node5_to_adjust][1] + label5_offset[1])
    plt.figure(figsize=(12, 12))
    nx.draw_networkx_nodes(G, pos, node_size=600, node_color='lightblue', alpha=0.9, cmap=color_map)
    nx.draw_networkx_labels(G, labels_pos, labels={i: var for i, var in enumerate(var_names)}, font_size=10)
    if G.number_of_edges() > 0:
        # Old version:
        # directed_edges = [(u, v, k) for u, v, k in G.edges(keys=True) if G[u][v][k].get("type") == "directed"]
        # undirected_edges = [(u, v, k) for u, v, k in G.edges(keys=True) if G[u][v][k].get("type") == "undirected"]
        # directed_widths = [abs(G[u][v][k]['weight']) * 10 for u, v, k in directed_edges]
        # undirected_widths = [abs(G[u][v][k]['weight']) * 10 for u, v, k in undirected_edges]
        # nx.draw_networkx_edges(
        #     G, pos, edgelist=[(u, v) for u, v, k in directed_edges], 
        #     edge_color='lightblue', edge_cmap=plt.cm.Blues, width=directed_widths, 
        #     arrowstyle='-|>', arrowsize=10, min_source_margin=10, min_target_margin=10
        # )
        # nx.draw_networkx_edges(
        #     G, pos, edgelist=[(u, v) for u, v, k in undirected_edges], 
        #     edge_color='gray', width=undirected_widths, arrowstyle='-'
        # )
        directed_solid = [(u, v, k) for u, v, k in G.edges(keys=True) if G[u][v][k].get("type") == "directed" and G[u][v][k].get("style") == "solid"]
        directed_dashed = [(u, v, k) for u, v, k in G.edges(keys=True) if G[u][v][k].get("type") == "directed" and G[u][v][k].get("style") == "dashed"]
        undirected_solid = [(u, v, k) for u, v, k in G.edges(keys=True) if G[u][v][k].get("type") == "undirected" and G[u][v][k].get("style") == "solid"]
        undirected_dashed = [(u, v, k) for u, v, k in G.edges(keys=True) if G[u][v][k].get("type") == "undirected" and G[u][v][k].get("style") == "dashed"]


        directed_solid_widths = [abs(G[u][v][k]['weight']) * 10 for u, v, k in directed_solid]
        directed_dashed_widths = [abs(G[u][v][k]['weight']) * 10 for u, v, k in directed_dashed]
        undirected_solid_widths = [abs(G[u][v][k]['weight']) * 10 for u, v, k in undirected_solid]
        undirected_dashed_widths = [abs(G[u][v][k]['weight']) * 10 for u, v, k in undirected_dashed]

        # Undirected solid
        nx.draw_networkx_edges(
            G, pos, edgelist=[(u, v) for u, v, k in undirected_solid],
            edge_color='gray', width=undirected_solid_widths,
            style='solid', arrows=False, arrowsize=10, min_source_margin=10, min_target_margin=10
        )

        # Undirected dashed
        undirected_dashed_edges =  nx.draw_networkx_edges(
            G, pos, edgelist=[(u, v) for u, v, k in undirected_dashed],
            edge_color='gray', width=undirected_dashed_widths,
            style='dashed', arrows = False, arrowsize=10, min_source_margin=10, min_target_margin=10
        )
        if isinstance(undirected_dashed_edges, list):
            for e in undirected_dashed_edges:
                e.set_dashes((8, 8))
        else:
            undirected_dashed_edges.set_linestyle((0, (8, 8)))
        
        # Directed solid
        nx.draw_networkx_edges(
            G, pos, edgelist=[(u, v) for u, v, k in directed_solid],
            edge_color='blue', edge_cmap=plt.cm.Blues, width=directed_solid_widths,
            style='solid', arrows=True, arrowsize=10, min_source_margin=10, min_target_margin=10
        )

        # Directed dashed
        nx.draw_networkx_edges(
            G, pos, edgelist=[(u, v) for u, v, k in directed_dashed],
            edge_color='blue', edge_cmap=plt.cm.Blues, width=directed_dashed_widths,
            style='dashed', arrows=True, arrowsize=10, min_source_margin=10, min_target_margin=10
        )

    plt.title(subfolder, fontsize=16)
    plt.axis('off')
    #plt.subplots_adjust(left=0.1, right=0.2, top=0.2, bottom=0.1)
    plt.tight_layout()
    #plt.show()
    new_file = 'pcmci+_'+subfolder+'.png'
    plt.savefig(os.path.join(new_folder_2,new_file), dpi=300)
    plt.close()