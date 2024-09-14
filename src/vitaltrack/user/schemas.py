"""
User schemas for data validation.
"""

from __future__ import annotations

from typing import Any

import pydantic

from vitaltrack import core
from vitaltrack import food

################################################################################
# Base Schemas
################################################################################


class UserBase(core.schemas.SchemaBase):
    username: str = pydantic.Field(description="Email")
    first_name: str = pydantic.Field(default="")
    last_name: str = pydantic.Field(default="")
    email: pydantic.EmailStr = pydantic.Field()
    phone_number: str = pydantic.Field(default="")
    providers: list[str] = pydantic.Field(default=[])

    body_measurements: BodyMeasurements = pydantic.Field(
        default_factory=lambda: BodyMeasurements()
    )
    conditions: list[str] = pydantic.Field(default=[])


class BodyMeasurements(core.schemas.SchemaBase):
    height: float = pydantic.Field(default=0.0, description="Height in centimeters")
    weight: float = pydantic.Field(default=0.0, description="Weight in kilograms")


class UserProfile(UserBase):
    foods: list[food.models.FoodInDB] = pydantic.Field(default=[])
    goals: dict[str, Any] = pydantic.Field(default={})


################################################################################
# Request Schemas
################################################################################


class UserRegisterRequest(UserBase):
    password: str = pydantic.Field(...)


class UserUpdateRequest(UserBase):
    # Redefines fields to make optional
    username: str = pydantic.Field(description="Email", default="")
    email: pydantic.EmailStr = pydantic.Field(default="")
    provider_code: str = pydantic.Field(default="")
    password: str = pydantic.Field(default="")


################################################################################
# Response Schemas
################################################################################


class UserRegisterResponse(core.schemas.ResponseBase):
    user: UserBase = pydantic.Field(...)


class UserLoginResponse(core.schemas.ResponseBase):
    access_token: str = pydantic.Field(...)
    token_type: str = pydantic.Field(...)


class UserUpdateResponse(core.schemas.ResponseBase):
    user: UserBase = pydantic.Field(...)


class UserProfileResponse(core.schemas.ResponseBase):
    user: UserProfile = pydantic.Field(...)
