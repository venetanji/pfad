from fastapi import FastAPI, Response
from xtts_model import XttsStreamer
from fastapi.responses import StreamingResponse
app = FastAPI()
tts = XttsStreamer()
tts.load()

# run this with
# uvicorn.bat xtts_talker:app

@app.post("/tts")
async def tts_endpoint(text: str, chunk_size: int = 2048):
    return StreamingResponse(tts.predict({"text":text,"chunk_size": chunk_size}), media_type="audio/wav")
