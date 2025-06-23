# OFFICIAL 13/06/2025
import tigramite
from tigramite import data_processing as pp
from tigramite.pcmci import PCMCI
from tigramite.independence_tests.cmiknn import CMIknn
from tigramite import plotting as tp

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import multiprocessing

# Crear carpeta de salida si no existe
# output_dir = "results"
output_dir = "results"
os.makedirs(output_dir, exist_ok=True)

# Función para convertir el grafo en matriz de adyacencia
def process_graph(graph, i):
    graph_i = graph[:,:,i]
    result = np.zeros_like(graph_i, dtype=int)
    result[graph_i == '-->'] = 1
    result[graph_i == '<--'] = -1
    result[graph_i == 'o-o'] = 2
    return result

# Función para obtener matriz de adyacencia con pesos
def update_adj_matrix_weighted(new_graph, val_matrix):
    n = new_graph.shape[0]
    adj_matrix_dir = np.zeros((n, n))
    adj_matrix_weighted = np.zeros((n, n))
    adj_matrix_dir[new_graph == 1] = 1
    adj_matrix_dir.T[new_graph == -1] = 1
    adj_matrix_dir[new_graph == 2] = 2
    for i in range(n):
        for j in range(n):
            if new_graph[i, j] != 0:
                adj_matrix_weighted[i, j] = val_matrix[i, j]
    return adj_matrix_dir, adj_matrix_weighted

# Función que ejecuta PCMCI+ en paralelo
def run_pcmci(data_bar):
    try:
        nombre = str(data_bar[0])
        diagname = str(data_bar[1]['y_eff'].iloc[0])  # Se usa iloc[0] para evitar errores
        print(f'Procesando grupo: {nombre} (diagnosis: {diagname})')

        data_bar1 = data_bar[1].drop(columns=['ID', 'y_eff'])
        new_data = np.array(data_bar1, dtype=np.float64)
        
        # Inicializar dataframe en Tigramite
        var_names = data_bar1.columns
        dataframe = pp.DataFrame(new_data, var_names=var_names)

        # Configurar el test de independencia
        cmiknn = CMIknn(
            knn=4,
            shuffle_neighbors=5,
            significance='shuffle_test',
            transform='ranks',
            workers=8
        )

        # Ejecutar PCMCI+
        pcmci = PCMCI(dataframe=dataframe, cond_ind_test=cmiknn, verbosity=0)
        tau_max = 1
        pc_alpha = 0.01
        results = pcmci.run_pcmciplus(tau_min=0, tau_max=tau_max, pc_alpha=pc_alpha)

        # Guardar gráfico de PCMCI+
        plt.figure(figsize=(8, 8))
        tp.plot_graph(
            val_matrix=results['val_matrix'],
            graph=results['graph'],
            var_names=var_names,
            link_colorbar_label='cross-MCI (edges)',
            node_colorbar_label='auto-MCI (nodes)',
            arrow_linewidth=3,
            node_label_size=8,
            node_size=0.1,
            tick_label_size=8
        )
        plt.tight_layout()
        plot_filename = os.path.join(output_dir, f'pcmci_plus_{nombre}.png')
        plt.savefig(plot_filename)
        plt.close()
        print(f"Gráfico guardado en {plot_filename}")

        # Guardar matrices de adyacencia
        for i in range(tau_max + 1):
            val_matrix = results['val_matrix'][:,:,i]
            graph = results['graph']
            adj_matrix_dir = update_adj_matrix_weighted(process_graph(graph,i),val_matrix)[0]
            adj_matrix_weighted = update_adj_matrix_weighted(process_graph(graph,i),val_matrix)[1]
            adj_filename_dir = os.path.join(output_dir, f'adj_{nombre}_lag{i}_dir.csv')
            adj_filename_weighted = os.path.join(output_dir, f'adj_{nombre}_lag{i}_weighted.csv')
            np.savetxt(adj_filename_dir, adj_matrix_dir, delimiter=",", fmt="%.6f", header=",".join(var_names))
            np.savetxt(adj_filename_weighted, adj_matrix_weighted, delimiter=",", fmt="%.6f", header=",".join(var_names))

    except Exception as e:
        print(f"Error en el grupo {data_bar[0]}: {str(e)}")

# Cargar datos
folder = '/Users/ele/Desktop/codici_finali/dataset/'
data = pd.read_csv(os.path.join(folder, 'general_data.csv'))
data = data.drop(columns = ['Unnamed: 0'])
data.columns = ['Felt.energetic', 'Felt.enthusiastic', 'Felt.content', 'Felt.irritable',
       'Felt.restless', 'Felt.worried', 'Felt.worthless.or.guilty',
       'Felt.frightened.or.afraid', 'Experienced.loss.of.interest.or.pleasure',
       'Felt.angry', 'Felt.hopeless', 'Felt.down.or.depressed',
       'Felt.positive', 'Felt.fatigued', 'Experienced.muscle.tension',
       'Had.difficulty.concentrating', 'Felt.accepted.or.supported',
       'Felt.threatened..judged..or.intimidated', 'Dwelled.on.the.past',
       'Avoided.activities', 'Procrastinated', 'Avoided.people', 'ID',
       'y_eff']
groups = list(data.groupby('ID'))  # Convertir a lista para evitar problemas con multiprocessing en Windows

# Ejecutar PCMCI+ en paralelo en Windows
if __name__ == '__main__':
    multiprocessing.freeze_support()  # Necesario para Windows
    with multiprocessing.Pool(processes=4) as pool:  # Ajusta el número de procesos
        pool.map(run_pcmci, groups)