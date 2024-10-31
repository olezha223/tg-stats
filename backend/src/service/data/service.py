import datetime

from .interface import DataServiceInterface
from ...database import get_db
from ...models.request_models import WhoTextedMore
from ...models.response_models import ResponseData
from ...repository import MongoRepository, get_repository


class DataService(DataServiceInterface):
    def __init__(self):
        self.repo: MongoRepository = get_repository()

    async def get_who_texted_more(
            self,
            model: WhoTextedMore
    ) -> ResponseData:
        async with (get_db() as session):
            result = await self.repo.get_who_texted_more(session, model)
        return ResponseData.model_validate(
            {'author_1': model.user, "author_2": model.name, "metric_1": result[0], "metric_2": result[1]},
            from_attributes=True)

    async def get_who_ignored_more(
            self,
            model
    ) -> ResponseData:
        async with get_db() as session:
            result = await self.repo.get_who_ignored_more(session, model)
        return ResponseData.model_validate(
            {'author_1': model.user, "author_2": model.name, "metric_1": result[0], "metric_2": result[1]},
            from_attributes=True)


    async def get_intervals(
            self,
            model
    ):
        async with get_db() as session:
            result = await self.repo.get_intervals(session, model)
        return ResponseData.model_validate(
            {'author_1': model.user, "author_2": model.name, "metric_1": result[0], "metric_2": result[1]},
            from_attributes=True)

