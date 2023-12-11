
# conda install pytorch::pytorch torchvision torchaudio -c pytorch
# pip install soundfile
# pip install git+https://github.com/huggingface/transformers.git
# pip install sentencepiec
# pip install protobuf

import soundfile as sf
from transformers import AutoProcessor, SeamlessM4TModel

TEXT = """This is DBM180 course on designing with advanced AI."""

repo_id = "facebook/hf-seamless-m4t-medium"
processor = AutoProcessor.from_pretrained(repo_id)
model = SeamlessM4TModel.from_pretrained(repo_id)
generated_audio = model.generate(**processor(text=TEXT, src_lang="eng", return_tensors="pt"), tgt_lang="nld")
sf.write("example_sts_translation.wav",  generated_audio[0].numpy().flatten(), samplerate=16000)
