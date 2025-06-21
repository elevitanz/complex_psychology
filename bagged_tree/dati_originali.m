% dati originali 2 classi:
clear
Tabla = readtable('/Users/ele/Desktop/codici_finali/dataset/general_data.csv', 'PreserveVariableNames', true);
Tabla(:,1) = [];
% Obtener los nombres de las variables de la tabla
vars = Tabla.Properties.VariableNames;
Tabla = Tabla(Tabla.y_eff ~= 3, :);

%PARA SUBCANJUNTOS-TAMBIEN SE PUEDE HACER PARA TODAS
% Definir el subconjunto de prefijos que queremos seleccionar
subconjunto_prefijos = ["Felt.energetic", "Felt.enthusiastic", "Felt.content", "Felt.irritable", ...
                        "Felt.restless", "Felt.worried", "Felt.worthless.or.guilty", ...
                        "Felt.frightened.or.afraid", "Experienced.loss.of.interest.or.pleasure", ...
                        "Felt.angry", "Felt.hopeless", "Felt.down.or.depressed", ...
                        "Felt.positive", "Felt.fatigued", "Experienced.muscle.tension", ...
                        "Had.difficulty.concentrating", "Felt.accepted.or.supported", ...
                        "Felt.threatened..judged..or.intimidated", "Dwelled.on.the.past", ...
                        "Avoided.activities", "Procrastinated", "Avoided.people"]; % Puedes modificarlo según necesites

% Seleccionar la primera columna
id = vars(end-1);
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
%selecciono los datos
data=table2array(T_filtrada);
%data=data(intersect(find(data(:,end-1)==0),intersect(find(data(:,end-2)<=36),find(data(:,end-2)>=30))),:);
subjects=unique(data(:,1));
numFeatures = size(data, 2) - 2; % Numero di feature (escludendo ID e y_eff)
varImportanceAll = zeros(length(subjects), numFeatures);
%predbag1=zeros(length(subjects),1);
%predbag2=zeros(length(subjects),1);
data_original = double(data(:,2:end));
%save('dati_originali.mat','data_original');

%MEDIA PER INDIVIDUO DEI DATI ORIGINALI: se vuoi classificare con questo,
%cambia data_mean in data e sistema y.
means_per_individual = varfun(@mean, T_filtrada, 'InputVariables', T_filtrada.Properties.VariableNames(~strcmp(T_filtrada.Properties.VariableNames,'ID')), ...
    'GroupingVariables', 'ID');
means_per_individual.GroupCount = [];
data_mean=table2array(means_per_individual);
data_mean_original = double(data_mean(:,2:end));
save('media_dati_originali.mat','data_mean_original');

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
y(i,1)=data(pos(i),end);
varImportanceAll(i, :) = varImportance; % Salvare importanza corrente
end
%y = data(:,end);
y = str2double(y);
[X,Y,T,AUC,OPTROCPT] = perfcurve(y-1,probi,1);
[ths0, SEN, SPC, ACC] =thsopt(y,probi);

[AUC SEN SPC ACC]

% **Media delle importanze su tutti i folds (LOOCV)**
meanVarImportance = mean(varImportanceAll, 1);

% Ordinare le importanze in ordine decrescente
[sortedImportance, sortedIdx] = sort(meanVarImportance, 'descend');

% Prendere solo le prime variabili
top10Idx = sortedIdx(1:10);
top10Importance = sortedImportance(1:10);
top10Variabili = vars_seleccionadas(top10Idx);
top10VariabiliNoPedice = strrep(top10Variabili, '_', '\_');
% **Visualizzare l'importanza delle prime 20 variabili originali**
figure;
bar(top10Importance);
title('Top 10 variables');
xlabel('');
ylabel('Mean Importance');
set(gca, 'XTickLabel', top10VariabiliNoPedice, 'XTickLabelRotation', 45);

predicted_class = double(probi > ths0);
confMat = confusionmat(y-1, predicted_class);
disp('Matrice di confusione:');
disp(confMat);
accuracy = sum(diag(confMat)) / sum(confMat(:));
disp(['Accuratezza: ', num2str(accuracy)]);

figure;
plot(X, Y, 'b-', 'LineWidth', 2); hold on;
plot(OPTROCPT(1), OPTROCPT(2), 'ro', 'MarkerSize', 11, 'LineWidth', 3); % Punto ottimale
plot([0 1], [0 1], 'k--'); % baseline random
xlabel('False Positive Rate', 'FontSize',16);
ylabel('True Positive Rate', 'FontSize',16);
%title(['ROC Curve (AUC = ' num2str(AUC, '%.3f') ')'], 'FontSize',16);
legend('ROC Curve', 'Optimal Threshold (0.54)', 'Chance level', 'Location', 'SouthEast', 'FontSize',13);
axis square;
grid on;
save('ROC1.mat', 'X', 'Y', 'OPTROCPT');
