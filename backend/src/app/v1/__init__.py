from fastapi import APIRouter

from src.app.v1.handlers.file import files_router
from src.app.v1.handlers.data import data_router

router_v1 = APIRouter(prefix="/v1")

router_v1.include_router(files_router)
router_v1.include_router(data_router)