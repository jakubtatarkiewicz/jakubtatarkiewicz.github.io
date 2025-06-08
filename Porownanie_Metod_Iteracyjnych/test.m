format long;

A1 = [4 -1  0;
     -1  4 -1;
      0 -1  4];
b1 = [1;2;3];
x0_1 = zeros(3,1);
IterationMethodsAnalytics(A1, b1, 100, x0_1, 1e-6, 'example1.csv');

A2 = [10 1 1;
      2 10 1;
      2  2 10];
b2 = [12;13;14];
x0_2 = zeros(3,1);
IterationMethodsAnalytics(A2, b2, 100, x0_2, 1e-6, 'example2.csv');

A3 = hilb(4);
b3 = A3 * ones(4,1);
x0_3 = zeros(4,1);
IterationMethodsAnalytics(A3, b3, 100, x0_3, 1e-6, 'example3.csv');

A4 = [ 8 -1  0  0  0;
      -1  7 -1  0  0;
       0 -1  6 -1  0;
       0  0 -1  5 -1;
       0  0  0 -1  4];
b4 = [5;4;3;2;1];
x0_4 = zeros(5,1);
IterationMethodsAnalytics(A4, b4, 100, x0_4, 1e-6, 'example4.csv');

Mmat = [ 1  2  0 -1;
         0  1  1  2;
        -1  0  2  1;
         1 -1  1  0 ];
A5 = Mmat' * Mmat + 0.1 * eye(4);
b5 = [2;1;3;1];
x0_5 = zeros(4,1);
IterationMethodsAnalytics(A5, b5, 100, x0_5, 1e-6, 'example5.csv');
