import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

new_folder = '/Users/ele/Desktop/codici_finali/network_metrics/results/'
# Carica i tre CSV
df_mdd = pd.read_csv(os.path.join(new_folder,"network_measures_MDD.csv"))
df_gad = pd.read_csv(os.path.join(new_folder,"network_measures_GAD.csv"))
df_gad_mdd = pd.read_csv(os.path.join(new_folder,"network_measures_GAD_MDD.csv"))
# Ordina i nodi per consistenza
nodes = df_mdd['Unnamed: 0']

# Liste per ciclo
metrics = ['In_Degree', 'Out_Degree', 'Degree_SUM', 'Closeness_SUM', 'Betweenness_SUM']
new_names = ['In Degree', 'Out Degree', 'Degree', 'Closeness Centrality', 'Betweenness Centrality']
rosella = '#eedbf2'
blu = '#0000ff'
azzurrino = '#b6d8eb'
colors = [rosella, blu, azzurrino]
labels = ['MDD', 'GAD', 'GAD_MDD']

# Imposta la posizione delle barre
x = np.arange(len(nodes))  # posizione base per ciascun nodo
width = 0.25  # larghezza di ogni barra

# Plot per ogni metrica
for i in range(len(metrics)):
    plt.figure(figsize=(16, 12))
    plt.bar(x - width, df_mdd[metrics[i]], width, label='MDD', color=colors[0])
    plt.bar(x, df_gad[metrics[i]], width, label='GAD', color=colors[1])
    plt.bar(x + width, df_gad_mdd[metrics[i]], width, label='Comorbidity', color=colors[2])

    # plt.title(f"Comparative Bar Chart: {metrics[i]}")
    # plt.xlabel("Symptoms")
    plt.xticks(x, nodes, rotation=90, fontsize=24)
    plt.yticks(fontsize=18)
    plt.ylabel(new_names[i], fontsize=28)
    plt.legend(fontsize=20)
    plt.tight_layout()
    # plt.show()
    plt.savefig(os.path.join(new_folder,metrics[i]+'.png'), dpi = 300)
