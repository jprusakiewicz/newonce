from fastapi import APIRouter
from starlette.responses import JSONResponse

from ..config import settings
from ..logger import setup_custom_logger

FIRST_MODULE_TAG = "FIRST_MODULE"
router = APIRouter()
logger = setup_custom_logger('worker', settings.LOG_LEVEL)


@router.get("/test", tags=[FIRST_MODULE_TAG])
async def test_first_module():
    logger.info("module test request")
    return JSONResponse(
        status_code=200,
        content={"detail": "success"}
    )
