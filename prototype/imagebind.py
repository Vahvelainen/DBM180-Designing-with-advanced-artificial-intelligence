

from imagebind import data
import torch
from imagebind.models import imagebind_model
from imagebind.models.imagebind_model import ModalityType

class ImagebindEncoder():

    def __init__(self) -> None:
        self.device = "cuda:0" if torch.cuda.is_available() else "cpu"

        # Instantiate model
        self.model = imagebind_model.imagebind_huge(pretrained=True)
        self.model.eval()
        self.model.to(self.device)

    def textEmbedding(self, text): #Could be used for getting all the embedding at once if its any better (it might)
        inputs = { ModalityType.TEXT: data.load_and_transform_text([text], self.device) }
        with torch.no_grad():
            tensor = self.model(inputs)['text']
        return tensor.detach().numpy()[0]
    
    def imageEmbedding(self, filepath): #Could be used for getting all the embedding at once if its any better (it might)
        inputs = { ModalityType.VISION: data.load_and_transform_vision_data([filepath], self.device) }
        with torch.no_grad():
            tensor = self.model(inputs)['vision']
        return tensor.detach().numpy()[0] 

    def imageEmbedding(self, filepath): #Could be used for getting all the embedding at once if its any better (it might)
        inputs = { ModalityType.AUDIO: data.load_and_transform_audio_data([filepath], self.device) }
        with torch.no_grad():
            tensor = self.model(inputs)['audio']
        return tensor.detach().numpy()[0] 

if __name__ == '__main__':
    file = '/Users/leevi/testikuvat/Camera/20191203_144711.jpg'
    encoder = ImagebindEncoder()
    embedding = encoder.imageEmbedding(file)
    print(F"Embedding: {embedding}")
    print(F"Embedding lenght: {len(embedding)}")
