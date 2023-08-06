"""
Defines DTOs used to load/dump objects from JSON.
"""
# pylint: disable=too-few-public-methods,missing-class-docstring

from enum import Enum
from typing import Optional

import pydantic


class BaseModel(pydantic.BaseModel):  # pylint: disable=no-member
    class Config:
        orm_mode = True


class TestStatus(Enum):
    N_A = "n/a"
    RUNNING = "running"
    PENDING = "pending"
    FAILED = "failed"
    SUCCEED = "succeed"


class TestStatusReadDTO(BaseModel):
    modulename: str
    classname: Optional[str]
    fullname: str
    funcname: str

    status: TestStatus
    refresh_date: Optional[str]
