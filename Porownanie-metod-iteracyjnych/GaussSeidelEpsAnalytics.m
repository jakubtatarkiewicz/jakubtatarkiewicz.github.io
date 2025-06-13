function [x,performed_iterations,x_before_iteration,diffs] = GaussSeidelEpsAnalytics(A,b,M,x0,eps)
    [m,n] = size(A);

    if m~=n
        return
    end

    x = x0;
    diffs = zeros(M,1);
    x_before_iteration = zeros(M+1,n);
    x_before_iteration(1,:) = x';
    performed_iterations = 0;

    while performed_iterations < M
        last = x;

        for i=1:n
            sum = 0;

            if i>1
                sum = A(i,1:i-1)*x(1:i-1);
            end

            if i<n
                sum = sum + A(i,i+1:n)*x(i+1:n);
            end
            x(i) = (b(i)-sum)/A(i,i);
        end

        performed_iterations = performed_iterations + 1;
        diffs(performed_iterations) = norm(x - last);
        x_before_iteration(performed_iterations + 1,:) = x';

        if diffs(performed_iterations) < eps
            break;
        end
    end
end