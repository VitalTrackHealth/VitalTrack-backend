"""
Provider schemas for data validation.
"""

from __future__ import annotations

from typing import Any

import pydantic

from vitaltrack import core
from vitaltrack import patient

################################################################################
# Base Schemas
################################################################################


class ProviderBase(core.schemas.SchemaBase):
    username: str = pydantic.Field(description="Email")
    first_name: str = pydantic.Field(default="")
    last_name: str = pydantic.Field(default="")
    email: pydantic.EmailStr = pydantic.Field()
    phone_number: str = pydantic.Field(default="")


class ProviderProfile(ProviderBase):
    provider_code: str = pydantic.Field(...)


################################################################################
# Request Schemas
################################################################################


class ProviderRegisterRequest(ProviderBase):
    password: str = pydantic.Field(...)


class ProviderUpdateRequest(ProviderBase):
    # Redefines fields to make optional
    username: str = pydantic.Field(description="Email", default="")
    email: pydantic.EmailStr = pydantic.Field(default="")
    password: str = pydantic.Field(default="")


################################################################################
# Response Schemas
################################################################################


class ProviderRegisterResponse(core.schemas.ResponseBase):
    data: ProviderProfile = pydantic.Field(...)


class ProviderLoginResponse(core.schemas.ResponseBase):
    access_token: str = pydantic.Field(...)
    token_type: str = pydantic.Field(...)


class ProviderUpdateResponse(core.schemas.ResponseBase):
    data: ProviderProfile = pydantic.Field(...)


class ProviderCodeCheckResponse(core.schemas.ResponseBase):
    message: str = pydantic.Field(...)


class PatientsListResponse(core.schemas.ResponseBase):
    data: list[patient.schemas.PatientProfile] = pydantic.Field(...)


class ProviderProfileResponse(core.schemas.ResponseBase):
    data: ProviderProfile = pydantic.Field(...)
