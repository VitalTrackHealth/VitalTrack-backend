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
    weight: Optional[float] = pydantic.Field(default=100, description="Weight in grams")
    qualified: Optional[list[dict[Any, Any]]] = pydantic.Field(default=[])


class FoodBase(core.schemas.SchemaBase):
    food_id: str = pydantic.Field()
    label: str = pydantic.Field(default=None)
    known_as: str = pydantic.Field(default=None)
    brand: Optional[str] = pydantic.Field(default=None)
    serving: float = pydantic.Field(default=100, description="Serving size in grams")
    nutrients: NutrientsBase = pydantic.Field(default=None)


class FoodFull(FoodBase):
    nutrients: NutrientsFull = pydantic.Field(default=None)


class NutrientsBase(core.schemas.SchemaBase):
    CALORIES: float = pydantic.Field()
    CARBOHYDRATE: float = pydantic.Field()
    FAT: float = pydantic.Field()
    PROTEIN: float = pydantic.Field()


class NutrientsFull(NutrientsBase):
    CALCIUM: float = pydantic.Field()
    CARBOHYDRATE_NET: float = pydantic.Field()
    CHOLESTEROL: float = pydantic.Field()
    FATTY_ACIDS_MONOUNSATURATED: float = pydantic.Field()
    FATTY_ACIDS_POLYUNSATURATED: float = pydantic.Field()
    FATTY_ACIDS_SATURATED: float = pydantic.Field()
    FATTY_ACIDS_TRANS: float = pydantic.Field()
    FIBER: float = pydantic.Field()
    FOLATE_DFE: float = pydantic.Field()
    FOLATE_FOOD: float = pydantic.Field()
    FOLIC_ACID: float = pydantic.Field()
    IRON: float = pydantic.Field()
    MAGNESIUM: float = pydantic.Field()
    NIACIN: float = pydantic.Field()
    PHOSPHORUS: float = pydantic.Field()
    POTASSIUM: float = pydantic.Field()
    RIBOFLAVIN: float = pydantic.Field()
    SODIUM: float = pydantic.Field()
    SUGAR_ALCOHOLS: float = pydantic.Field()
    SUGARS_ADDED: float = pydantic.Field()
    SUGARS: float = pydantic.Field()
    THIAMIN: float = pydantic.Field()
    VITAMIN_A_RAE: float = pydantic.Field()
    VITAMIN_B12: float = pydantic.Field()
    VITAMIN_B6: float = pydantic.Field()
    VITAMIN_C: float = pydantic.Field()
    VITAMIN_D: float = pydantic.Field()
    VITAMIN_E: float = pydantic.Field()
    VITAMIN_K: float = pydantic.Field()
    WATER: float = pydantic.Field()
    ZINC: float = pydantic.Field()


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
