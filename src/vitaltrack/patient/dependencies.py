"""
Patient dependencies
"""

from typing import Annotated

import fastapi

from vitaltrack import core
from vitaltrack import config

from . import models


async def get_current_patient(
    token_data: core.dependencies.authenticate_dep,
    db_manager: core.dependencies.database_manager_dep,
) -> models.PatientInDB:
    patients_collection = await db_manager.get_collection(
        config.PATIENTS_COLLECTION_NAME
    )
    patient = await patients_collection.find_one({"username": token_data.username})

    if patient is None:
        raise core.exceptions.TokenValidationError()

    # Check if patient is disabled
    if patient.get("disabled"):
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_400_BAD_REQUEST, detail="Inactive entity"
        )

    return models.PatientInDB(**patient)


patient_authenticate_dep = Annotated[
    models.PatientInDB, fastapi.Depends(get_current_patient)
]
