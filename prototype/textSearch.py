
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

import subprocess, os, platform
from CLIP import CLipEncoder
from IndexTools import readIndex

'''
Text based search for images that have been indexed with createIndex.py
The program reads the index file, asks for a search query and open best five mathes for the given search.
'''

print('Initalizing the model...')

# Init encoder
encoder = CLipEncoder()

# Read filenames and embeddings of the index file
index_file = "index.csv"
embeddings, files = readIndex(index_file)

while True:
  # Ask for query and create and embedding of it
  query = input('What are you searching for? (exit w empty) ')

  if query == '':
    exit()

  query_embedding = encoder.textEmbedding(query)

  # Convert the list of embeddings to a 2D array
  embeddings_array = np.vstack(embeddings)

  # Calculate pairwise cosine similarity between the target and list of embeddings
  similarities = cosine_similarity([query_embedding], embeddings_array)

  # Get the indices that would sort the array
  sorted_indices = np.argsort(similarities)

  # Take the last five indices for the five largest values
  five_largest_indices = sorted_indices[0, -5:]

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
