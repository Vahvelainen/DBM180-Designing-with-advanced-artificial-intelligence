
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration

class BlipDecoder():
  def __init__(self) -> None:
    self.processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
    self.model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

  def caption(self, image_path: str):
    raw_image = Image.open(image_path)
    # unconditional image captioning
    inputs = self.processor(raw_image, return_tensors="pt")
    out = self.model.generate(**inputs, max_new_tokens=20)
    return self.processor.decode(out[0], skip_special_tokens=True)
