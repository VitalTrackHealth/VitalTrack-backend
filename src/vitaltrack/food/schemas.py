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
    CALCIUM: Optional[float] = pydantic.Field(default=None)
    CARBOHYDRATE_NET: Optional[float] = pydantic.Field(default=None)
    CHOLESTEROL: Optional[float] = pydantic.Field(default=None)
    FATTY_ACIDS_MONOUNSATURATED: Optional[float] = pydantic.Field(default=None)
    FATTY_ACIDS_POLYUNSATURATED: Optional[float] = pydantic.Field(default=None)
    FATTY_ACIDS_SATURATED: Optional[float] = pydantic.Field(default=None)
    FATTY_ACIDS_TRANS: Optional[float] = pydantic.Field(default=None)
    FIBER: Optional[float] = pydantic.Field(default=None)
    FOLATE_DFE: Optional[float] = pydantic.Field(default=None)
    FOLATE_FOOD: Optional[float] = pydantic.Field(default=None)
    FOLIC_ACID: Optional[float] = pydantic.Field(default=None)
    IRON: Optional[float] = pydantic.Field(default=None)
    MAGNESIUM: Optional[float] = pydantic.Field(default=None)
    NIACIN: Optional[float] = pydantic.Field(default=None)
    PHOSPHORUS: Optional[float] = pydantic.Field(default=None)
    POTASSIUM: Optional[float] = pydantic.Field(default=None)
    RIBOFLAVIN: Optional[float] = pydantic.Field(default=None)
    SODIUM: Optional[float] = pydantic.Field(default=None)
    SUGAR_ALCOHOLS: Optional[float] = pydantic.Field(default=None)
    SUGARS_ADDED: Optional[float] = pydantic.Field(default=None)
    SUGARS: Optional[float] = pydantic.Field(default=None)
    THIAMIN: Optional[float] = pydantic.Field(default=None)
    VITAMIN_A_RAE: Optional[float] = pydantic.Field(default=None)
    VITAMIN_B12: Optional[float] = pydantic.Field(default=None)
    VITAMIN_B6: Optional[float] = pydantic.Field(default=None)
    VITAMIN_C: Optional[float] = pydantic.Field(default=None)
    VITAMIN_D: Optional[float] = pydantic.Field(default=None)
    VITAMIN_E: Optional[float] = pydantic.Field(default=None)
    VITAMIN_K: Optional[float] = pydantic.Field(default=None)
    WATER: Optional[float] = pydantic.Field(default=None)
    ZINC: Optional[float] = pydantic.Field(default=None)


class FoodsInSearchResponse(core.schemas.ResponseBase):
    class _OrganizedFoods(core.schemas.SchemaBase):
        suggested: list[FoodBase] = pydantic.Field(...)
        all: list[FoodBase] = pydantic.Field(...)

    data: _OrganizedFoods = pydantic.Field(...)


class IngredientsInRequest(pydantic.BaseModel):
    ingredients: list[IngredientsEdamam] = pydantic.Field(...)


class NutrientsInResponse(core.schemas.ResponseBase):
    class _OrganizedNutrients(core.schemas.SchemaBase):
        nutrients: NutrientsFull = pydantic.Field(...)
        health_labels: list[str] = pydantic.Field(default=[])
        cautions: list[str] = pydantic.Field(default=[])

    data: _OrganizedNutrients = pydantic.Field(...)


class FoodIdsInResponse(core.schemas.ResponseBase): ...
