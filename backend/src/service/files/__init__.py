from .service import FilesService


def get_files_service() -> FilesService:
    return FilesService()


__all__ = ['FilesService', 'get_files_service']
