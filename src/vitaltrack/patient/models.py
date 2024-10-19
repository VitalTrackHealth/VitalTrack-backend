"""
Patient models interactions with MongoDB.

'InDB' is add to class names to add more distinction from schemas.
"""

from __future__ import annotations

import uuid
import pydantic

from vitaltrack import core
from vitaltrack import food


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
    foods: list[food.models.FoodInDB] = pydantic.Field(default=[])
    favorites: list[str] = pydantic.Field(default=[])

    disabled: bool = pydantic.Field(default=False)


class BodyMeasurements(core.models.ModelInDBBase):
    height: float = pydantic.Field(default=0, description="Height in centimeters")
    weight: float = pydantic.Field(default=0, description="Weight in kilograms")
