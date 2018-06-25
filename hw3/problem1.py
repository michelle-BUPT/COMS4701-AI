import sys, csv
import numpy as np

MAX_ITER = 1000
def pla(input):
    weight = np.zeros(len(input[0]))
    input = np.insert(input, 2, 1, axis = 1)
    output = [] * len(weight)

    for i in range(MAX_ITER):
        converged = True
        for sample in input:
            feature = sample[0: len(sample) - 1]
            label = sample[len(sample) - 1]
            if weight.dot(feature) * label <= 0:
                converged = False
                weight += feature * label
        if converged:
            break
        output.append(np.copy(weight))

    return output

if __name__ == '__main__':
    filename_input, filename_output = sys.argv[1], sys.argv[2]
    with open(filename_input, 'r') as file_in, open(filename_output, 'w') as file_out:
        output = pla(np.array(list(csv.reader(file_in)), dtype=float))
        writer_output = csv.writer(file_out, delimiter=',')
        for row in output:
            writer_output.writerow(row)
