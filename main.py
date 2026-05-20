import os

import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse

app = FastAPI()

DATA_DIR = "data"

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)


@app.get("/")
async def read_index():
    return FileResponse("index.html")


@app.get("/api/files")
async def get_files():
    supported_extensions = (".mp3", ".wav", ".ogg", ".m4a", ".flac")
    try:
        files = [
            f for f in os.listdir(DATA_DIR) if f.lower().endswith(supported_extensions)
        ]
        return JSONResponse(content={"files": files})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.get("/data/{filename}")
async def get_audio_file(filename: str):
    file_path = os.path.join(DATA_DIR, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return JSONResponse(content={"error": "File not found"}, status_code=404)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
