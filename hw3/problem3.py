from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

from sklearn.cluster import KMeans
from sklearn.utils import shuffle

from scipy.misc import imread

Ks = [4, 16, 32]

def recreate_image(code, labels, width, height):
    image_recreate = np.zeros([width, height, 3])
    label_idx = 0
    for i in range(width):
        for j in range(height):
            image_recreate[i][j] = code[labels[label_idx]]
            label_idx += 1

    return np.array(image_recreate, dtype = np.uint8)

def kmeans_cluster(cluster_num, image_color):
    kmeans = KMeans(n_clusters=cluster_num, random_state=0).fit(image_color)
    labels = kmeans.predict(image_color)
    return kmeans, labels

def display_pic(kmeans, labels):
    plt.figure()
    plt.clf()
    ax = plt.axes([0, 0, 1, 1])
    plt.axis('off')
    plt.title('Quantized image (64 colors, K-Means)')
    plt.imshow(recreate_image(kmeans.cluster_centers_, labels, width, height))


if __name__ == '__main__':

    im = imread('trees.png')
    image = np.array(im, dtype = float)

    width, height, color = image.shape
    image_color = np.reshape(image, (width * height, color))

    plt.figure()
    plt.clf()
    ax = plt.axes([0, 0, 1, 1])
    plt.axis('off')
    plt.title('Original image (96,615 colors)')
    plt.imshow(im)

    for cluster_num in Ks:
        kmeans, labels = kmeans_cluster(cluster_num, image_color)
        display_pic(kmeans, labels)

    plt.show()
