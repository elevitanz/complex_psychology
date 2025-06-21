# modifica per il discorso ordine colonne delle misure di complessità
import pandas as pd
import numpy as np
import os
df = pd.read_csv("resultados_rqa_crqa_complexity.csv")
old_columns = df.columns
folder = '/Users/ele/Desktop/napoli_acc/dati/4_fisher/Fisher/'
y_tot = pd.read_csv(os.path.join(folder,'diagnosis.txt'), delimiter = ' ')
diag = y_tot[['ID', 'Primary_diagnosis']]
mapping_diag = {'MDD,GAD': '3', 'GAD': '1', 'GAD,SAD':'1', 'GAD,Agor':'1', 'MDD':'2'}
diag['Primary_diagnosis'] = diag['Primary_diagnosis'].replace(mapping_diag)
mapping = {
    "Procrastinated": "TEMP_VALUE",  # Passaggio intermedio per evitare conflitti
    "Avoided.activities": "Procrastinated",
    "Avoided.people": "Avoided.activities",
    "TEMP_VALUE": "Avoided.people"
}

# Funzione per la sostituzione simultanea
def rename_columns(col):
    for old, new in mapping.items():
        col = col.replace(old, new)
    return col

# Applica la funzione a tutti i nomi di colonna
df.columns = [rename_columns(col) for col in old_columns]
df = df.drop(columns =['y_eff'])
# Merge basato sulla colonna 'ID'
df = df.merge(diag[['ID', 'Primary_diagnosis']], on='ID', how='left')
# Rinomina la colonna assegnando il nome 'y_eff'
df = df.rename(columns={'Primary_diagnosis': 'y_eff'})
df.to_csv("modified_resultados_rqa_crqa_complexity.csv")
