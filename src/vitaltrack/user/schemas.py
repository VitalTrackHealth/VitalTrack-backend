"""
User schemas for data validation.
"""

from __future__ import annotations

from typing import Any

import pydantic

from vitaltrack import core
from vitaltrack import food


class UserBase(core.schemas.SchemaBase):
    """
    Base model for user information.

    Attributes:
        first_name: The first name of the user.
        last_name: The last name of the user.
        phone_number: The phone number of the user.
        email: The email address of the user.
        provider: A list of strings representing the providers associated with the user.
        conditions: Conditions a user has.
    """

    first_name: str = pydantic.Field(...)
    last_name: str = pydantic.Field(...)
    phone_number: str = pydantic.Field(...)
    email: pydantic.EmailStr = pydantic.Field(...)
    conditions: list[str] = pydantic.Field(...)
    body_measurements: BodyMeasurements = pydantic.Field()


class BodyMeasurements(core.schemas.SchemaBase):
    height: float = pydantic.Field(description="Height in centimeters")
    weight: float = pydantic.Field(description="Weight in kilograms")


class UserProfile(UserBase):
    foods: list[food.models.FoodInDB] = pydantic.Field(default=[])
    goals: dict[str, Any] = pydantic.Field(default={})


class UserProfileResponse(core.schemas.ResponseBase):
    data: UserProfile = pydantic.Field(...)


class UserInRegister(UserBase):
    """
    User model for handling user data when registering.

    Attributes:
        password: Unhashed password of the user.
    """

    password: str = pydantic.Field(...)
    provider_code: str = pydantic.Field(...)


class UserRegisterResponse(core.schemas.ResponseBase):
    data: UserBase = pydantic.Field(...)


class UserInLogin(core.schemas.SchemaBase):
    """
    User model for handling user data when at login.

    Attributes:
        email: Email of the user.
        password: Unhashed password of the user.
    """

    email: pydantic.EmailStr = pydantic.Field(...)
    password: str = pydantic.Field(...)


class UserLoginResponse(core.schemas.ResponseBase):
    data: dict[str, Any] = pydantic.Field(...)
