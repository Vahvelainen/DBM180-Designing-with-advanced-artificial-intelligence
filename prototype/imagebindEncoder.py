

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

    def audioEmbedding(self, filepath): #Could be used for getting all the embedding at once if its any better (it might)
        inputs = { ModalityType.AUDIO: data.load_and_transform_audio_data([filepath], self.device) }
        with torch.no_grad():
            tensor = self.model(inputs)['audio']
        return tensor.detach().numpy()[0] 

if __name__ == '__main__':
    image_file = '/Users/leevi/testikuvat/Camera/20191203_144711.jpg'
    audio_file = '/Users/leevi/Datasets/voice recordings/clips/common_voice_en_38488270.mp3'
    text = 'Martijn has a small goose hidden in his closet'
    encoder = ImagebindEncoder()

    text_embedding = encoder.textEmbedding(text)
    print(F"Text Embedding: {text_embedding}")
    print(F"Embedding lenght: {len(text_embedding)}")

    image_embedding = encoder.imageEmbedding(image_file)
    print(F"Image Embedding: {image_embedding}")
    print(F"Embedding lenght: {len(image_embedding)}")

    audio_embedding = encoder.audioEmbedding(audio_file)
    print(F"Audio Embedding: {audio_embedding}")
    print(F"Embedding lenght: {len(audio_embedding)}")
