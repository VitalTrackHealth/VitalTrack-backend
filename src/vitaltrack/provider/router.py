"""
Provider endpoints.
"""

from __future__ import annotations

import uuid

import fastapi
import pydantic

from vitaltrack import core
from vitaltrack import patient

from . import dependencies
from . import schemas
from . import services


router = fastapi.APIRouter()


@router.post("/register", response_model=schemas.ProviderRegisterResponse)
async def register_provider(
    db_manager: core.dependencies.database_manager_dep,
    provider: schemas.ProviderRegisterRequest,
):
    try:
        registered_provider = await services.register_provider(db_manager, provider)
        if not registered_provider:
            raise fastapi.HTTPException(
                status_code=fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to register provider",
            )
        return {"data": registered_provider.model_dump()}
    except ValueError as e:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e),
        )


@router.post("/update", response_model=schemas.ProviderUpdateResponse)
async def update_provider(
    current_provider: dependencies.provider_authenticate_dep,
    db_manager: core.dependencies.database_manager_dep,
    update_provider: schemas.ProviderUpdateRequest,
):
    provider_in_db = await services.update_provider(
        db_manager, {"email": current_provider.email}, update_provider
    )
    if not provider_in_db:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update provider",
        )
    return {"data": provider_in_db.model_dump()}


@router.get(
    "/profile",
    response_model=schemas.ProviderProfileResponse,
)
async def profile(
    current_provider: dependencies.provider_authenticate_dep,
    db_manager: core.dependencies.database_manager_dep,
):
    provider_in_db = await services.get_provider(
        db_manager, {"email": current_provider.email}
    )
    if not provider_in_db:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get provider",
        )
    return {"data": provider_in_db.model_dump()}


@router.get(
    "/check-provider-code",
    response_model=schemas.ProviderCodeCheckResponse,
)
async def check_provider_code(
    provider_code: str,
    db_manager: core.dependencies.database_manager_dep,
):
    provider_in_db = await services.get_provider(
        db_manager, {"provider_code": provider_code}
    )
    if not provider_in_db:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
            detail="Provider code is invalid",
        )
    return {"message": "Provider code is valid"}


@router.get(
    "/patients",
    response_model=schemas.PatientsListResponse,
)
async def profile(
    current_provider: dependencies.provider_authenticate_dep,
    db_manager: core.dependencies.database_manager_dep,
):
    provider_in_db = await services.get_provider(
        db_manager, {"email": current_provider.email}
    )
    if not provider_in_db:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get provider",
        )

    patient_list = []
    for patient_id in provider_in_db.patients:
        patient_in_db = await patient.services.get_patient(
            db_manager, {"_id": patient_id}
        )
        patient_list.append(
            patient.schemas.PatientProfile(**patient_in_db.model_dump())
        )

    return {
        "message": f"{len(patient_list)} patient(s) found",
        "data": patient_list,
    }
