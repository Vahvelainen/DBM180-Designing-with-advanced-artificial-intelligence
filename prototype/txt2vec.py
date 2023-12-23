import torch
from transformers import AutoTokenizer, Data2VecTextModel

class textTokenizer:
  '''
    Creates an embedding as numpy array of the length 768 with the facebooks data2vec-text model
  '''

  def __init__(self) -> None:
    # Load pre-trained model tokenizer and model
    self.tokenizer = AutoTokenizer.from_pretrained('facebook/data2vec-text-base')
    self.model = Data2VecTextModel.from_pretrained('facebook/data2vec-text-base')

    # Enter evaluation mode (disables dropout)
    self.model.eval()

  def getEmbedding(self, input_text: str):
    # Encode some text
    encoded_input = self.tokenizer(input_text, return_tensors='pt')

    # Get embeddings from the model
    with torch.no_grad():
        outputs = self.model(**encoded_input)

    # The last_hidden_state is the output of the model
    last_hidden_state = outputs.last_hidden_state

    # You can mean pool the last_hidden_state for a naïve sentence-level embedding
    vector = last_hidden_state.mean(dim=1)

    # Isolate the embedding as numpy array
    sentence_embedding = vector.detach().numpy()[0]

    return sentence_embedding
