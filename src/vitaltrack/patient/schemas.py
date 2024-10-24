"""
Patient schemas for data validation.
"""

from __future__ import annotations

import uuid
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

    body_measurements: BodyMeasurements = pydantic.Field(
        default_factory=lambda: BodyMeasurements()
    )
    conditions: list[str] = pydantic.Field(default=[])


class BodyMeasurements(core.schemas.SchemaBase):
    height: float = pydantic.Field(default=0.0, description="Height in centimeters")
    weight: float = pydantic.Field(default=0.0, description="Weight in kilograms")


class NutritionGoals(core.schemas.SchemaBase):
    calorie: int = pydantic.Field(default=2000, description="Calorie goal")
    protein: int = pydantic.Field(default=150, description="Protein goal")
    fat: int = pydantic.Field(default=65, description="Fat goal")
    carbs: int = pydantic.Field(default=200, description="Carbs goal")


class PatientProfile(PatientBase):
    providers: list[uuid.UUID] = pydantic.Field(default=[])
    foods: list[food.models.FoodInDB] = pydantic.Field(default=[])
    nutrition_goals: NutritionGoals = pydantic.Field(
        default_factory=lambda: NutritionGoals()
    )


################################################################################
# Request Schemas
################################################################################


class PatientRegisterRequest(PatientBase):
    password: str = pydantic.Field(...)
    provider_code: str = pydantic.Field(default="")


class PatientUpdateRequest(PatientBase):
    # Redefines fields to make optional
    username: str = pydantic.Field(description="Email", default="")
    email: pydantic.EmailStr = pydantic.Field(default="")
    password: str = pydantic.Field(default="")


class PatientAddFoodRequest(core.schemas.SchemaBase):
    class _PatientAddFoodRequestItem(core.schemas.SchemaBase):
        food_id: str = pydantic.Field(...)
        food_name: str = pydantic.Field(...)
        details: dict[str, Any] = pydantic.Field(default={})

    foods: list[_PatientAddFoodRequestItem] = pydantic.Field(...)


################################################################################
# Response Schemas
################################################################################


class PatientRegisterResponse(core.schemas.ResponseBase):
    data: PatientBase = pydantic.Field(...)


class PatientLoginResponse(core.schemas.ResponseBase):
    access_token: str = pydantic.Field(...)
    token_type: str = pydantic.Field(...)


class PatientUpdateResponse(core.schemas.ResponseBase):
    data: PatientBase = pydantic.Field(...)


class PatientProfileResponse(core.schemas.ResponseBase):
    data: PatientProfile = pydantic.Field(...)


class PatientFoodLogResponse(core.schemas.ResponseBase):
    # TODO: Abnormal, should call a schema not a model
    data: list[food.models.FoodInDB] = pydantic.Field(...)
