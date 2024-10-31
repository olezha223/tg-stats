from pydantic import BaseModel
from enum import Enum


class Period(Enum):
    DAY = 1
    WEEK = 7
    TWO_WEEKS = 14
    MONTH = 30
    QUARTER = 120


class WhoTextedMore(BaseModel):
    user: str
    name: str
    interval: Period


class WhoIgnoredMore(BaseModel):
    user: str
    name: str
    min_ignore_minutes: int
    interval: Period


class MeanIntervals(BaseModel):
    user: str
    name: str
    interval: Period
