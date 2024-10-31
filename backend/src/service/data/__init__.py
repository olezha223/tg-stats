from .service import DataService


def get_data_service() -> DataService:
    return DataService()


__all__ = ['DataService', 'get_data_service']
