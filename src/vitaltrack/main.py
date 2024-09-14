"""
FastAPI backend application initialization.
"""

from contextlib import asynccontextmanager

import fastapi
from fastapi.middleware import cors

from vitaltrack import config
from vitaltrack import core
from vitaltrack import food
from vitaltrack import provider
from vitaltrack import user


# Actions before and after the application begins accepting requests.
# See: https://fastapi.tiangolo.com/advanced/events/?h=#lifespan
@asynccontextmanager
async def lifespan(app: fastapi.FastAPI):
    # Setup
    core.database.global_db_manager.connect_to_cluster(url=config.MONGO_DB_URL)
    core.database.global_db_manager.connect_to_database(config.MONGO_DB_DATABASE)
    yield
    # Teardown
    core.database.global_db_manager.close_cluster_connection()


app = fastapi.FastAPI(lifespan=lifespan)

# TODO: Tighten this up
origins = ["*"]

app.add_middleware(
    cors.CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(core.router.router, tags=["core"])
app.include_router(user.router.router, prefix="/user", tags=["user"])
app.include_router(provider.router.router, prefix="/provider", tags=["provider"])
app.include_router(food.router.router, prefix="/food", tags=["food"])
