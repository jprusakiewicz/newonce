import os

import uvicorn
from fastapi import FastAPI

from app.spotify import spotify_router

app = FastAPI()


@app.get("/")
async def get():
    return {"status": "ok"}


app.include_router(spotify_router.router, prefix='/spotify')
#
# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=5000)
