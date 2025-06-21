function data_clean = rimuoviDuplicatiPerSoggetto(data)
    % Assicura che il dataset sia un cell array di stringhe
    if isstring(data)
        data = cellstr(data); % Converte array di stringhe in cell array
    end

    % Trova soggetti unici (prima colonna)
    soggetti = unique(data(:, 1), 'stable'); % Mantiene l'ordine originale

    % Prealloca un cell array con lo stesso formato di data
    data_clean = strings(length(soggetti), size(data, 2)); % Usa array di stringhe

    % Per ogni soggetto, seleziona solo la prima riga
    for i = 1:length(soggetti)
        idx = find(strcmp(data(:, 1), soggetti{i}), 1, 'first'); % Trova la prima occorrenza
        data_clean(i, :) = string(data(idx, :)); % Mantiene array di stringhe per ogni riga
    end
end

