"""
Core router.
"""

from typing import Annotated

import fastapi
from fastapi.security import OAuth2PasswordRequestForm

from . import dependencies
from . import schemas
from . import services
from . import exceptions


router = fastapi.APIRouter()


@router.post("/token", response_model=schemas.TokenResponse)
async def login_for_access_token(
    db_manager: dependencies.database_manager_dep,
    form_data: Annotated[OAuth2PasswordRequestForm, fastapi.Depends()],
):
    access_token = await services.authenticate_entity(
        db_manager, form_data.username, form_data.password
    )
    if not access_token:
        raise exceptions.TokenValidationError(detail="Incorrect username or password")
    return {"access_token": access_token, "token_type": "bearer"}
