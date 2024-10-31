from .mongo_repository import MongoRepository
from .interface import RepositoryInterface


def get_repository() -> MongoRepository:
    return MongoRepository()


__all__ = [
    'get_repository',
    'MongoRepository',
]
