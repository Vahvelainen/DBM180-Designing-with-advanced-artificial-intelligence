
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

import csv 
from txt2vec import textTokenizer

# Init tex tokenizer
txt2vec = textTokenizer()


# Read filenames and embeddings of the index file
index_file = "index.csv"

files = []
embeddings = []

with open(index_file) as file_obj: 
  reader = csv.reader(file_obj) 
  for row in reader:
      if ( len(row) == 768 + 1 ):
        files.append( row.pop(0) )
        embeddings.append( np.array(row) )

# Ask for quesry and create and embeddign of it
query = input('What are you searching for? ')
query_embedding = txt2vec.getEmbedding(query)

# Convert the list of embeddings to a 2D array
embeddings_array = np.vstack(embeddings)

# Calculate pairwise cosine similarity between the target and list of embeddings
similarities = cosine_similarity([query_embedding], embeddings_array)

# Find the index of the most similar embedding
most_similar_index = np.argmax(similarities)

# Retrieve the most similar embedding
most_similar_embedding = files[most_similar_index]

print(f"Most similar embedding index: {most_similar_index}")
print(f"Most similar embedding: {most_similar_embedding}")
