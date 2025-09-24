from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import torch
from TTS.api import TTS
import uuid


app = FastAPI()

# Get device
device = "cuda" if torch.cuda.is_available() else "cpu"

# Init TTS
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
output_path = "samples/"

class TTSRequest(BaseModel):
    text: str
    language: str = "en"
    speaker_wav: str = None

@app.post("/generate_audio/")
async def generate_audio(request: TTSRequest):
    # Generate audio file

    tts_kwargs = {
        "text": request.text,
        "language": request.language,
        "file_path": f'{output_path}{uuid.uuid1()}.wav'
    }

    if request.speaker_wav:
        tts_kwargs["speaker_wav"] = request.speaker_wav
    else:
        tts_kwargs["speaker"] = "Wulf Carlevaro"

    
    tts.tts_to_file(**tts_kwargs)
    
    return {"file_path": tts_kwargs["file_path"]}


# To run the FastAPI app, use the command: uvicorn wav_talker:app --reload

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)