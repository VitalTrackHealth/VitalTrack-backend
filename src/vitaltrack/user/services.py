"""
User business logic
"""

from __future__ import annotations

from typing import Any

from pymongo import ReturnDocument

from vitaltrack import config
from vitaltrack import core

from . import models


async def get_user(
    db_manager: core.database.DatabaseManager,
    filter: dict[str, Any],
) -> models.UserInDB | None:
    result = await db_manager.db[config.USERS_COLLECTION_NAME].find_one(filter)
    if result:
        return models.UserInDB(**result)


async def update_user(
    db_manager: core.database.DatabaseManager,
    filter: dict[str, Any],
    userUpdate: dict[str, Any],
) -> models.UserInDB | None:
    # TODO: Update password correctly
    # TODO: Update provider correctly
    result = await db_manager.db[config.USERS_COLLECTION_NAME].find_one_and_update(
        filter, {"$set": userUpdate}, return_document=ReturnDocument.AFTER
    )
    if result:
        return models.UserInDB(**result)
