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
    current_patient: dependencies.patient_authenticate_dep,
    request: schemas.PatientAddFoodRequest,
    db_manager: core.dependencies.database_manager_dep,
):
    patient_in_db = await services.get_patient(
        db_manager, {"username": current_patient.username}
    )
    foods_to_insert = [
        food.models.FoodInDB(
            food_id=food_to_insert.food_id,
            food_name=food_to_insert.food_name,
            patient_id=patient_in_db.id,
            details=food_to_insert.details,
        ).model_dump()
        for food_to_insert in request.foods
    ]

    result = await db_manager.db[config.FOOD_COLLECTION_NAME].insert_many(
        foods_to_insert
    )

    return {
        "message": f"{len(result.inserted_ids)} food(s) added",
        "data": {"inserted_ids": [str(id) for id in result.inserted_ids]},
    }


@router.get("/food-log", response_model=schemas.PatientFoodLogResponse)
async def food_log(
    current_patient: dependencies.patient_authenticate_dep,
    db_manager: core.dependencies.database_manager_dep,
):
    patient_in_db = await services.get_patient(
        db_manager, {"username": current_patient.username}
    )

    food_log = await food.services.get_food_log(
        db_manager, {"patient_id": patient_in_db.id}
    )
    if not food_log:
        food_log = []

    return {"data": food_log}
