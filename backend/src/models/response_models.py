from pydantic import BaseModel
from datetime import datetime
from enum import Enum


class ResponseData(BaseModel):
    author_1: str
    author_2: str
    metric_1: dict[str, int | float]
    metric_2: dict[str, int | float]


class SaveStatus(Enum):
    OK = "ok"
    ERROR = "error"
