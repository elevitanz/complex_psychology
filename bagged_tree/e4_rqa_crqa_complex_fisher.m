% 2 classi dati statici
clear
Tabla = readtable('/Users/ele/Desktop/codici_finali/complexity_metrics/3_modified_resultados_rqa_crqa_complexity.csv', 'PreserveVariableNames', true);
Tabla(:,1) = [];
% Obtener los nombres de las variables de la tabla
vars = Tabla.Properties.VariableNames;
outertestdata = Tabla(Tabla.y_eff == 3, 1:end - 1);
%2 clases:
Tabla = Tabla(Tabla.y_eff ~= 3, :);
data1 = load('ROC1.mat');
%PARA SUBCANJUNTOS-TAMBIEN SE PUEDE HACER PARA TODAS
% Definir el subconjunto de prefijos que queremos seleccionar

%subconjunto_prefijos = ["Felt.down.or.depressed_Appr Entropy", "Experienced.muscle.tension_Petrosian FD", "Felt.worried_Higuchi FD", "Experienced.loss.of.interest.or.pleasure_Hurst Exponent", "Experienced.muscle.tension_Sample Entropy", "Experienced.loss.of.interest.or.pleasure_Perm Entropy", "Felt.angry_Petrosian FD", "Felt.enthusiastic_Sample Entropy", "Felt.down.or.depressed_Perm Entropy", "Avoided.activities_Perm Entropy", "Felt.energetic_Sample Entropy", "Felt.restless_Petrosian FD", "Felt.frightened.or.afraid_Sample Entropy", "Felt.content_DFA", "Felt.enthusiastic_Appr Entropy", "Felt.worried_Petrosian FD", "Felt.worthless.or.guilty_Number of zero crossings", "Felt.frightened.or.afraid_Appr Entropy", "Experienced.muscle.tension_Higuchi FD", "Felt.angry_Number of zero crossings", "Felt.threatened..judged..or.intimidated_Petrosian FD", "Felt.positive_Sample Entropy", "Felt.accepted.or.supported_DFA", "Had.difficulty.concentrating_Higuchi FD", "Procrastinated_Appr Entropy", "Felt.enthusiastic_Higuchi FD", "Experienced.loss.of.interest.or.pleasure_Sample Entropy", "Felt.enthusiastic_Hurst Exponent", "Avoided.people_Higuchi FD", "Felt.irritable_DFA", "Felt.worried_Perm Entropy", "Felt.enthusiastic_Petrosian FD", "Felt.hopeless_Perm Entropy", "Dwelled.on.the.past_Sample Entropy", "Felt.worthless.or.guilty_Perm Entropy", "Avoided.people_Petrosian FD", "Felt.enthusiastic_Perm Entropy", "Felt.irritable_Sample Entropy", "Felt.energetic_Number of zero crossings", "Felt.worthless.or.guilty_Higuchi FD", "Felt.restless_Perm Entropy"];
%subconjunto_prefijos = ["Felt.worried_Higuchi FD", "Experienced.muscle.tension_Petrosian FD", "Felt.frightened.or.afraid_Sample Entropy", "Felt.worthless.or.guilty_Perm Entropy", "Felt.worried_Perm Entropy", "Felt.restless_Petrosian FD", "Experienced.loss.of.interest.or.pleasure_Perm Entropy", "Felt.enthusiastic_Sample Entropy", "Felt.angry_Petrosian FD", "Experienced.muscle.tension_Sample Entropy", "Experienced.muscle.tension_Higuchi FD", "Felt.irritable_DFA", "Felt.down.or.depressed_Appr Entropy", "Felt.energetic_Sample Entropy", "Felt.hopeless_Perm Entropy", "Avoided.activities_Perm Entropy", "Felt.enthusiastic_Petrosian FD", "Felt.down.or.depressed_Perm Entropy", "Felt.restless_Perm Entropy", "Felt.worthless.or.guilty_Number of zero crossings", "Experienced.loss.of.interest.or.pleasure_Hurst Exponent", "Avoided.people_Higuchi FD", "Felt.irritable_Sample Entropy"];
%subconjunto_prefijos = ["Experienced.muscle.tension_Petrosian FD", "Felt.worried_Higuchi FD", "Felt.enthusiastic_Petrosian FD", "Felt.restless_Petrosian FD", "Experienced.loss.of.interest.or.pleasure_Perm Entropy", "Experienced.muscle.tension_Sample Entropy", "Felt.down.or.depressed_Appr Entropy", "Experienced.loss.of.interest.or.pleasure_Hurst Exponent", "Avoided.people_Higuchi FD", "Felt.worthless.or.guilty_Perm Entropy", "Felt.worried_Perm Entropy", "Felt.angry_Petrosian FD", "Felt.frightened.or.afraid_Sample Entropy", "Felt.irritable_Sample Entropy", "Felt.irritable_DFA", "Felt.hopeless_Perm Entropy", "Felt.enthusiastic_Sample Entropy"];
%subconjunto_prefijos = ["Experienced.muscle.tension_Petrosian FD", "Experienced.loss.of.interest.or.pleasure_Perm Entropy", "Felt.worried_Higuchi FD", "Felt.restless_Petrosian FD", "Felt.down.or.depressed_Appr Entropy", "Felt.enthusiastic_Petrosian FD", "Felt.worried_Perm Entropy", "Felt.frightened.or.afraid_Sample Entropy", "Felt.worthless.or.guilty_Perm Entropy", "Felt.angry_Petrosian FD", "Felt.enthusiastic_Sample Entropy", "Felt.irritable_DFA", "Experienced.muscle.tension_Sample Entropy", "Felt.hopeless_Perm Entropy", "Avoided.people_Higuchi FD"];
%subconjunto_prefijos = ["Felt.worried_Higuchi FD", "Felt.enthusiastic_Petrosian FD", "Experienced.loss.of.interest.or.pleasure_Perm Entropy", "Experienced.muscle.tension_Petrosian FD", "Experienced.muscle.tension_Sample Entropy", "Felt.frightened.or.afraid_Sample Entropy", "Felt.worthless.or.guilty_Perm Entropy", "Felt.worried_Perm Entropy", "Felt.enthusiastic_Sample Entropy", "Felt.restless_Petrosian FD", "Felt.angry_Petrosian FD", "Felt.hopeless_Perm Entropy"];
%11:
%subconjunto_prefijos = ["Experienced.muscle.tension_Petrosian FD", "Experienced.loss.of.interest.or.pleasure_Perm Entropy", "Felt.restless_Petrosian FD", "Felt.worried_Perm Entropy", "Felt.worried_Higuchi FD", "Felt.enthusiastic_Petrosian FD", "Experienced.muscle.tension_Sample Entropy", "Felt.enthusiastic_Sample Entropy", "Felt.frightened.or.afraid_Sample Entropy", "Felt.worthless.or.guilty_Perm Entropy", "Felt.hopeless_Perm Entropy"];
%10:
subconjunto_prefijos = ["Experienced.muscle.tension_Petrosian FD", "Experienced.loss.of.interest.or.pleasure_Perm Entropy", "Felt.restless_Petrosian FD", "Felt.worried_Perm Entropy", "Felt.worried_Higuchi FD", "Felt.enthusiastic_Petrosian FD", "Experienced.muscle.tension_Sample Entropy", "Felt.enthusiastic_Sample Entropy", "Felt.frightened.or.afraid_Sample Entropy", "Felt.worthless.or.guilty_Perm Entropy"];
%7:
% subconjunto_prefijos = ["Experienced.muscle.tension_Petrosian FD",...
% "Experienced.loss.of.interest.or.pleasure_Perm Entropy",...
% "Experienced.muscle.tension_Sample Entropy",...
% "Felt.frightened.or.afraid_Sample Entropy",...
% "Dwelled.on.the.past_DFA",...
% "Felt.enthusiastic_Sample Entropy",...
% "Had.difficulty.concentrating_Sample Entropy"];

%TODAS:
% subconjunto_prefijos = ["Felt.energetic", "Felt.enthusiastic", "Felt.content", "Felt.irritable", ...
%                         "Felt.restless", "Felt.worried", "Felt.worthless.or.guilty", ...
%                         "Felt.frightened.or.afraid", "Experienced.loss.of.interest.or.pleasure", ...
%                         "Felt.angry", "Felt.hopeless", "Felt.down.or.depressed", ...
%                         "Felt.positive", "Felt.fatigued", "Experienced.muscle.tension", ...
%                         "Had.difficulty.concentrating", "Felt.accepted.or.supported", ...
%                         "Felt.threatened..judged..or.intimidated", "Dwelled.on.the.past", ...
%                         "Avoided.activities", "Procrastinated", "Avoided.people"]; % Puedes modificarlo según necesites
%time varying:
%39:
%subconjunto_prefijos = ["Felt.worried_DFA", "Felt.frightened.or.afraid_DFA", "Felt.hopeless_DFA", "Experienced.loss.of.interest.or.pleasure_DFA", "Felt.energetic_DFA", "Avoided.people_DFA", "Felt.threatened..judged..or.intimidated_DFA", "Felt.worthless.or.guilty_DFA", "Felt.threatened..judged..or.intimidated_Lmax", "Felt.positive_DFA", "Avoided.activities_Lmax", "Felt.energetic_Radius", "Had.difficulty.concentrating_vs_Avoided.activities_CrossAvgVert", "Felt.irritable_AvgVerticalLength", "Felt.angry_DFA", "Experienced.loss.of.interest.or.pleasure_vs_Dwelled.on.the.past", "Experienced.loss.of.interest.or.pleasure_Laminarity", "Dwelled.on.the.past_vs_Avoided.activities_CrossVmax", "Experienced.loss.of.interest.or.pleasure_vs_Avoided.activitie_5", "Felt.enthusiastic_vs_Dwelled.on.the.past_CrossAvgVerticalLength", "Felt.energetic_Laminarity", "Felt.enthusiastic_vs_Experienced.muscle.tension_CrossRecurrence", "Felt.energetic_TrappingTime", "Felt.positive_Corr Dim", "Avoided.activities_TrappingTime", "Felt.irritable_vs_Felt.angry_CrossTrappingTime", "Felt.energetic_AvgDiagonalLength", "Felt.content_Corr Dim", "Felt.restless_Radius", "Felt.angry_Vmax", "Avoided.people_Lmax", "Felt.content_AvgDiagonalLength", "Had.difficulty.concentrating_DFA", "Felt.down.or.depressed_vs_Avoided.people_CrossLaminarity", "Felt.energetic_vs_Felt.content_CrossVmax", "Felt.content_Vmax", "Felt.enthusiastic_vs_Experienced.muscle.tension_CrossAvgVertica", "Felt.threatened..judged..or.intimidated_Divergence", "Felt.enthusiastic_Radius"];
%22:
%subconjunto_prefijos = ["Felt.worried_DFA", "Felt.hopeless_DFA", "Felt.frightened.or.afraid_DFA", "Experienced.loss.of.interest.or.pleasure_DFA", "Felt.energetic_DFA", "Avoided.people_DFA", "Felt.threatened..judged..or.intimidated_DFA", "Felt.worthless.or.guilty_DFA", "Avoided.activities_Lmax", "Felt.threatened..judged..or.intimidated_Lmax", "Felt.enthusiastic_vs_Dwelled.on.the.past_CrossAvgVerticalLength", "Felt.positive_DFA", "Had.difficulty.concentrating_vs_Avoided.activities_CrossAvgVert", "Felt.energetic_Radius", "Felt.energetic_Laminarity", "Dwelled.on.the.past_vs_Avoided.activities_CrossVmax", "Felt.energetic_TrappingTime", "Experienced.loss.of.interest.or.pleasure_vs_Dwelled.on.the.past", "Felt.content_Vmax", "Felt.threatened..judged..or.intimidated_Divergence", "Felt.enthusiastic_vs_Experienced.muscle.tension_CrossAvgVertica", "Felt.enthusiastic_vs_Experienced.muscle.tension_CrossRecurrence"];
%19:
%subconjunto_prefijos = ["Felt.worried_DFA", "Experienced.loss.of.interest.or.pleasure_DFA", "Felt.hopeless_DFA", "Felt.frightened.or.afraid_DFA", "Felt.energetic_DFA", "Avoided.people_DFA", "Felt.threatened..judged..or.intimidated_DFA", "Felt.worthless.or.guilty_DFA", "Avoided.activities_Lmax", "Felt.threatened..judged..or.intimidated_Lmax", "Felt.positive_DFA", "Felt.energetic_Radius", "Felt.enthusiastic_vs_Dwelled.on.the.past_CrossAvgVerticalLength", "Had.difficulty.concentrating_vs_Avoided.activities_CrossAvgVert", "Dwelled.on.the.past_vs_Avoided.activities_CrossVmax", "Experienced.loss.of.interest.or.pleasure_vs_Dwelled.on.the.past", "Felt.energetic_Laminarity", "Felt.threatened..judged..or.intimidated_Divergence", "Felt.energetic_TrappingTime"];
%18:
%subconjunto_prefijos = ["Felt.worried_DFA", "Felt.hopeless_DFA", "Felt.frightened.or.afraid_DFA", "Experienced.loss.of.interest.or.pleasure_DFA", "Felt.energetic_DFA", "Avoided.people_DFA", "Felt.threatened..judged..or.intimidated_DFA", "Felt.worthless.or.guilty_DFA", "Avoided.activities_Lmax", "Felt.threatened..judged..or.intimidated_Lmax", "Felt.positive_DFA", "Felt.enthusiastic_vs_Dwelled.on.the.past_CrossAvgVerticalLength", "Had.difficulty.concentrating_vs_Avoided.activities_CrossAvgVert", "Felt.energetic_Radius", "Felt.energetic_Laminarity", "Experienced.loss.of.interest.or.pleasure_vs_Dwelled.on.the.past", "Felt.energetic_TrappingTime", "Dwelled.on.the.past_vs_Avoided.activities_CrossVmax"];


% subconjunto_prefijos = ["Felt.frightened.or.afraid", "Experienced.loss.of.interest.or.pleasure", ...
% "Dwelled.on.the.past", "Felt.enthusiastic", "Experienced.muscle.tension", "Had.difficulty.concentrating"];
% subconjunto_prefijos = ["Avoided.people_Appr Entropy", ...
% "Felt.down.or.depressed_Appr Entropy", ...
% "Felt.worthless.or.guilty_Hurst Exponent", ...
% "Avoided.people_DFA", ...
% "Felt.irritable_Number of zero crossings", ...
% "Felt.angry_DFA", ...
% "Felt.frightened.or.afraid_Number of zero crossings", ...
% "Felt.enthusiastic_Appr Entropy", "Experienced.muscle.tension_Number of zero crossings", "Had.difficulty.concentrating_DFA"];

% Seleccionar la primera columna
id = vars(1);
y_eff=vars(end);
% Crear una máscara lógica para seleccionar variables que comiencen con cualquier prefijo del subconjunto
mascara = false(size(vars)); % Inicializa una máscara de falsos

% Iterar sobre cada prefijo para marcar las variables que comienzan con él
for i = 1:length(subconjunto_prefijos)
    mascara = mascara | startsWith(vars, subconjunto_prefijos(i));
end

% Obtener las variables seleccionadas
vars_seleccionadas = vars(mascara);

% Incluir la primera columna en la selección
vars_finales = [id, vars_seleccionadas y_eff];

% Crear una nueva tabla con solo las variables seleccionadas
T_filtrada = Tabla(:, vars_finales);
%selecciono los que quiero
%loc=find((Tabla.age<=36).*(Tabla.sex==0));
T_filtrada.ID = string(T_filtrada.ID); % Converti la colonna 'ID' in stringa

% Quitar las variables constantes por individuo
uniqueSubjects = unique(T_filtrada{:,1}); % Trova gli ID unici degli individui
numVars = size(T_filtrada, 2) - 2; % Numero totale di variabili
removeVars = true(1, numVars); % Vettore per segnare le variabili da eliminare

for i = 1:length(uniqueSubjects)
    subjIdx = T_filtrada{:,1} == uniqueSubjects(i); % Trova le righe dell'individuo
    subjData = T_filtrada{subjIdx, 2:end-1}; % Estrai i dati numerici dell'individuo
    
    % Se almeno un individuo ha una variabile che cambia, la manteniamo
    removeVars = removeVars & all(subjData == subjData(1, :), 1);
end

% Mostra quali variabili sono costanti dentro ogni individuo
disp('Variabili costanti dentro ogni individuo (verranno rimosse):');
disp(find(removeVars));

% Rimuovi le colonne costanti dentro ogni individuo
T_filtrada(:, find(~removeVars) + 1) = []; % +1 perché la prima colonna è l'ID
var_nuevas = T_filtrada.Properties.VariableNames(2:end-1);
%selecciono los datos
data=table2array(T_filtrada);
data = rimuoviDuplicatiPerSoggetto(data);
% Out of samples para ver la terzera clase
data_comp = double(data(:,2:end));
save('complexity_unique.mat','data_comp');
%trainingData = data_new(find(data_new(:,end) < 3),:);
%testdata = data_new(find(data_new(:,end) == 3),1:end-1);

%data=data(intersect(find(data(:,end-1)==0),intersect(find(data(:,end-2)<=36),find(data(:,end-2)>=30))),:);
subjects=unique(data(:,1));
numFeatures = size(data, 2) - 2; % Numero di feature (escludendo ID e y_eff)
varImportanceAll = zeros(length(subjects), numFeatures);
%predbag1=zeros(length(subjects),1);
%predbag2=zeros(length(subjects),1);

predbagi=zeros(length(subjects),1);
for i=1:length(subjects)
i
pos=find(data(:,1) == subjects(i));
mask=true(1,length(data(:,1)));
%pos=find(dataLDT2(:,1)==subjects(i));
mask(pos)=false;

trainingData=data(mask,2:end);
testdata=data(pos,2:end-1);
trainingData = str2double(trainingData);
testdata = str2double(testdata);
% classWeights = [0.3, 0.7];
[cls prob varImportance]= ExtraTrees(trainingData,testdata);
predbagi(pos)=prob(:,2); % prob que 
%predbag1(i,1)=mean(prob(:,1));
%predbag2(i,1)=mean(prob(:,2));
end

for i=1:length(subjects)
i
pos=find(data(:,1) == subjects(i));
probi(i,1)=mean(predbagi(pos));
%y(i,1)=data(pos(i),end);
varImportanceAll(i, :) = varImportance; % Salvare importanza corrente
end
y = data(:,end);
y = str2double(y);
[X,Y,T,AUC,OPTROCPT] = perfcurve(y-1,probi,1);
[ths0, SEN, SPC, ACC] =thsopt(y,probi);

[AUC SEN SPC ACC]
save('ROC2.mat', 'X', 'Y', 'OPTROCPT');
% **Media delle importanze su tutti i folds (LOOCV)**
meanVarImportance = mean(varImportanceAll, 1);

% Ordinare le importanze in ordine decrescente
[sortedImportance, sortedIdx] = sort(meanVarImportance, 'descend');

% Prendere solo le prime 20 variabili
top10Idx = sortedIdx(1:10);
top10Importance = sortedImportance(1:10);
top10Variabili = var_nuevas(top10Idx);
top10VariabiliNoPedice = strrep(top10Variabili, '_', '\_');
% **Visualizzare l'importanza delle prime 20 variabili originali**
figure;
bar(top10Importance);
title('Top 10 variables');
xlabel('');
ylabel('Mean Importance');
set(gca, 'XTick', 1:10, 'XTickLabel', top10VariabiliNoPedice, 'XTickLabelRotation', 45);

predicted_class = double(probi > ths0);
confMat = confusionmat(y-1, predicted_class);
disp('Matrice di confusione:');
disp(confMat);
accuracy = sum(diag(confMat)) / sum(confMat(:));
disp(['Accuratezza: ', num2str(accuracy)]);
[AUC SEN SPC ACC]
aa =var_nuevas(sortedIdx(sortedImportance > 0));
% Estrai le stringhe dal cell array e uniscile separandole da ", "
result_string = ['["', strjoin(aa, '", "'), '"]'];
% Visualizza la stringa risultante
disp(result_string);

%[X,Y,T,AUC,OPTROCPT] = perfcurve(y-1,probi,1);
%[ths0, SEN, SPC, ACC] =thsopt(y,probi);

figure;
plot(data1.X, data1.Y, 'b-', 'LineWidth', 2); hold on;   % Prima curva ROC
plot(X, Y, 'r-', 'LineWidth', 2);                        % Seconda curva ROC
plot(OPTROCPT(1), OPTROCPT(2), 'ro', 'MarkerSize', 11, 'LineWidth', 3); % Secondo punto ottimale
plot(data1.OPTROCPT(1), data1.OPTROCPT(2), 'bo', 'MarkerSize', 11, 'LineWidth', 3); % Primo punto ottimale
plot([0 1], [0 1], 'k--');                               % Linea base (random)
xlabel('False Positive Rate', 'FontSize',16);
ylabel('True Positive Rate', 'FontSize',16);
legend('ROC Curve Complexity Case', 'ROC Curve Original Data', 'Optimal Threshold Complexity Case (0.77)', 'Optimal Threshold Original Data (0.53)', 'Chance level', ...
    'Location', 'SouthEast', 'FontSize',13);
% Annotazione della soglia ottimale
%text(OPTROCPT(1) + 0.02, OPTROCPT(2) - 0.05, ...
%    ['Optimal threshold = ' num2str(ths0, '%.2f')], ...
%    'FontSize', 12, 'Color', 'r', 'FontWeight', 'bold');

