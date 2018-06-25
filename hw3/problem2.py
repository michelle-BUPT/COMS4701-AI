import sys, csv
import numpy as np
from numpy import *
# from problem1 import load_args
from sklearn.preprocessing import StandardScaler
from sklearn import preprocessing
ALPHAS = [0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1, 5, 10]
ITERATION = 100
INF = float('inf')
'''
best parameter for tenth line
'''

def gd(X, Y, alpha, iteration_max):
    n = len(Y)
    beta = np.zeros(len(X[0]))

    for _ in range(ITERATION):
        fx = beta.dot(X.T)
        beta -= X.T.dot(fx - Y) * alpha / n

    diff = beta.dot(X.T) - Y
    loss = diff.dot(diff.T) / (2 * n)
    return beta, loss


if __name__ == '__main__':
    filename_input, filename_output = sys.argv[1], sys.argv[2]

    with open(filename_input, 'r') as file_in, open(filename_output, 'w') as file_out:
        input  = np.array(list(csv.reader(file_in)), dtype=float)
        # print(input)
        X = input[:, 0 : len(input[0]) - 1]

        Y = input[:, len(input[0]) - 1]

        # X_scaled = (X - mean(X, axis=0)) / std(X, axis=0)
        # scaler = StandardScaler()
        # X_scaled = scaler.fit_transform(X)
        X_scaled = preprocessing.scale(X)
        # print(X_scaled)
        X_beta = np.insert(X_scaled, 0, 1, axis=1)

        writer_output = csv.writer(file_out, delimiter=',')

        for alpha in ALPHAS:
            beta, loss= gd(X_beta, Y, alpha, ITERATION)
            writer_output.writerow([alpha, ITERATION] + list(beta))

        best_loss = INF
        for alpha in np.arange(0.1, 1.1, 0.1):
            for iteration_max in np.arange(100, 1010, 10):
                beta, loss = gd(X_beta, Y, alpha, iteration_max)
                row = [alpha, iteration_max] + list(beta)
                if loss < best_loss:
                    best_loss, best_row = loss, row

        writer_output.writerow(best_row)
