import pandas as pd
import os
import numpy as np
folder = '/Users/ele/Desktop/napoli_acc/dati/4_fisher/Fisher/'
y_tot = pd.read_csv(os.path.join(folder,'y_tot.csv'), header = None)
y_tot.columns = ['y_eff']
subfolders = [f for f in os.listdir(folder) if os.path.isdir(os.path.join(folder, f))]
cont = 0
general_list = []
l = []
r = []
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
        if data_bar.columns[-3:].tolist() == ['Avoided.activities', 'Procrastinated', 'Avoided.people']:
            new_order = ['Procrastinated','Avoided.people', 'Avoided.activities']
            cols_to_reverse = ['Avoided.activities', 'Procrastinated', 'Avoided.people']
            cols = list(data_bar.columns)  
            idx = [cols.index(c) for c in cols_to_reverse] 
            cols[idx[0]:idx[-1]+1] = new_order
            data_bar = data_bar[cols]
        data_bar.columns = ['Felt.energetic', 'Felt.enthusiastic', 'Felt.content', 'Felt.irritable',
       'Felt.restless', 'Felt.worried', 'Felt.worthless.or.guilty',
       'Felt.frightened.or.afraid', 'Experienced.loss.of.interest.or.pleasure',
       'Felt.angry', 'Felt.hopeless', 'Felt.down.or.depressed',
       'Felt.positive', 'Felt.fatigued', 'Experienced.muscle.tension',
       'Had.difficulty.concentrating', 'Felt.accepted.or.supported',
       'Felt.threatened..judged..or.intimidated', 'Dwelled.on.the.past',
       'Avoided.activities', 'Procrastinated', 'Avoided.people', 'ID']
        # Remove missing values
        l.append(data_bar.isna().sum().max())
        data_bar = data_bar.dropna()
        r.append(data_bar.shape[0])
        for col in data_bar.columns[:-1]:
            data_bar[col] = (data_bar[col] - data_bar[col].mean())/data_bar[col].std()
        general_list.append(data_bar)
r_mean = np.mean(r)
l_mean = np.mean(l)
r_std = np.std(r)
l_std = np.std(l)
general_data = pd.concat(general_list, axis = 0, ignore_index=True)
general_data['y_eff'] = y_tot['y_eff']
import pdb; pdb.set_trace()
general_data.to_csv('general_data.csv')