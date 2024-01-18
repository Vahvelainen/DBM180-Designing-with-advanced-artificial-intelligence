
from CLIP import CLipEncoder
from clusters import Cluster, readIndex
from tools import openFileInDefaultProgram

'''
Text based search for images that have been indexed with createIndex.py
The program reads the index file, asks for a search query and open best five mathes for the given search.
'''

print('Initalizing the model...')

# Init encoder
encoder = CLipEncoder()

# Read filenames and embeddings of the index file
index_file = "index.csv"
index = readIndex(index_file)

while True:
  # Ask for query and create and embedding of it
  query = input('What are you searching for? (exit w empty) ')

  if query == '':
    exit()

  # Get embedding to query and sort the index based on it
  query_embedding = encoder.textEmbedding(query)
  index.sortByDistanceTo(query_embedding)

  print('Five best matches:')
  for i in range(5):
    filepath = index.files[i]
    print(filepath)
    openFileInDefaultProgram(filepath)
