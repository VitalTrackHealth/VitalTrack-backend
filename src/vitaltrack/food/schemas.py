"""
Food schemas for data validation.
"""

from __future__ import annotations

import pydantic

from typing import Any
from typing import Optional

from vitaltrack import core


class FoodEdamam(core.schemas.SchemaBase):
    # https://developer.edamam.com/food-database-api-docs
    food_id: str = pydantic.Field(alias="foodId")
    uri: Optional[pydantic.HttpUrl] = pydantic.Field(default=None)
    label: Optional[str] = pydantic.Field(default=None)
    known_as: Optional[str] = pydantic.Field(alias="knownAs", default=None)
    nutrients: Optional[dict[str, Any]] = pydantic.Field(default=None)
    brand: Optional[str] = pydantic.Field(default=None)
    category: Optional[str] = pydantic.Field(default=None)
    category_label: Optional[str] = pydantic.Field(alias="categoryLabel", default=None)
    content_label: Optional[str] = pydantic.Field(
        alias="foodContentsLabel", default=None
    )
    image: Optional[str] = pydantic.Field(default=None)
    serving_sizes: Optional[list[QuantityEdamam]] = pydantic.Field(
        alias="servingSizes", default=None
    )
    servings_per_container: Optional[float] = pydantic.Field(
        alias="servingsPerContainer", default=None
    )


class QuantityEdamam(core.schemas.SchemaBase):
    uri: Optional[pydantic.HttpUrl] = pydantic.Field(default=None)
    label: Optional[str] = pydantic.Field(default=None)
    quantity: Optional[int | float] = pydantic.Field()


class IngredientsEdamam(core.schemas.SchemaBase):
    quantity: int | float = pydantic.Field()
    measure_uri: Optional[int] = pydantic.Field(alias="measureURI", default="")
    qualifiers: Optional[list[str]] = pydantic.Field(default=[])
    food_id: str = pydantic.Field(alias="foodId")


class MeasureEdamam(core.schemas.SchemaBase):
    uri: Optional[pydantic.HttpUrl] = pydantic.Field(default=None)
    label: Optional[str] = pydantic.Field(default=None)
    weight: Optional[float] = pydantic.Field(default=None)
    qualified: Optional[list[dict[Any, Any]]] = pydantic.Field()


class FoodsInSearchResponse(core.schemas.ResponseBase):
    class _OrganizedFoods(core.schemas.SchemaBase):
        suggested: list[FoodEdamam] = pydantic.Field(...)
        all: list[FoodEdamam] = pydantic.Field(...)

    data: _OrganizedFoods = pydantic.Field(...)


class IngredientsInRequest(pydantic.BaseModel):
    ingredients: list[IngredientsEdamam] = pydantic.Field(...)


class NutrientsInResponse(core.schemas.ResponseBase):
    data: dict[str, Any] = pydantic.Field(...)


class FoodIdsInResponse(core.schemas.ResponseBase): ...
