"""
Food endpoints.py
"""

from __future__ import annotations

from typing import Annotated

import fastapi
import httpx

from vitaltrack import config

from . import schemas
from . import utils

router = fastapi.APIRouter()


@router.get(
    "/search",
    # response_model=schemas.FoodsInSearchResponse,
    # response_model_by_alias=False,
)
async def search(ingredient="", brand=""):
    # TODO: Error handling
    # TODO: Add validation to make sure ingredient of brand exists
    res = httpx.get(
        config.EDAMAM_PARSER_URL,
        params={
            "ingr": ingredient,
            "brand": brand,
            "nutrition-type": "logging",
        },
    )
    res_dict = res.json()

    all_food_list = []
    for food in res_dict["hints"]:
        food_edamam = schemas.FoodEdamam(**food["food"])
        food_serving_measure_edamam = schemas.MeasureEdamam()
        food_serving = [d for d in food["measures"] if d["label"] == "Serving"]
        if food_serving:
            food_serving_measure_edamam = schemas.MeasureEdamam(**food_serving[0])

        # Find out serving size
        # Parser response returns macros per 100g
        # See: https://developer.edamam.com/api/faq
        macros_per_gram = {
            "CALORIES": food_edamam.nutrients.get(
                utils.EDAMAM_NUTRIENT_MAPPING["CALORIES"], 0.0
            )
            / 100,
            "PROTEIN": food_edamam.nutrients.get(
                utils.EDAMAM_NUTRIENT_MAPPING["PROTEIN"], 0.0
            )
            / 100,
            "FAT": food_edamam.nutrients.get(utils.EDAMAM_NUTRIENT_MAPPING["FAT"], 0.0)
            / 100,
            "CARBOHYDRATE": food_edamam.nutrients.get(
                utils.EDAMAM_NUTRIENT_MAPPING["CARBOHYDRATE"], 0.0
            )
            / 100,
        }
        macros_per_serving = {**macros_per_gram}
        for macro_key in macros_per_serving:
            macros_per_serving[macro_key] *= food_serving_measure_edamam.weight
        basic_nutrients = schemas.NutrientsBase(**macros_per_serving)

        all_food_list.append(
            schemas.FoodBase(
                **food_edamam.model_dump(exclude={"nutrients"}),
                nutrients=basic_nutrients,
                serving=food_serving_measure_edamam.weight,
            )
        )

    return {
        "message": f"food search returned {len(res_dict['hints']) } items",
        "data": {"suggested": [], "all": all_food_list},
    }


@router.post(
    "/nutrients",
    response_model=schemas.NutrientsInResponse,
    response_model_by_alias=False,
)
async def nutrients(ingredients: schemas.IngredientsInRequest):
    # TODO: Error handling

    res = httpx.post(
        config.EDAMAM_NUTRIENTS_URL,
        # TODO: Edamam doesn't allow multiple ingredients in request?
        json=ingredients.model_dump(by_alias=True),
    )
    res_dict = res.json()

    return {
        "message": "nutrients queried",
        "data": res_dict,
    }
