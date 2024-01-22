from imagebind import data
import torch
from imagebind.models import imagebind_model
from imagebind.models.imagebind_model import ModalityType

class ImagebindEncoder():
    '''
    Class for producing embedding vectors of 1024 dimensions with the imagebind model by MetaAI
    '''

    def __init__(self) -> None:
        self.device = "cuda:0" if torch.cuda.is_available() else "cpu"

        # Instantiate model
        self.model = imagebind_model.imagebind_huge(pretrained=True)
        self.model.eval()
        self.model.to(self.device)

    def textEmbedding(self, text):
        '''
        Get text embdding with imageBind
        1. attribute: input text
        Note: unlike other modalities, text embedding takes the text itself, not a filepath
        '''
        inputs = { ModalityType.TEXT: data.load_and_transform_text([text], self.device) }
        with torch.no_grad():
            tensor = self.model(inputs)['text']
        return tensor.detach().numpy()[0]
    
    def imageEmbedding(self, filepath): 
        '''
        Get image embdding with imageBind
        1. attribute: path to input file
        '''
        inputs = { ModalityType.VISION: data.load_and_transform_vision_data([filepath], self.device) }
        with torch.no_grad():
            tensor = self.model(inputs)['vision']
        return tensor.detach().numpy()[0] 

    def audioEmbedding(self, filepath):
        '''
        Get audio embdding with imageBind
        1. attribute: path to input file
        '''
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
