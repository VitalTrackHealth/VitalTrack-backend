"""
Food buisness logic.
"""

from __future__ import annotations

from typing import Any

from vitaltrack import config
from vitaltrack import core

from . import models


async def get_food_log(
    db_manager: core.database.DatabaseManager,
    filter: dict[str, Any],
) -> list[models.FoodInDB] | None:
    foods_collection = await db_manager.get_collection(config.FOOD_COLLECTION_NAME)
    existing_food_list = await foods_collection.find(filter).to_list(length=None)
    if existing_food_list:
        return [models.FoodInDB(**food) for food in existing_food_list]
