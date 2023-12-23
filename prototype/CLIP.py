from transformers import CLIPProcessor, CLIPModel
from PIL import Image

class CLipEncoder():
  '''
    Creates comparable embeddings of length 512 from text and images
    using the CLIP model https://huggingface.co/docs/transformers/model_doc/clip
    with hugginface 
  '''

  def __init__(self):
    model_name = "openai/clip-vit-base-patch32"
    self.model = CLIPModel.from_pretrained(model_name)
    self.processor = CLIPProcessor.from_pretrained(model_name)

  def imageEmbedding(self, image_path: str):
    image = Image.open(image_path)
    # Preprocess image
    inputs = self.processor(images=image, return_tensors="pt")

    # Get image embeddings
    vector = self.model.get_image_features(**inputs)

    # Isolate the embedding as numpy array
    image_embedding = vector.detach().numpy()[0]

    return image_embedding
  
  def textEmbedding(self, input_text: str):
    # Prepare the text inputs.
    text_inputs = self.processor(text=input_text, return_tensors="pt", padding=True)

    # Get text embeddings.
    vector = self.model.get_text_features(**text_inputs)
    sentence_embedding = vector.detach().numpy()[0]

    return sentence_embedding

