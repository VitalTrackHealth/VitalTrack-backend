"""
User endpoints.
"""

from __future__ import annotations

import traceback
from typing import Annotated

import fastapi
import pydantic

from vitaltrack import config
from vitaltrack import core
from vitaltrack import food

from . import dependencies
from . import schemas
from . import services

router = fastapi.APIRouter()


@router.post("/register", response_model=schemas.UserRegisterResponse)
async def register_user(
    db_manager: core.dependencies.database_manager_dep,
    user: schemas.UserRegisterRequest,
):
    try:
        registered_user = await services.register_user(db_manager, user)
        if not registered_user:
            raise fastapi.HTTPException(
                status_code=fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to register user",
            )
        return {"user": registered_user.model_dump()}
    except ValueError as e:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e),
        )


@router.post("/update", response_model=schemas.UserUpdateResponse)
async def update_user(
    current_user: dependencies.user_authenticate_dep,
    db_manager: core.dependencies.database_manager_dep,
    update_user: schemas.UserUpdateRequest,
):
    user_in_db = await services.update_user(
        db_manager, {"username": current_user.username}, update_user
    )
    if not user_in_db:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update user",
        )
    return {"user": user_in_db.model_dump()}


@router.get(
    "/profile",
    response_model=schemas.UserProfileResponse,
)
async def profile(
    email: pydantic.EmailStr,
    db_manager: core.dependencies.database_manager_dep,
):
    user_in_db = await services.get_user(db_manager, {"email": email})
    if not user_in_db:
        raise fastapi.HTTPException(status_code=400, detail="incorrect email")

    return {
        "message": "",
        "data": user_in_db.model_dump(),
    }


@router.post(
    "/add-food",
    response_model=food.schemas.FoodIdsInResponse,
)
async def add_food(
    email: Annotated[pydantic.EmailStr, fastapi.Body()],
    food_ids: Annotated[list[str], fastapi.Body()],
    db_manager: core.dependencies.database_manager_dep,
):
    foods = [food.models.FoodInDB(food_id=food_id).model_dump() for food_id in food_ids]
    result = await db_manager.db[config.USERS_COLLECTION_NAME].update_one(
        {"email": email}, {"$push": {"foods": {"$each": foods}}}
    )

    if result.matched_count == 0:
        raise fastapi.HTTPException(status_code=400, detail="no user with email found")

    return {
        "message": f"{result.modified_count} food(s) added",
        "data": {},
    }
