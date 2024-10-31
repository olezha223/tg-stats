from fastapi import UploadFile
import json
from .interface import FilesServiceInterface
from ...database import get_db
from ...repository import get_repository, MongoRepository


class FilesService(FilesServiceInterface):

    def __init__(self):
        self.repo: MongoRepository = get_repository()

    async def upload(self, file: UploadFile, user: str, name: str):
        data = json.loads(file.file.read())
        async with get_db() as session:
            return await self.repo.add_chat(session=session, data=data, user=user, name=name)

    async def delete(self, user: str, name: str):
        async with get_db() as session:
            await self.repo.delete_chat(session, user, name)

    async def update(self, user: str, name: str, new_file: UploadFile):
        data = json.loads(new_file.file.read())
        async with get_db() as session:
            return await self.repo.update_chat(session=session, new_data=data, user=user, name=name)
