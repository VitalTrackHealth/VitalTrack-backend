"""
User business logic
"""

from __future__ import annotations

import uuid
from typing import Any

from pymongo import ReturnDocument

from vitaltrack import config
from vitaltrack import core

from . import models
from . import schemas


async def register_user(
    db_manager: core.database.DatabaseManager,
    user: schemas.UserRegisterRequest,
) -> models.UserInDB | None:
    # Ensure username and email are the same
    if user.username != user.email:
        raise ValueError("Username and email must be the same")

    users_collection = await db_manager.get_collection(config.USERS_COLLECTION_NAME)

    existing_user = await users_collection.find_one({"username": user.username})
    if existing_user:
        raise ValueError("User with this email already exists")

    # Generate user password hash
    salt = core.utils.generate_salt()
    password_hash = core.utils.get_password_hash(
        user.password.encode("utf-8"),
        salt,
    )

    new_user = models.UserInDB(
        id=uuid.uuid4(),
        password_hash=password_hash,
        salt=salt,
        disabled=False,
        **user.model_dump(exclude={"password"}),
    )
    result = await users_collection.insert_one(new_user.model_dump(by_alias=True))
    if result.inserted_id:
        return new_user


async def get_user(
    db_manager: core.database.DatabaseManager,
    filter: dict[str, Any],
) -> models.UserInDB | None:
    users_collection = await db_manager.get_collection(config.USERS_COLLECTION_NAME)
    existing_user = await users_collection.find_one(filter)
    if existing_user:
        return models.UserInDB(**existing_user)


async def update_user(
    db_manager: core.database.DatabaseManager,
    filter: dict[str, Any],
    user_update: schemas.UserUpdateRequest,
) -> models.UserInDB | None:
    # TODO: Update password correctly
    # TODO: Update provider correctly
    users_collection = await db_manager.get_collection(config.USERS_COLLECTION_NAME)

    user_update_dict = user_update.model_dump(exclude_unset=True, exclude_none=True)
    result = await users_collection.find_one_and_update(
        filter, {"$set": user_update_dict}, return_document=ReturnDocument.AFTER
    )
    if result:
        return models.UserInDB(**result)


async def add_provider_to_user(
    db_manager: core.database.DatabaseManager,
    user_id: uuid.UUID,
    provider_id: uuid.UUID,
) -> models.UserInDB | None:
    users_collection = await db_manager.get_collection(config.USERS_COLLECTION_NAME)

    result = await users_collection.find_one_and_update(
        {"_id": user_id},
        {"$addToSet": {"provider": provider_id}},
        return_document=ReturnDocument.AFTER,
    )
    if result.upserted_id:
        return models.UserInDB(**result)

    #     # Add Provider relationship
    # provider_in_db = await provider.services.get_provider(
    #     db_manager, {"provider_code": user_in_req_dict["provider_code"]}
    # )
    # provider_in_db_id_list = []
    # if provider_in_db:
    #     provider_in_db_id_list.append(provider_in_db.id)

    # if provider_in_db:
    #     await db_manager.db[config.PROVIDERS_COLLECTION_NAME].update_one(
    #         {"_id": provider_in_db.id}, {"$addToSet": {"users": new_user.id}}
    #     )
