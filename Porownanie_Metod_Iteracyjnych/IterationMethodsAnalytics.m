function IterationMethodsAnalytics(A,b,M,x0,eps,file_name)
    if isstring(file_name), file_name=char(file_name); end
    [~,~,ext] = fileparts(file_name);
    if isempty(ext), file_name = [file_name,'.csv']; end

    % --- historia iteracji i różnice ---
    [~, iters_gs, Xhist_gs, diffs_gs] = GaussSeidelEpsAnalytics(A,b,M,x0,eps);
    [~, iters_j,  Xhist_j,  diffs_j ] = JacobiEpsAnalytics    (A,b,M,x0,eps);

    R = max(iters_gs, iters_j) + 1;  % liczba wierszy bez "true value"
    n = length(x0);

    % --- przygotowanie Xgs i diffs_out_gs ---
    Xgs = Xhist_gs(1:iters_gs+1, :);
    diffs_out_gs = [NaN; diffs_gs(1:iters_gs)];
    if size(Xgs,1) < R
        Xgs = [Xgs;               NaN(R - size(Xgs,1), n)];
        diffs_out_gs = [diffs_out_gs; NaN(R - length(diffs_out_gs), 1)];
    end

    % --- przygotowanie Xj i diffs_out_j ---
    Xj = Xhist_j(1:iters_j+1, :);
    diffs_out_j = [NaN; diffs_j(1:iters_j)];
    if size(Xj,1) < R
        Xj = [Xj;               NaN(R - size(Xj,1), n)];
        diffs_out_j = [diffs_out_j; NaN(R - length(diffs_out_j), 1)];
    end

    % --- dopięcie wiersza "true value" ---
    x_true = A\b;
    Xgs = [Xgs; x_true'];
    Xj  = [Xj;  x_true'];

    % dopięcie brakującego elementu do diffs (ostatni wiersz NaN)
    diffs_out_gs = [diffs_out_gs; NaN];
    diffs_out_j  = [diffs_out_j;  NaN];

    % --- wyliczenie błędów od wartości true dla każdej iteracji ---
    N = size(Xgs,1);  % powinno być R+1
    gs_error = NaN(N,1);
    j_error  = NaN(N,1);
    for k = 1:N
        v_gs = Xgs(k, :)';
        v_j  = Xj(k,  :)';
        if all(~isnan(v_gs))
            gs_error(k) = norm(x_true - v_gs);
        end
        if all(~isnan(v_j))
            j_error(k)  = norm(x_true - v_j);
        end
    end

    % --- składanie końcowej macierzy ---
    out = [ ...
      Xgs,         diffs_out_gs, gs_error, ...
      Xj,          diffs_out_j, j_error   ...
    ];

    % --- nazwy kolumn ---
    gs_names = arrayfun(@(i) sprintf('gs_x%d',i), 1:n, 'UniformOutput', false);
    j_names  = arrayfun(@(i) sprintf('j_x%d',i),  1:n, 'UniformOutput', false);
    varNames = [ ...
      gs_names,   {'gs_diff','gs_error'}, ...
      j_names,    {'j_diff','j_error'}    ...
    ];

    % --- nazwy wierszy ---
    rowNames = cell(R+1,1);
    rowNames{1} = 'Initial data';
    for k = 1:(R-1)
      rowNames{k+1} = sprintf('%dth approximation', k);
    end
    rowNames{R+1} = 'true value';

    % --- zapis do tabeli i CSV ---
    T = array2table(out, 'VariableNames', varNames, 'RowNames', rowNames);
    writetable(T, file_name, 'WriteRowNames', true);
end
