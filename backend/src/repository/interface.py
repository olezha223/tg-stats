from typing import Any
from bson import ObjectId
from abc import ABC, abstractmethod


class RepositoryInterface(ABC):
    """Интерфейс сервиса по работе с публикациями"""
