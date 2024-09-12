"""
User schemas for data validation.
"""

from __future__ import annotations

from typing import Any
from typing import Optional

import pydantic

from vitaltrack import core
from vitaltrack import food


class UserBase(core.schemas.SchemaBase):
    first_name: str = pydantic.Field(...)
    last_name: str = pydantic.Field(...)
    phone_number: str = pydantic.Field(...)
    email: pydantic.EmailStr = pydantic.Field(...)
    body_measurements: Optional[BodyMeasurements] = pydantic.Field(
        default_factory=lambda: BodyMeasurements()
    )
    conditions: Optional[list[str]] = pydantic.Field(default=[])


class BodyMeasurements(core.schemas.SchemaBase):
    height: float = pydantic.Field(default=0.0, description="Height in centimeters")
    weight: float = pydantic.Field(default=0.0, description="Weight in kilograms")


class UserProfile(UserBase):
    foods: list[food.models.FoodInDB] = pydantic.Field(default=[])
    goals: dict[str, Any] = pydantic.Field(default={})


class UserProfileResponse(core.schemas.ResponseBase):
    data: UserProfile = pydantic.Field(...)


class UserInRegister(UserBase):
    password: str = pydantic.Field(...)
    provider_code: Optional[str] = pydantic.Field(default="")


class UserRegisterResponse(core.schemas.ResponseBase):
    data: UserBase = pydantic.Field(...)


class UserInLogin(core.schemas.SchemaBase):
    email: pydantic.EmailStr = pydantic.Field(...)
    password: str = pydantic.Field(...)


class UserLoginResponse(core.schemas.ResponseBase):
    data: UserBase = pydantic.Field(...)


class UserInUpdate(core.schemas.SchemaBase):
    email: pydantic.EmailStr = pydantic.Field(...)
    first_name: Optional[str] = pydantic.Field(default="")
    last_name: Optional[str] = pydantic.Field(default="")
    phone_number: Optional[str] = pydantic.Field(default="")
    body_measurements: Optional[BodyMeasurements] = pydantic.Field(default={})
    conditions: Optional[list[str]] = pydantic.Field(default=[])
    password: Optional[str] = pydantic.Field(default="")
    provider_code: Optional[str] = pydantic.Field(default="")


class UserUpdateResponse(core.schemas.ResponseBase):
    data: UserBase = pydantic.Field(...)
