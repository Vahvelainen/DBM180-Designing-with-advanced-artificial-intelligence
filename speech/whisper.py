import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
from datasets import load_dataset

# pip install datasets
# pip install accelerate
# pip install librosa

device = "cpu"
torch_dtype = torch.float32

if torch.cuda.is_available():
  device = "cuda:0"
  torch_dtype = torch.float16 
# # Mac silicon usable with macOS 13.0 and latest (Nightly) PyTorch
# elif torch.backends.mps.is_available():
#   device = torch.device('mps')

# model_id = "openai/whisper-tiny" # HAHAHA no.
# model_id = "openai/whisper-small" # LOL not quite
# model_id = "openai/whisper-medium" # Very interesting, tends to translate to English
model_id = "openai/whisper-large-v3" # Almost perfect


model = AutoModelForSpeechSeq2Seq.from_pretrained(
    model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True
)
model.to(device)

processor = AutoProcessor.from_pretrained(model_id)

pipe = pipeline(
    "automatic-speech-recognition",
    model=model,
    tokenizer=processor.tokenizer,
    feature_extractor=processor.feature_extractor,
    max_new_tokens=128,
    chunk_length_s=30,
    batch_size=16,
    return_timestamps=True,
    torch_dtype=torch_dtype,
    device=device,
)

dataset = load_dataset("distil-whisper/librispeech_long", "clean", split="validation")
sample = dataset[0]["audio"]

result = pipe('speech/soundfile.m4a')
print(result["text"])
