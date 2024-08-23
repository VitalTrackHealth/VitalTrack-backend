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
    response_model=schemas.FoodsInSearchResponse,
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
        macros_per_serving = {}
        for nutrient_code, marco_per_100g in food_edamam.nutrients.items():
            nutrient_name = utils.get_nutrient_name_from_edamam_code(nutrient_code)
            macros_per_serving[nutrient_name] = (
                marco_per_100g / 100
            ) * food_serving_measure_edamam.weight

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
)
async def nutrients(ingredients: schemas.IngredientsInRequest):
    # TODO: Error handling

    res = httpx.post(
        config.EDAMAM_NUTRIENTS_URL,
        # TODO: Edamam doesn't allow multiple ingredients in request?
        json=ingredients.model_dump(by_alias=True),
    )
    res_dict = res.json()

    food_serving_measure_edamam = schemas.MeasureEdamam(weight=res_dict["totalWeight"])

    nutrients_per_100g = {}
    for nutrient_code, marco_per_serving in res_dict["totalNutrients"].items():
        nutrient_name = utils.get_nutrient_name_from_edamam_code(nutrient_code)
        nutrients_per_100g[nutrient_name] = (
            marco_per_serving["quantity"] / food_serving_measure_edamam.weight
        ) * 100

    return {
        "message": "nutrients per 100 grams",
        "data": {
            "nutrients": nutrients_per_100g,
            "health_labels": res_dict.get("healthLabels"),
            "cautions": res_dict.get("cautions"),
        },
    }
