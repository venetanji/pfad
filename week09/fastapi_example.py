from fastapi import FastAPI
from pydantic import BaseModel

class MusicRequest(BaseModel):
    prompt: str
    seconds: int

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/gio")
def read_root(mr: MusicRequest):
    return {"Hello": "Gio"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0")