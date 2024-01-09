#pip install simple_term_menu
from simple_term_menu import TerminalMenu

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import subprocess, os, platform
from BLIP import BlipDecoder

from IndexTools import readIndex
from sklearn.cluster import KMeans

print('Initalizing models...')
#encoder = CLipEncoder()
decoder = BlipDecoder()

# Read filenames and embeddings of the index file
print('Opening index file...')
index_file = "index_bu.csv"
embeddings, files = readIndex(index_file)

while True:

  # Do one round of clustering with k means
  kmeans = KMeans(n_clusters=4, random_state=1, n_init=10)
  kmeans.fit(embeddings)
  labels = kmeans.labels_
  cluster_centers = kmeans.cluster_centers_

  print('Making the labelings...')
  label_files = [] 
  label_names = []
  center_similarities = []

  # Find closest neighbour of the centroids to use for labeling
  for center in cluster_centers:
    similarities = cosine_similarity([center], embeddings)[0]
    center_similarities.append(similarities)
    closest_index = np.argmax(similarities)
    closest_file = files[closest_index]
    label_files.append(closest_file)
    label_name = decoder.caption(closest_file)
    label_names.append(label_name)

  # Ask which cluster to explore
  print('please select which cluster to explore')
  terminal_menu = TerminalMenu(label_names)
  menu_entry_index = terminal_menu.show()
  print(f"You have selected {label_names[menu_entry_index]}!")

  #Next would be to ask if user wants to open images or keep diggin but we are jsut going to open 5 images now an loop back

  # Get the indices that would sort the array
  sorted_indices = np.argsort(center_similarities[menu_entry_index])
  five_largest_indices = sorted_indices[-5:]
  print('Five best matches:')
  for i in five_largest_indices:
    filepath = files[i]
    print(filepath)
    # Open the file in defaul program
    if platform.system() == 'Darwin':       # macOS
        os.system(f"open {filepath}")
    elif platform.system() == 'Windows':    # Windows
        os.startfile(filepath)
    else:                                   # linux variants
        subprocess.call(('xdg-open', filepath))

  print('Filering the files...')
  filtered_files = []
  filtered_embeddings = []
  for i, label in enumerate(labels):
    if label == menu_entry_index:
        filtered_files.append(files[i])
        filtered_embeddings.append(embeddings[i])

  files = filtered_files
  embeddings = filtered_embeddings
      
