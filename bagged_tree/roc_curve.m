data1 = load('ROC1.mat');
data2 = load('ROC2.mat');
rosella = [0.9, 0.7, 0.9];  % Un lilla chiaro, tendente al rosa
lightblue = [0.68, 0.85, 0.90];  % Light blue (simile a 'powder blue')

figure;
plot(data1.X, data1.Y, '-', 'Color', rosella, 'LineWidth', 2); hold on;   % Prima curva ROC
plot(data2.X, data2.Y, 'b-', 'LineWidth', 2);            % Seconda curva ROC
plot(data2.OPTROCPT(1), data2.OPTROCPT(2), 'o','MarkerFaceColor','b','MarkerEdgeColor', lightblue, 'MarkerSize', 11, 'LineWidth', 3); % Secondo punto ottimale
plot(data1.OPTROCPT(1), data1.OPTROCPT(2), 'o','MarkerFaceColor', rosella, 'MarkerSize', 11, 'LineWidth', 3); % Primo punto ottimale
plot([0 1], [0 1], 'k--');                               % Linea base (random)
xlabel('False Positive Rate', 'FontSize',16);
ylabel('True Positive Rate', 'FontSize',16);
legend('Original Data','Complexity measures', 'Optimal Threshold (0.77)', 'Optimal Threshold (0.53)', 'Chance level', ...
    'Location', 'best', 'FontSize',13);