"""
Application dependenices.

See: https://fastapi.tiangolo.com/tutorial/dependencies/
"""

from typing import Annotated

import fastapi
import jwt

from . import database
from . import exceptions
from . import schemas
from . import utils

database_manager_dep = Annotated[
    database.DatabaseManager, fastapi.Depends(database.get_database_manager)
]

oauth2_scheme = fastapi.security.OAuth2PasswordBearer(tokenUrl="token")
oauth2_scheme_dep = Annotated[str, fastapi.Depends(oauth2_scheme)]


async def get_current_entity(
    token: oauth2_scheme_dep,
) -> schemas.TokenData:
    # Decode token
    try:
        payload = utils.decode_access_token(token)
        username = payload.get("sub")
        entity_type = payload.get("entity_type")
        if username is None or entity_type is None:
            raise exceptions.TokenValidationError()
        token_data = schemas.TokenData(username=username, entity_type=entity_type)
    except jwt.exceptions.InvalidTokenError:
        raise exceptions.TokenValidationError()

    return token_data


authenticate_dep = Annotated[schemas.TokenData, fastapi.Depends(get_current_entity)]
