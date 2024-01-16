
from GUI import TkWindow
from IndexTools import readIndex
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity

window = TkWindow()

# Clustering here
print('Opening index file...')
index_file = "index_fujifilm.csv"
embeddings, files = readIndex(index_file)

K = 4
kmeans = KMeans(K, random_state=1, n_init=10)
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
embedding_clusters = sorted_embedding_clusters
file_clusters = sorted_file_clusters

for files in file_clusters:
    window.addFileCarousel(files, max_open=5)

window.mainloop()
