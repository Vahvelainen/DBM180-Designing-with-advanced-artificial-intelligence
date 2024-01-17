
from GUI import TkWindow, FileCarousel
from IndexTools import readIndex
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity

# Clustering here
print('Opening index file...')
index_file = "index_fujifilm.csv"
embeddings, files = readIndex(index_file)

def doClustering(embeddings, files):
    K = 4
    kmeans = KMeans(K, init="k-means++", n_init="auto")
    kmeans.fit(embeddings)
    labels = kmeans.labels_
    cluster_centers = kmeans.cluster_centers_

    file_clusters = [[] for i in range(K)]
    embedding_clusters = [[] for i in range(K)]
    for i, label in enumerate(labels):
        file_clusters[label].append( files[i] )
        embedding_clusters[label].append( embeddings[i] )

    # Sort by distance to the cluster center
    sorted_embedding_clusters = []
    sorted_file_clusters = []
    for clusterIndex, center in enumerate(cluster_centers):
        clusterEmbeddings = embedding_clusters[clusterIndex]
        clusterFiles = file_clusters[clusterIndex]
        similarities = cosine_similarity([center], clusterEmbeddings)[0]
        sorted_indexes = np.argsort(similarities)
        sorted_indexes = np.flip(sorted_indexes)
        sorted_embedding_clusters.append([ clusterEmbeddings[i] for i in sorted_indexes ])
        sorted_file_clusters.append([ clusterFiles[i] for i in sorted_indexes ])

    return sorted_embedding_clusters, sorted_file_clusters

window = TkWindow( (embeddings, files), doClustering )
window.mainloop()
