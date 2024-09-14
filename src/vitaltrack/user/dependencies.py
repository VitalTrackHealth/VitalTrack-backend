"""
User dependencies
"""

from typing import Annotated

import fastapi

from vitaltrack import core
from vitaltrack import config

from . import models


async def get_current_user(
    token_data: core.dependencies.authenticate_dep,
    db_manager: core.dependencies.database_manager_dep,
) -> models.UserInDB:
    users_collection = await db_manager.get_collection(config.USERS_COLLECTION_NAME)
    user = await users_collection.find_one({"username": token_data.username})

    if user is None:
        raise core.exceptions.TokenValidationError()

    # Check if user is disabled
    if user.get("disabled"):
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_400_BAD_REQUEST, detail="Inactive entity"
        )

    return models.UserInDB(**user)


user_authenticate_dep = Annotated[models.UserInDB, fastapi.Depends(get_current_user)]
