import abc
from pydantic import BaseModel as PydanticBaseModel


class BaseModel(abc.ABC, PydanticBaseModel):
    ...