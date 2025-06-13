function [x, k] = JacobiEps(A, b, M, x0, eps)
    [m, n] = size(A);
    if m ~= n
        return
    end

    x    = x0;
    last = zeros(n,1);
    k    = 1;

    while k < M && (norm(x - last) >= eps || k == 1)
        last = x;
        k = k + 1;
        
        y = zeros(n, 1);
        for i = 1:n
            sum = 0;
            if i > 1
                sum = A(i,1:i-1) * x(1:i-1);
            end

            if i < n
                sum = sum + A(i,i+1:n) * x(i+1:n);
            end
            
            y(i) = (b(i) - sum) / A(i,i);
        end

        x=y;
    end
end
