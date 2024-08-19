"""
Food models interactions with MongoDB.

'InDB' is add to class names to add more distinction from schemas.
"""

from __future__ import annotations

import time
from typing import Optional

import pydantic

from vitaltrack import core


class FoodInDB(core.models.ModelInDBBase):
    timestamp: Optional[int] = pydantic.Field(default_factory=lambda: int(time.time()))
    food_id: str = pydantic.Field(...)
    tags: Optional[list[str]] = pydantic.Field(default=[])
