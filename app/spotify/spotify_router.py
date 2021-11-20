from fastapi import APIRouter
from starlette.responses import JSONResponse

from app.config import settings
from app.logger import setup_custom_logger
from app.spotify.call_spotify import get_songs_features

FIRST_MODULE_TAG = "SPOTIFY"
router = APIRouter()
logger = setup_custom_logger('worker', settings.LOG_LEVEL)


@router.get("/songs_features", tags=[FIRST_MODULE_TAG])
async def test_first_module(album: str, artist: str):
    logger.info("module test request")
    songs_features = get_songs_features(album, artist)
    return JSONResponse(
        status_code=200,
        content=songs_features
    )
