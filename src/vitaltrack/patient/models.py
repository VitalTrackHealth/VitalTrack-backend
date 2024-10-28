"""
Patient models interactions with MongoDB.

'InDB' is add to class names to add more distinction from schemas.
"""

from __future__ import annotations

import uuid
import pydantic

from vitaltrack import core


class PatientInDB(core.models.ModelInDBBase, core.models.AuthenticatedEntity):
    first_name: str = pydantic.Field(default="")
    last_name: str = pydantic.Field(default="")
    email: pydantic.EmailStr = pydantic.Field(default="")
    phone_number: str = pydantic.Field(default="")
    providers: list[uuid.UUID] = pydantic.Field(default=[])

    conditions: list[str] = pydantic.Field(default=[])
    body_measurements: BodyMeasurements = pydantic.Field(
        default_factory=lambda: BodyMeasurements()
    )
    favorites: list[str] = pydantic.Field(default=[])
    nutrition_goals: NutritionGoals = pydantic.Field(
        default_factory=lambda: NutritionGoals()
    )

    disabled: bool = pydantic.Field(default=False)


class BodyMeasurements(core.models.ModelInDBBase):
    height: float = pydantic.Field(default=0, description="Height in centimeters")
    weight: float = pydantic.Field(default=0, description="Weight in kilograms")


class NutritionGoals(core.models.ModelInDBBase):
    calorie: int = pydantic.Field(default=2000, description="Calorie goal")
    protein: int = pydantic.Field(default=150, description="Protein goal")
    fat: int = pydantic.Field(default=65, description="Fat goal")
    carbs: int = pydantic.Field(default=200, description="Carbs goal")
