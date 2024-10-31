from abc import ABC, abstractmethod


class FilesServiceInterface(ABC):
    """Интерфейс для работы с файлами json"""

    @abstractmethod
    async def upload(self, file, user, name):
        ...

    @abstractmethod
    async def delete(self, user, name):
        ...
