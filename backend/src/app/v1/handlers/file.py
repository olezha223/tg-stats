from fastapi import APIRouter, Depends, UploadFile
from src.service.files import FilesService, get_files_service

files_router = APIRouter(
    prefix="/files",
    tags=["Files"]
)


@files_router.post("/upload_file/")
async def create_upload_file(
    file: UploadFile,
    user: str,
    name: str,
    service: FilesService = Depends(get_files_service)
):
    return str(await service.upload(file, user, name))


@files_router.delete("/delete_file/")
async def delete_file(
    user: str,
    name: str,
    service: FilesService = Depends(get_files_service)
):
    await service.delete(user, name)


@files_router.put("/update_file/")
async def update_file(
    file: UploadFile,
    user: str,
    name: str,
    service: FilesService = Depends(get_files_service)
):
    await service.update(new_file=file, user=user, name=name)
