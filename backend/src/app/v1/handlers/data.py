from fastapi import APIRouter, Depends

from src.models.request_models import WhoTextedMore, WhoIgnoredMore, MeanIntervals
from src.models.response_models import ResponseData
from src.service.data import DataService, get_data_service

data_router = APIRouter(
    prefix="/data",
    tags=["Data"]
)


@data_router.post("/who_texted_more/", response_model=ResponseData)
async def get_who_texted_more(
    chat_params: WhoTextedMore,
    service: DataService = Depends(get_data_service)
) -> ResponseData:
    return await service.get_who_texted_more(chat_params)


@data_router.post("/get_who_ignored_more/")
async def get_who_ignored_more(
    chat_params: WhoIgnoredMore,
    service: DataService = Depends(get_data_service)
) -> ResponseData:
    return await service.get_who_ignored_more(chat_params)


@data_router.post("/get_intervals/")
async def get_intervals(
    chat_params: MeanIntervals,
    service: DataService = Depends(get_data_service)
) -> ResponseData:
    return await service.get_intervals(chat_params)
