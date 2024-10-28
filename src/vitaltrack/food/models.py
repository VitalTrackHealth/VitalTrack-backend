"""
Food models interactions with MongoDB.

'InDB' is add to class names to add more distinction from schemas.
"""

from __future__ import annotations

import time
import uuid
from typing import Any
from typing import Optional

import pydantic
import pydantic_mongo

from vitaltrack import core


class FoodInDB(core.models.ModelInDBBase):
    id: pydantic_mongo.PydanticObjectId = pydantic.Field(
        alias="_id", default_factory=pydantic_mongo.PydanticObjectId
    )
    added_at: Optional[int] = pydantic.Field(default_factory=lambda: int(time.time()))
    food_id: str = pydantic.Field(...)
    patient_id: uuid.UUID = pydantic.Field(default=None)
    food_name: str = pydantic.Field(...)
    tags: Optional[list[str]] = pydantic.Field(default=[])
    details: Optional[dict[str, Any]] = pydantic.Field(default={})
