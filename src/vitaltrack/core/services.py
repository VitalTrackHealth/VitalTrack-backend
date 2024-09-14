"""
Core services
"""

from vitaltrack import config

from . import database
from . import utils
from . import models


async def authenticate_entity(
    db_manager: database.DatabaseManager,
    username: str,
    password: str,
) -> str | None:
    # Try to authenticate as a user
    user_collection = await db_manager.get_collection(config.USERS_COLLECTION_NAME)
    user = await user_collection.find_one({"username": username})
    if user:
        user_model = models.AuthenticatedEntity(**user)
        if user_model.check_password(password):
            return utils.create_access_token(
                data={"sub": user_model.username, "entity_type": "user"}
            )

    # If not a user, try to authenticate as a provider
    provider_collection = await db_manager.get_collection(
        config.PROVIDERS_COLLECTION_NAME
    )
    provider = await provider_collection.find_one({"username": username})
    if provider:
        provider_model = models.AuthenticatedEntity(**provider)
        if provider_model.check_password(password):
            return utils.create_access_token(
                data={"sub": provider_model.username, "entity_type": "provider"}
            )

    return None
