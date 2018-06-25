import numpy as np
import matplotlib.pyplot as plt

from sklearn import cluster, datasets
from sklearn.preprocessing import StandardScaler
from itertools import cycle, islice


n_samples = 1500
random_state = 170

plot_num = 1
k_clusters = 2

X, y = datasets.make_blobs(n_samples=n_samples, random_state=random_state)
transformation = [[0.6, -0.6], [-0.4, 0.8]]
X_aniso = np.dot(X, transformation)
aniso = (X_aniso, y)

varied = datasets.make_blobs(n_samples=n_samples,
                             cluster_std=[1.0, 2.5, 0.5],
                             random_state=random_state)

noisy_circles = datasets.make_circles(n_samples=n_samples, factor=.5, noise=.05)

datasets = [aniso, varied, noisy_circles]

for i_dataset, dataset in enumerate(datasets):
    X, y = dataset
    X = StandardScaler().fit_transform(X)

    kmeans = cluster.KMeans(n_clusters=k_clusters)
    spectral = cluster.SpectralClustering(n_clusters=k_clusters, eigen_solver='arpack', affinity="nearest_neighbors")

    clustering_algorithms = (('KMeans', kmeans),('SpectralClustering', spectral))

    for algorithm_name, algorithm in clustering_algorithms:

        algorithm.fit(X)
        if hasattr(algorithm, 'labels_'):
            y_pred = algorithm.labels_.astype(np.int)
        else:
            y_pred = algorithm.predict(X)
        plt.figure()
        plt.plot(len(datasets), len(clustering_algorithms), plot_num)
        plt.title(algorithm_name, size=15)

        colors = np.array(list(islice(cycle(['#377eb8', '#ff7f00', '#4daf4a']),int(max(y_pred) + 1))))

        plt.scatter(X[:, 0], X[:, 1], s=10, color=colors[y_pred])
        plt.xlim(-3, 3)
        plt.ylim(-3, 3)
        plt.xticks(())
        plt.yticks(())




plt.show()
