import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity

class Cluster():
  '''
  class for clusters with ferecnte to the parent with tag etc.
  for building the breadcrumps and history and everythigns
  '''
  def __init__(self, embeddings, files, label, parent = None ) -> None:
    self.embeddings = embeddings
    self.files = files
    self.label = label
    self.parent = parent
    self.len = len(embeddings)

    if parent == None:
      self.str = label
    else:
      self.str = str(parent) + ' > ' + label

  def __str__(self) -> str:
    return self.str
  
  def __hash__(self) -> int:
    return hash(self.str)
  
  def kmeans(self, K = 3):
    kmeans = KMeans(K, init="k-means++", n_init="auto")
    kmeans.fit(self.embeddings)
    labels = kmeans.labels_
    cluster_centers = kmeans.cluster_centers_

    file_clusters = [[] for i in range(K)]
    embedding_clusters = [[] for i in range(K)]
    for i, label in enumerate(labels):
        file_clusters[label].append( self.files[i] )
        embedding_clusters[label].append( self.embeddings[i] )

    # Sort by distance to the cluster center
    clusters = []
    for clusterIndex, center in enumerate(cluster_centers):
        clusterEmbeddings = embedding_clusters[clusterIndex]
        clusterFiles = file_clusters[clusterIndex]
        similarities = cosine_similarity([center], clusterEmbeddings)[0]
        sorted_indexes = np.argsort(similarities)
        sorted_indexes = np.flip(sorted_indexes)

        embeddings2 = [ clusterEmbeddings[i] for i in sorted_indexes ]
        files2 = [ clusterFiles[i] for i in sorted_indexes ]
        cluster2 = Cluster(embeddings2, files2, F"Cluster #{clusterIndex}", self)
        clusters.append(cluster2)

    return clusters