# for fusion mixed graph plots
# Import libraries
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import numpy as np
import os
from sklearn.preprocessing import StandardScaler
from matplotlib.colors import ListedColormap
from cdlib import algorithms
import matplotlib.lines as mlines

# datos
folder = '/Users/ele/Desktop/napoli_acc/dati/4_fisher/Fisher/'
new_folder = '/Users/ele/Desktop/codici_finali/pcmci+/results/'
new_folder_2 = '/Users/ele/Desktop/codici_finali/pcmci+/results_fusion_2/'
new_folder_fusion = '/Users/ele/Desktop/codici_finali/pcmci+/results_fusion/'
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
MDD = ['P014', 'P019','P072', 'P074', 'P137', 'P139', 'P163', 'P169', 'P220', 'P223', 'P244']
GAD_MDD = ['P001','P003', 'P006', 'P007', 'P008', 'P010',
'P013', 'P048', 'P115', 'P117', 'P203']
GAD = [sub for sub in sorted(subfolders)[:45] if sub not in MDD and sub not in GAD_MDD]
diagnosis = ['GAD', 'MDD', 'GAD_MDD']
for diag_str in diagnosis:
    if diag_str == 'GAD':
        diag = GAD
    elif diag_str == 'MDD':
        diag = MDD
    else:
        diag = GAD_MDD
    # 22x22 matrices for directed and undirected links
    count_directed = np.zeros((22, 22))
    count_undirected = np.zeros((22, 22))
    count_lag_0 = np.zeros((22, 22))
    count_lag_1 = np.zeros((22, 22))
    count = np.zeros((22, 22))
    for subfolder in diag:
        file_name_0_dir = 'adj_'+ subfolder + '_lag0_dir.csv'
        file_name_1_dir = 'adj_'+ subfolder + '_lag1_dir.csv'
        #file_name_0_weighted = 'adj_'+ subfolder + '_lag0_weighted.csv'
        #file_name_1_weighted = 'adj_'+ subfolder + '_lag1_weighted.csv'
        adj_0_dir = pd.read_csv(os.path.join(new_folder,file_name_0_dir))
        adj_1_dir = pd.read_csv(os.path.join(new_folder,file_name_1_dir))
        #adj_0_weighted = pd.read_csv(os.path.join(new_folder,file_name_0_weighted))
        #adj_1_weighted = pd.read_csv(os.path.join(new_folder,file_name_1_weighted))
        # dejar: removing lag 0 loops
        np.fill_diagonal(adj_0_dir.values, 0)
        #np.fill_diagonal(adj_0_weighted.values, 0)
        #lags 0 and 1:
        adj_dir = adj_1_dir + adj_0_dir
        #adj_weighted = adj_1_weighted + adj_0_weighted
        lag = '0y1'
        # quitar:
        adj_dir.rename(columns={'# Felt.energetic': 'Felt.energetic'}, inplace=True)
        adj_0_dir.rename(columns={'# Felt.energetic': 'Felt.energetic'}, inplace=True)
        adj_1_dir.rename(columns={'# Felt.energetic': 'Felt.energetic'}, inplace=True)
        #adj_weighted.rename(columns={'# Felt.energetic': 'Felt.energetic'}, inplace=True)
        if adj_dir.columns[-3:].tolist() == ['Avoided.activities', 'Procrastinated', 'Avoided.people']:
            new_order = ['Procrastinated','Avoided.people', 'Avoided.activities']
            cols_to_reverse = ['Avoided.activities', 'Procrastinated', 'Avoided.people']
            cols = list(adj_dir.columns)  
            idx = [cols.index(c) for c in cols_to_reverse] 
            cols[idx[0]:idx[-1]+1] = new_order
            adj_dir = adj_dir[cols]
            adj_dir.columns = var_names
        # if adj_weighted.columns[-3:].tolist() == ['Avoided.activities', 'Procrastinated', 'Avoided.people']:
        #     new_order = ['Procrastinated','Avoided.people', 'Avoided.activities']
        #     cols_to_reverse = ['Avoided.activities', 'Procrastinated', 'Avoided.people']
        #     cols = list(adj_weighted.columns)  
        #     idx = [cols.index(c) for c in cols_to_reverse] 
        #     cols[idx[0]:idx[-1]+1] = new_order
        #     adj_weighted = adj_weighted[cols]
        #     adj_weighted.columns = var_names
        # dejar: counting directed and undirected links separately
        mask_directed = adj_dir == 1
        count_directed += mask_directed
        mask_undirected = adj_dir == 2
        count_undirected += mask_undirected
        mask_lag_0 = adj_0_dir != 0
        count_lag_0 += mask_lag_0
        mask_lag_1 = adj_1_dir != 0
        count_lag_1 += mask_lag_1
        # counting directed and undirected links together for the graph kernel in R:
        mask = adj_dir != 0
        count += mask
    count_directed = count_directed / len(diag)
    count_undirected = count_undirected / len(diag)
    count = count / len(diag)
    count_lag_0 = count_lag_0 / len(diag)
    count_lag_1 = count_lag_1 / len(diag)
    # Saving count:
    count.to_csv(os.path.join(new_folder_fusion,lag+'_count_'+str(diag_str)+'.csv'))
    count_directed = count_directed[count_directed > 0]
    count_undirected = count_undirected[count_undirected > 0]
    count_directed.fillna(0, inplace=True)
    count_undirected.fillna(0, inplace=True)
    # Cambiar el nombre:
    count_directed.to_csv(os.path.join(new_folder_fusion,lag+'_count_dir'+str(diag_str)+'.csv'))
    count_undirected.to_csv(os.path.join(new_folder_fusion,lag+'_count_undir'+str(diag_str)+'.csv'))
    # Creating the mixed graph
    G = nx.MultiDiGraph()
    for i, var in enumerate(var_names):
        G.add_node(i, label=var)
    for i in range(22):
        for col in var_names:
            j = np.where(np.array(var_names) == col)[0][0]
            if count_directed[col][i] != 0 and count_lag_0[col][i] != 0:
                G.add_edge(i, j, weight=count_directed[col][i], type = "directed", style = "dashed") # da i a j
            elif count_directed[col][i] != 0 and count_lag_1[col][i] != 0:
                G.add_edge(i, j, weight=count_directed[col][i], type = "directed", style = "solid") # da i a j
            elif count_undirected[col][i] != 0 and count_lag_0[col][i] != 0:
                G.add_edge(i, j, weight=count_undirected[col][i], type = "undirected", style = "dashed") # indiretto
            elif count_undirected[col][i] != 0 and count_lag_1[col][i] != 0:
                G.add_edge(i, j, weight=count_undirected[col][i], type = "undirected", style = "solid")
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
    label3_offset = (0.05, 0.01)
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
    plt.figure(figsize=(8, 8))
    nx.draw_networkx_nodes(G, pos, node_size=600, node_color='lightblue', alpha=0.9)#, cmap=color_map)
    nx.draw_networkx_labels(G, labels_pos, labels={i: var for i, var in enumerate(var_names)}, font_size=7)
    # if len(G.edges) != 0:
    #     edge_colors = ['blue' if G[u][v]['weight'] > 0 else 'red' for u, v in G.edges]
    #     edge_widths = [abs(G[u][v]['weight'])*10 for u, v in G.edges]
    #     nx.draw_networkx_edges(G, pos, edgelist=edges, arrowstyle='-|>', arrowsize=10, edge_color=edge_colors,
    #         edge_cmap=plt.cm.Blues, width=edge_widths, min_source_margin=10, min_target_margin=10)
    if G.number_of_edges() > 0:
        #edge_colors = ['blue' if G[u][v][k]['weight'] > 0 else 'red' for u, v, k in G.edges(keys=True)]
        
        # OLD VERSION:
        #directed_edges = [(u, v, k) for u, v, k in G.edges(keys=True) if G[u][v][k].get("type") == "directed"]
        #undirected_edges = [(u, v, k) for u, v, k in G.edges(keys=True) if G[u][v][k].get("type") == "undirected"]
        # nx.draw_networkx_edges(
        #     G, pos, edgelist=[(u, v) for u, v, k in directed_edges], 
        #     edge_color='blue', edge_cmap=plt.cm.Blues, width=directed_widths, 
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
        undirected_dashed_edges = nx.draw_networkx_edges(
            G, pos, edgelist=[(u, v) for u, v, k in undirected_dashed],
            edge_color='gray', width=undirected_dashed_widths,
            style='dashed', arrows = False, arrowsize=10, min_source_margin=10, min_target_margin=10
        )
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

    # legend_handles = [
    # mlines.Line2D([], [], color='blue', linewidth=2, linestyle='dashed', label='Lag 0 directed'),
    # mlines.Line2D([], [], color='blue', linewidth=2, linestyle='solid', label='Lag 1 directed'),
    # mlines.Line2D([], [], color='gray', linewidth=2, linestyle='dashed', label='Lag 0 undirected'),
    # ]
    # plt.legend(handles=legend_handles, loc='upper left', fontsize=12, frameon=True)

    #plt.title(str(diag_str), fontsize=16)
    plt.axis('off')
    plt.tight_layout()
    print(G.in_degree())
    #plt.show()
    new_file = 'lag'+lag+'_'+str(diag_str)+'_pcmci+_'+'.png'
    plt.savefig(os.path.join(new_folder_2,new_file), dpi = 600)
    plt.close()