"""
Patient schemas for data validation.
"""

from __future__ import annotations

from typing import Any

import pydantic

from vitaltrack import core
from vitaltrack import food

################################################################################
# Base Schemas
################################################################################


class PatientBase(core.schemas.SchemaBase):
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


class PatientProfile(PatientBase):
    foods: list[food.models.FoodInDB] = pydantic.Field(default=[])
    goals: dict[str, Any] = pydantic.Field(default={})


################################################################################
# Request Schemas
################################################################################


class PatientRegisterRequest(PatientBase):
    password: str = pydantic.Field(...)


class PatientUpdateRequest(PatientBase):
    # Redefines fields to make optional
    username: str = pydantic.Field(description="Email", default="")
    email: pydantic.EmailStr = pydantic.Field(default="")
    provider_code: str = pydantic.Field(default="")
    password: str = pydantic.Field(default="")


################################################################################
# Response Schemas
################################################################################


class PatientRegisterResponse(core.schemas.ResponseBase):
    patient: PatientBase = pydantic.Field(...)


class PatientLoginResponse(core.schemas.ResponseBase):
    access_token: str = pydantic.Field(...)
    token_type: str = pydantic.Field(...)


class PatientUpdateResponse(core.schemas.ResponseBase):
    patient: PatientBase = pydantic.Field(...)


class PatientProfileResponse(core.schemas.ResponseBase):
    patient: PatientProfile = pydantic.Field(...)
