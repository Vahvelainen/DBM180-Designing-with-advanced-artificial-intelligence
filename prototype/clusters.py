import numpy as np
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.metrics.pairwise import cosine_similarity
import csv 

'''
Class for handling clusters
Also a method for loading index into cluster
'''

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
    '''
    Divides cluster into K sub-clusters with kmeans
    the sub-clusters are sorted by the distance to the cluster center 
    '''

    kmeans = KMeans(K, init="k-means++", n_init="auto")
    kmeans.fit(self.embeddings)
    labels = kmeans.labels_
    cluster_centers = kmeans.cluster_centers_

    file_clusters = [[] for i in range(K)]
    embedding_clusters = [[] for i in range(K)]
    for i, label in enumerate(labels):
        file_clusters[label].append( self.files[i] )
        embedding_clusters[label].append( self.embeddings[i] )

    clusters = []
    for i in range(K):
      cluster = Cluster(embedding_clusters[i], file_clusters[i], F"Cluster #{i}", self)
      cluster.sortByDistanceTo(cluster_centers[i])
      clusters.append(cluster)

    return clusters
  
  def agglomerativeClustering(self, K = 3):
    '''
    Divides cluster into K sub-clusters with AgglomerativeClustering
    the sub-clusters are sorted by the distance to the cluster center 
    '''
    np_embeddings = np.array(self.embeddings, dtype=float) 
    clustering = AgglomerativeClustering(K).fit(np_embeddings)
    labels = clustering.labels_

    file_clusters = [[] for i in range(K)]
    embedding_clusters = [[] for i in range(K)]
    for i, label in enumerate(labels):
        file_clusters[label].append( self.files[i] )
        embedding_clusters[label].append( np_embeddings[i] )

    # Calculate cluster centers bc Agg doesnt rock it
    cluster_centers = []
    for cluster in embedding_clusters:
        centroid = np.mean(cluster, axis=0)
        cluster_centers.append(centroid)

    # Make and sort clusters
    clusters = []
    for i in range(K):
      cluster = Cluster(embedding_clusters[i], file_clusters[i], F"Cluster #{i}", self)
      cluster.sortByDistanceTo(cluster_centers[i])
      clusters.append(cluster)

    return clusters
    
  def sortByDistanceTo(self, center):
      similarities = cosine_similarity([center], self.embeddings)[0]
      sorted_indexes = np.argsort(similarities)
      sorted_indexes = np.flip(sorted_indexes)
      self.embeddings = [ self.embeddings[i] for i in sorted_indexes ]
      self.files = [ self.files[i] for i in sorted_indexes ]

def readIndex(index_file):
  '''
  Reads csv file creted with createIndex.py and reurns (embeddings, files) as lists
  '''
  files = []
  embeddings = []

  with open(index_file) as file_obj: 
    reader = csv.reader(file_obj) 
    for row in reader:
        # Check that csv.row is as long as embedding + the filename
        if ( len(row) == 512 + 1 ):
          files.append( row.pop(0) )
          embeddings.append( np.array(row) )

  return Cluster(embeddings, files, 'Index')
