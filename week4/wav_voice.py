import torch
from TTS.api import TTS

# Get device
device = "cuda" if torch.cuda.is_available() else "cpu"

# Init TTS
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

tts.tts_to_file(text="Hello, how are you?", file_path="samples/voice.wav", speaker="Wulf Carlevaro", language="en")    