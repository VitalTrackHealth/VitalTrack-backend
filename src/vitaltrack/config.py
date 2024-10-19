"""
Global config variables.
"""

import os

import dotenv


API_V1_STR = "/api/v1"

dotenv.load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

MONGO_DB_USER = os.getenv("MONGO_DB_USER")
MONGO_DB_PASSWORD = os.getenv("MONGO_DB_PASSWORD")
MONGO_DB_CLUSTER = os.getenv("MONGO_DB_CLUSTER")
MONGO_DB_URL = (
    f"mongodb+srv://{MONGO_DB_USER}:{MONGO_DB_PASSWORD}@{MONGO_DB_CLUSTER}.mongodb.net"
)
MONGO_DB_DATABASE = os.getenv("MONGO_DB_DATABASE")

MIN_CONNECTIONS_COUNT = 10
MAX_CONNECTIONS_COUNT = 10

EDAMAM_API_ID = os.getenv("EDAMAM_API_ID")
EDAMAM_API_KEY = os.getenv("EDAMAM_API_KEY")
EDAMAM_PARSER_URL = f"https://api.edamam.com/api/food-database/v2/parser?app_id={EDAMAM_API_ID}&app_key={EDAMAM_API_KEY}"
EDAMAM_NUTRIENTS_URL = f"https://api.edamam.com/api/food-database/v2/nutrients?app_id={EDAMAM_API_ID}&app_key={EDAMAM_API_KEY}"

PATIENTS_COLLECTION_NAME = "patient"
PROVIDERS_COLLECTION_NAME = "provider"
FOOD_COLLECTION_NAME = "food"
