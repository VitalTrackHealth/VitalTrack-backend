"""
Provider business logic
"""

from __future__ import annotations

import uuid
from typing import Any

from pymongo import ReturnDocument

from vitaltrack import config
from vitaltrack import core

from . import models
from . import schemas
from . import utils


async def register_provider(
    db_manager: core.database.DatabaseManager,
    provider: schemas.ProviderRegisterRequest,
) -> models.ProviderInDB | None:
    # Ensure username and email are the same
    if provider.username != provider.email:
        raise ValueError("Username and email must be the same")

    providers_collection = await db_manager.get_collection(
        config.PROVIDERS_COLLECTION_NAME
    )

    existing_provider = await providers_collection.find_one({"email": provider.email})
    if existing_provider:
        raise ValueError("Provider with this email already exists")

    # Generate provider password hash
    salt = core.utils.generate_salt()
    password_hash = core.utils.get_password_hash(
        provider.password.encode("utf-8"),
        salt,
    )

    # Generate unique provider code
    provider_code = await utils.generate_provider_code(db_manager)

    new_provider = models.ProviderInDB(
        id=uuid.uuid4(),
        password_hash=password_hash,
        salt=salt,
        provider_code=provider_code,
        **provider.model_dump(exclude={"password"}),
    )

    result = await db_manager.db[config.PROVIDERS_COLLECTION_NAME].insert_one(
        new_provider.model_dump(by_alias=True)
    )
    if result.inserted_id:
        return new_provider


async def get_provider(
    db_manager: core.database.DatabaseManager,
    filter: dict[str, Any],
) -> models.ProviderInDB | None:
    providers_collection = await db_manager.get_collection(
        config.PROVIDERS_COLLECTION_NAME
    )
    existing_provider = await providers_collection.find_one(filter)
    if existing_provider:
        return models.ProviderInDB(**existing_provider)


async def update_provider(
    db_manager: core.database.DatabaseManager,
    filter: dict[str, Any],
    provider_update: schemas.ProviderUpdateRequest,
) -> models.ProviderInDB | None:
    # TODO: Update password correctly
    # TODO: Update provider correctly
    providers_collection = await db_manager.get_collection(
        config.PROVIDERS_COLLECTION_NAME
    )

    provider_update_dict = provider_update.model_dump(
        exclude_unset=True, exclude_none=True
    )
    result = await providers_collection.find_one_and_update(
        filter, {"$set": provider_update_dict}, return_document=ReturnDocument.AFTER
    )
    if result:
        return models.ProviderInDB(**result)
