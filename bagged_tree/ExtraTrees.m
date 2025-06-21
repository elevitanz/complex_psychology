function [predictedLabels, classProbabilities, varImportance] = ExtraTrees(trainingData,testdata, ClassWeights)
% Train a Random Forest-like model with TreeBagger
nTrees = 300;  % Number of trees
numPredictorsToSample ='all';  % Sample all predictors at each node (for more randomness)
X = trainingData(:, 1:end-1);  % Predictors
Y = trainingData(:, end);      % Class labels (0 or 1)
Y = categorical(Y);  % Convert to categorical if not already
%'ClassNames', {'0', '1'},

% Definir los pesos de clase según se proporcionen
if nargin < 3 || isempty(classWeights)
        % Si no se especifican pesos, se usan proporcionales a la frecuencia de clases
        classCounts = countcats(Y);
        classWeights = sum(classCounts) ./ (length(classCounts) * classCounts);
end
extraTreesModel = TreeBagger(nTrees, X, Y, 'Method', 'classification',...
                             'NumPredictorsToSample',...
                            numPredictorsToSample, ... 
                            'OOBPrediction', 'on',... 
                            'OOBPredictorImportance', 'on',...
                            'Prior', classWeights); % Abilita importanza OOB);
% Compute variable importance
varImportance = extraTreesModel.OOBPermutedPredictorDeltaError;
%varImportance = extraTreesModel.DeltaCriterionDecisionSplit;

% Predict using the model (returns predicted class and probabilities)
[predictedLabels, classProbabilities] = predict(extraTreesModel, testdata);