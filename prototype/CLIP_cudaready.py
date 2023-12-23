import torch
from transformers import CLIPProcessor, CLIPModel
from PIL import Image

class CLipEncoder():
  '''
    A version of CLIP.py that can use NVIDIA GPUs
    Spoiler: it makes no difference and code is more complicated

    Creates comparable embeddings of length 512 from text and images
    using the CLIP model https://huggingface.co/docs/transformers/model_doc/clip
    with hugginface 
  '''

  def __init__(self):
    self.device = "cpu"
    torch_dtype = torch.float32

    if torch.cuda.is_available():
      self.device = "cuda:0"
      torch_dtype = torch.float16 


    model_name = "openai/clip-vit-base-patch32"
    self.model = CLIPModel.from_pretrained(model_name, torch_dtype=torch_dtype)
    self.processor = CLIPProcessor.from_pretrained(model_name)
    self.model.to(self.device)

  def imageEmbedding(self, image_path: str):
      image = Image.open(image_path)
      image = image.convert("RGB")  # Ensure the image is in the correct format (RGB)
      
      # Preprocess image
      inputs = self.processor(images=image, return_tensors="pt")

      # Move the preprocessed inputs to the same device as the model
      inputs = {k: v.to(self.device) for k, v in inputs.items()}

      # Get image embeddings
      vector = self.model.get_image_features(**inputs)

      # Move vectors back to CPU if needed, then convert to numpy array
      image_embedding = vector.detach().cpu().numpy()[0]

      return image_embedding

  def textEmbedding(self, input_text: str):
      # Prepare the text inputs.
      text_inputs = self.processor(text=input_text, return_tensors="pt", padding=True)

      # Move the prepared text inputs to the same device as the model
      text_inputs = {k: v.to(self.device) for k, v in text_inputs.items()}

      # Get text embeddings.
      vector = self.model.get_text_features(**text_inputs)

      # Move vectors back to CPU if needed, then convert to numpy array
      sentence_embedding = vector.detach().cpu().numpy()[0]

      return sentence_embedding

