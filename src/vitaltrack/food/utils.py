"""
Food Utilities.
"""

EDAMAM_NUTRIENT_MAPPING = {
    "CALCIUM": "CA",
    "CARBOHYDRATE": "CHOCDF",
    "CARBOHYDRATE_NET": "CHOCDF.net",
    "CHOLESTEROL": "CHOLE",
    "CALORIES": "ENERC_KCAL",
    "FATTY_ACIDS_MONOUNSATURATED": "FAMS",
    "FATTY_ACIDS_POLYUNSATURATED": "FASAT",
    "FATTY_ACIDS_SATURATED": "FAPU",
    "FAT": "FAT",
    "FATTY_ACIDS_TRANS": "FATRN",
    "IRON": "FE",
    "FIBER": "FIBTG",
    "FOLIC_ACID": "FOLAC",
    "FOLATE_DFE": "FOLDFE",
    "FOLATE_DFE": "FOLDFE",
    "FOLATE_FOOD": "FOLFD",
    "POTASSIUM": "K",
    "MAGNESIUM": "MG",
    "SODIUM": "NA",
    "NIACIN": "NIA",
    "PHOSPHORUS": "P",
    "PROTEIN": "PROCNT",
    "RIBOFLAVIN": "RIBF",
    "SUGARS": "SUGAR",
    "SUGARS_ADDED": "SUGAR.added",
    "SUGAR_ALCOHOLS": "Sugar.alcohol",
    "THIAMIN": "THIA",
    "Vitamin_E": "TOCPHA",
    "Vitamin_A_RAE": "VITA_RAE",
    "Vitamin_B12": "VITB12",
    "Vitamin_B6": "VITB6A",
    "Vitamin_C": "VITC",
    "Vitamin_D": "VITD",
    "Vitamin_K": "VITK1",
    "WATER": "WATER",
    "ZINC": "ZN",
}

REVERSE_EDAMAM_NUTRIENT_MAPPING = {v: k for k, v in EDAMAM_NUTRIENT_MAPPING.items()}


def get_edamam_nutrient_code(nutrient_name: str):
    return EDAMAM_NUTRIENT_MAPPING.get(nutrient_name, None)


def get_nutrient_name_from_edamam_code(nutrient_code: str):
    return REVERSE_EDAMAM_NUTRIENT_MAPPING.get(nutrient_code, None)
