"""
Patient endpoints.
"""

from __future__ import annotations

from typing import Annotated

import fastapi
import pydantic

from vitaltrack import config
from vitaltrack import core
from vitaltrack import food

from . import dependencies
from . import schemas
from . import services

router = fastapi.APIRouter()


@router.post("/register", response_model=schemas.PatientRegisterResponse)
async def register_patient(
    db_manager: core.dependencies.database_manager_dep,
    patient: schemas.PatientRegisterRequest,
):
    try:
        registered_patient = await services.register_patient(db_manager, patient)
        if not registered_patient:
            raise fastapi.HTTPException(
                status_code=fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to register patient",
            )
        return {"data": registered_patient.model_dump()}
    except ValueError as e:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e),
        )


@router.post("/update", response_model=schemas.PatientUpdateResponse)
async def update_patient(
    current_patient: dependencies.patient_authenticate_dep,
    db_manager: core.dependencies.database_manager_dep,
    update_patient: schemas.PatientUpdateRequest,
):
    patient_in_db = await services.update_patient(
        db_manager, {"username": current_patient.username}, update_patient
    )
    if not patient_in_db:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update patient",
        )
    return {"data": patient_in_db.model_dump()}


@router.get(
    "/profile",
    response_model=schemas.PatientProfileResponse,
)
async def profile(
    current_patient: dependencies.patient_authenticate_dep,
    db_manager: core.dependencies.database_manager_dep,
):
    patient_in_db = await services.get_patient(
        db_manager, {"username": current_patient.username}
    )
    if not patient_in_db:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get patient",
        )
    return {"data": patient_in_db.model_dump()}


@router.post(
    "/add-food",
    response_model=food.schemas.FoodIdsInResponse,
)
async def add_food(
    email: Annotated[pydantic.EmailStr, fastapi.Body()],
    food_ids: Annotated[list[str], fastapi.Body()],
    db_manager: core.dependencies.database_manager_dep,
):
    foods = [food.models.FoodInDB(food_id=food_id).model_dump() for food_id in food_ids]
    result = await db_manager.db[config.PATIENTS_COLLECTION_NAME].update_one(
        {"email": email}, {"$push": {"foods": {"$each": foods}}}
    )

    if result.matched_count == 0:
        raise fastapi.HTTPException(
            status_code=400, detail="no patient with email found"
        )

    return {
        "message": f"{result.modified_count} food(s) added",
        "data": {},
    }
