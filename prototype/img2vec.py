from transformers import AutoFeatureExtractor, Data2VecVisionModel
from PIL import Image
import numpy as np


class imageTokenizer():
  '''
    Creates an embedding as numpy array of the length 768 with the facebooks data2vec-vision model
  '''

  def __init__(self):
    self.feature_extractor = AutoFeatureExtractor.from_pretrained('facebook/data2vec-vision-base')
    self.model = Data2VecVisionModel.from_pretrained('facebook/data2vec-vision-base')

  def getEmbedding(self, image_path: str):
    image = Image.open(image_path)
    # Preprocess image
    inputs = self.feature_extractor(images=image, return_tensors="pt")

    # Get image embeddings
    outputs = self.model(**inputs)
    last_hidden_states = outputs.last_hidden_state

    # Take one mean of the pool of embedding created
    vector = last_hidden_states.mean(dim=1)

    # Isolate the embedding as numpy array
    image_embedding = vector.detach().numpy()[0]

    # Now you have the embeddings
    return image_embedding
