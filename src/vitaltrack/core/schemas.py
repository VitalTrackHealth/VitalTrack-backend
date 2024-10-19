"""
Global schemas for data validation.
"""

from typing import Literal

import pydantic


################################################################################
# Base Schemas
################################################################################


class SchemaBase(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(populate_by_name=True, extra="ignore")


class ResponseBase(pydantic.BaseModel): ...


class ErrorResponseBase(pydantic.BaseModel):
    message: str = pydantic.Field(...)


class Token(pydantic.BaseModel):
    access_token: str = pydantic.Field(...)
    token_type: str = pydantic.Field(...)


class TokenData(pydantic.BaseModel):
    username: str = pydantic.Field(default="")
    entity_type: Literal["patient", "provider"] = pydantic.Field(default="")


################################################################################
# Response Schemas
################################################################################


class TokenResponse(SchemaBase):
    access_token: str = pydantic.Field(...)
    token_type: str = pydantic.Field(...)
