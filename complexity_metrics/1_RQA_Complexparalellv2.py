# misure di complessità calcolate sui dati normalizzati
import pandas as pd
import numpy as np
import itertools
from scipy.spatial.distance import pdist, squareform, cdist
from tqdm import tqdm
from multiprocessing import Pool, cpu_count
import nolds
import antropy as ant
from pyrqa.time_series import TimeSeries
from pyrqa.analysis_type import Classic, Cross
from pyrqa.settings import Settings
from pyrqa.neighbourhood import FixedRadius
from pyrqa.computation import RQAComputation
import os
import warnings
from sklearn.exceptions import UndefinedMetricWarning
warnings.simplefilter("ignore", category=UndefinedMetricWarning)


# ✅ Función para calcular el radio en RQA
def calcular_radio(ts, embedding_dim, target_rr):
    ts = np.array(ts, dtype=np.float64)
    ts = ts[~np.isnan(ts) & np.isfinite(ts)]
    if len(ts) < embedding_dim * 2:
        return np.nan
    embedded_ts = np.array([ts[i:i + embedding_dim] for i in range(len(ts) - embedding_dim + 1)])
    dist_values = squareform(pdist(embedded_ts, metric='euclidean'))[np.triu_indices(len(embedded_ts), k=1)]
    return np.percentile(dist_values, target_rr * 100)


# ✅ Función para calcular el radio en CRQA
def calcular_radiocros(ts1, ts2, embedding_dim, target_rr):
    ts1, ts2 = map(lambda x: np.array(x, dtype=np.float64), (ts1, ts2))
    ts1, ts2 = ts1[~np.isnan(ts1) & np.isfinite(ts1)], ts2[~np.isnan(ts2) & np.isfinite(ts2)]

    if len(ts1) < embedding_dim * 2 or len(ts2) < embedding_dim * 2:
        return np.nan

    embedded_ts1 = np.array([ts1[i:i + embedding_dim] for i in range(len(ts1) - embedding_dim + 1)])
    embedded_ts2 = np.array([ts2[i:i + embedding_dim] for i in range(len(ts2) - embedding_dim + 1)])
    dist_matrix = cdist(embedded_ts1, embedded_ts2, metric='euclidean')
    dist_values = dist_matrix[np.triu_indices_from(dist_matrix, k=1)]
    
    return np.percentile(dist_values, target_rr * 100)


# ✅ Función para calcular métricas de complejidad
def calcular_complejidad(ts, embedding_dim):
    ts = np.array(ts, dtype=np.float64)
    ts = ts[~np.isnan(ts) & np.isfinite(ts)]

    if len(ts) < embedding_dim * 2:
        return {k: np.nan for k in [
            "Lyapunov Exp", "Shannon Entropy", "Perm Entropy", "Sample Entropy",
            "Appr Entropy", "Hurst Exponent", "DFA", "Corr Dim", "Kaplan-Yorke Dim",
            "Higuchi FD", "Petrosian FD", "LZC","Number of zero crossings"
        ]}
    #import pdb;pdb.set_trace()
    try:
        return {
            #"Lyapunov Exp": nolds.lyap_r(ts, emb_dim=embedding_dim),
            #"Shannon Entropy": ant.shannon_entropy(ts),
            "Number of zero crossings": ant.num_zerocross(ts),
            "Perm Entropy": ant.perm_entropy(ts),
            "Sample Entropy": ant.sample_entropy(ts),
            "Appr Entropy": ant.app_entropy(ts),
            "Hurst Exponent": nolds.hurst_rs(ts),
            "DFA": nolds.dfa(ts),
            "Corr Dim": nolds.corr_dim(ts, embedding_dim),
            #"Kaplan-Yorke Dim": nolds.kaplan_yorke(ts),
            "Higuchi FD": ant.higuchi_fd(ts),
            "Petrosian FD": ant.petrosian_fd(ts),
            #"LZC": ant.lziv_complexity(ts)
        }
    except:
        return {k: np.nan for k in calcular_complejidad(ts, embedding_dim).keys()}


# ✅ Función principal para procesar cada individuo
def procesar_individuo(args):
    individual_id, individuo_data, combinations = args
    results = []
    y_eff = individuo_data.iloc[0][["y_eff"]]

    for embedding_dim, time_delay, target_rr in combinations:
        row_results = {
            "ID": individual_id,
            "embedding_dim": embedding_dim,
            "time_delay": time_delay,
            "target_rr": target_rr
        }

        # 🔹 Cálculo de RQA y Complejidad para cada serie temporal
        for var_name in individuo_data.columns[0:22]:
            ts = individuo_data[var_name].dropna().values
            if len(ts) < embedding_dim * 2:
                continue

            radius = calcular_radio(ts, embedding_dim, target_rr)
            row_results[f"{var_name}_Radius"] = radius

            ts_rqa = TimeSeries(ts, embedding_dimension=embedding_dim, time_delay=time_delay)
            settings = Settings(ts_rqa, analysis_type=Classic, neighbourhood=FixedRadius(radius))
            result = RQAComputation.create(settings).run()

            #row_results.update({f"{var_name}_{metric}": getattr(result, metric) for metric in vars(result)})
            row_results.update({
                f"{var_name}_RecurrenceRate": result.recurrence_rate,
                f"{var_name}_Determinism": result.determinism,
                f"{var_name}_Laminarity": result.laminarity,
                f"{var_name}_TrappingTime": result.trapping_time,
                f"{var_name}_Lmax": result.longest_diagonal_line,
                f"{var_name}_Vmax": result.longest_vertical_line,
                f"{var_name}_Divergence": result.divergence,
                f"{var_name}_EntropyDiagonal": result.entropy_diagonal_lines,
                f"{var_name}_AvgDiagonalLength": result.average_diagonal_line,
                f"{var_name}_AvgVerticalLength": result.average_white_vertical_line
            })
            # 🔹 Calcular medidas de complejidad
            complejidad = calcular_complejidad(ts, embedding_dim)
            row_results.update({f"{var_name}_{key}": value for key, value in complejidad.items()})

        # 🔹 CRQA entre pares de series temporales
        for var1, var2 in itertools.combinations(individuo_data.columns[0:22], 2):
            ts1, ts2 = individuo_data[var1].dropna().values, individuo_data[var2].dropna().values
            if len(ts1) < embedding_dim * 2 or len(ts2) < embedding_dim * 2:
                continue

            radius_crqa = calcular_radiocros(ts1, ts2, embedding_dim, target_rr)
            ts_crqa = TimeSeries(np.column_stack((ts1, ts2)), embedding_dimension=embedding_dim, time_delay=time_delay)
            settings_crqa = Settings(ts_crqa, analysis_type=Cross, neighbourhood=FixedRadius(radius_crqa))
            result_crqa = RQAComputation.create(settings_crqa).run()

            #row_results.update({f"{var1}_vs_{var2}_{metric}": getattr(result_crqa, metric) for metric in vars(result_crqa)})
            row_results.update({
                f"{var1}_vs_{var2}_CrossRecurrenceRate": result_crqa.recurrence_rate,
                f"{var1}_vs_{var2}_CrossDeterminism": result_crqa.determinism,
                f"{var1}_vs_{var2}_CrossLaminarity": result_crqa.laminarity,
                f"{var1}_vs_{var2}_CrossTrappingTime": result_crqa.trapping_time,
                f"{var1}_vs_{var2}_CrossLmax": result_crqa.longest_diagonal_line,
                f"{var1}_vs_{var2}_CrossVmax": result_crqa.longest_vertical_line,
                f"{var1}_vs_{var2}_CrossDivergence": result_crqa.divergence,
                f"{var1}_vs_{var2}_CrossEntropyDiagonal": result_crqa.entropy_diagonal_lines,
                f"{var1}_vs_{var2}_CrossAvgDiagonalLength": result_crqa.average_diagonal_line,
                f"{var1}_vs_{var2}_CrossAvgVerticalLength": result_crqa.average_white_vertical_line
            })

        row_results.update({"y_eff": y_eff})
        results.append(row_results)

    return results


# ✅ Código principal
if __name__ == "__main__":
    # file_path = "C:/Users/Usuario/Dropbox/LinusBio/CHARGE_MARBLES_LDT2_with_metadata_ALL_UNBLINDED/dataLBdivS.csv"

    # data = pd.read_csv(file_path, low_memory=False, header=None)
    # data.columns=["ID","Li","Mg","Al","P","S","Ca","Mn","Cu","Zn","As","Sr","Ba","Pb",'age','sex','asd']
    # #data.iloc[:, 1:] = data.iloc[:, 1:].apply(pd.to_numeric, errors='coerce')
    folder = '/Users/ele/Desktop/napoli_acc/dati/4_fisher/Fisher/'
    y_tot = pd.read_csv(os.path.join(folder,'y_tot.csv'), header = None)
    y_tot.columns = ['y_eff']
    subfolders = [f for f in os.listdir(folder) if os.path.isdir(os.path.join(folder, f))]
    cont = 0
    general_list = []
    for subfolder in sorted(subfolders):
        if subfolder.startswith('P'):  # Checking for folders that start with 'P'
            cont += 1
            print(f'Accessing subfolder: {subfolder}')
            
            subfolder_path = os.path.join(folder, subfolder)
            
            # Read the data from the CSV file
            if not subfolder.startswith('P206'):
                data = pd.read_csv(os.path.join(subfolder_path, 'dat.csv'))
            else:
                data = pd.read_csv(os.path.join(subfolder_path, 'dat.csv'), delimiter = ';')
            # Remove the last 6 columns
            data = data.iloc[:, :-6]
            
            data['ID'] = [subfolder for i in range(len(data))]
            # Remove specific columns
            if not subfolder.startswith('P206'):
                data_bar = data.drop(columns=['Unnamed: 0','Sought.reassurance', 'Survey.Creation.Date', 'Survey.Completion.Date', 
                                              'How.many.hours.did.you.sleep.last.night', 'Experienced.difficulty.falling.or.staying.asleep',
                                              'Experienced.restless.or.unsatisfying.sleep'])
            else:
                data_bar = data.drop(columns=['Unnamed: 0','Survey.Creation.Date', 'Survey.Completion.Date', 
                                              'How.many.hours.did.you.sleep.last.night', 
                                              'Experienced.difficulty.falling.or.staying.asleep', 
                                              'Experienced.restless.or.unsatisfying.sleep'])
            data_bar.columns = ['Felt.energetic', 'Felt.enthusiastic', 'Felt.content', 'Felt.irritable',
           'Felt.restless', 'Felt.worried', 'Felt.worthless.or.guilty',
           'Felt.frightened.or.afraid', 'Experienced.loss.of.interest.or.pleasure',
           'Felt.angry', 'Felt.hopeless', 'Felt.down.or.depressed',
           'Felt.positive', 'Felt.fatigued', 'Experienced.muscle.tension',
           'Had.difficulty.concentrating', 'Felt.accepted.or.supported',
           'Felt.threatened..judged..or.intimidated', 'Dwelled.on.the.past',
           'Avoided.activities', 'Procrastinated', 'Avoided.people', 'ID']
            # Remove missing values
            data_bar = data_bar.dropna()
            for col in data_bar.columns[:-1]:
                data_bar[col] = (data_bar[col] - data_bar[col].mean())/data_bar[col].std()
            general_list.append(data_bar)

    data = pd.concat(general_list, axis = 0, ignore_index=True)
    data['y_eff'] = y_tot['y_eff']
    embedding_dims = [2, 3, 4, 5, 6]
    time_delays = [1, 2, 3, 4, 5]
    target_rrs = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    combinations = list(itertools.product(embedding_dims, time_delays, target_rrs))

    args_list = [(ind_id, data[data["ID"] == ind_id], combinations) for ind_id in data["ID"].unique()]

    args_temp = [('P001', data[data["ID"] == 'P001'], [combinations[0]])]
    aa = procesar_individuo(args_temp[0])
    
    with Pool(processes=cpu_count()) as pool:
        results = list(tqdm(pool.imap(procesar_individuo, args_list), total=len(args_list), desc="Procesando individuos"))

    df_results = pd.DataFrame([row for sublist in results for row in sublist])
    df_results.to_csv("resultados_rqa_crqa_complexity.csv", index=False, float_format="%.5f")


    print("✅ Resultados guardados en 'resultados_rqa_crqa_complexity.csv'")

