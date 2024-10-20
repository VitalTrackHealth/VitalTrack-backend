"""
Provider dependencies
"""

from typing import Annotated

import fastapi

from vitaltrack import core
from vitaltrack import config

from . import models


async def get_current_provider(
    token_data: core.dependencies.authenticate_dep,
    db_manager: core.dependencies.database_manager_dep,
) -> models.ProviderInDB:
    providers_collection = await db_manager.get_collection(
        config.PROVIDERS_COLLECTION_NAME
    )
    provider = await providers_collection.find_one({"email": token_data.username})

    if provider is None:
        raise core.exceptions.TokenValidationError()

    # Check if provider is disabled
    if provider.get("disabled"):
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_400_BAD_REQUEST, detail="Inactive entity"
        )

    return models.ProviderInDB(**provider)


provider_authenticate_dep = Annotated[
    models.ProviderInDB, fastapi.Depends(get_current_provider)
]
