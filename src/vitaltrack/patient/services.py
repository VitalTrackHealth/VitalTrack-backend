"""
Patient business logic
"""

from __future__ import annotations

import uuid
from typing import Any

from pymongo import ReturnDocument

from vitaltrack import config
from vitaltrack import core
from vitaltrack import provider
from . import models
from . import schemas


async def register_patient(
    db_manager: core.database.DatabaseManager,
    patient: schemas.PatientRegisterRequest,
) -> models.PatientInDB | None:
    # Ensure username and email are the same
    if patient.username != patient.email:
        raise ValueError("Username and email must be the same")

    patients_collection = await db_manager.get_collection(
        config.PATIENTS_COLLECTION_NAME
    )

    existing_patient = await patients_collection.find_one(
        {"username": patient.username}
    )
    if existing_patient:
        raise ValueError("Patient with this email already exists")

    # Generate patient password hash
    salt = core.utils.generate_salt()
    password_hash = core.utils.get_password_hash(
        patient.password.encode("utf-8"),
        salt,
    )

    provider_in_db = None
    if patient.provider_code:
        provider_in_db = await provider.services.get_provider(
            db_manager, {"provider_code": patient.provider_code}
        )

    new_patient = models.PatientInDB(
        id=uuid.uuid4(),
        password_hash=password_hash,
        salt=salt,
        disabled=False,
        providers=[provider_in_db.id] if provider_in_db else [],
        **patient.model_dump(exclude={"password", "provider_code"}),
    )
    result = await patients_collection.insert_one(new_patient.model_dump(by_alias=True))

    if provider_in_db:
        await db_manager.db[config.PROVIDERS_COLLECTION_NAME].update_one(
            {"_id": provider_in_db.id}, {"$addToSet": {"patients": new_patient.id}}
        )

    if result.inserted_id:
        return new_patient


async def get_patient(
    db_manager: core.database.DatabaseManager,
    filter: dict[str, Any],
) -> models.PatientInDB | None:
    patients_collection = await db_manager.get_collection(
        config.PATIENTS_COLLECTION_NAME
    )
    existing_patient = await patients_collection.find_one(filter)
    if existing_patient:
        return models.PatientInDB(**existing_patient)


async def update_patient(
    db_manager: core.database.DatabaseManager,
    filter: dict[str, Any],
    patient_update: schemas.PatientUpdateRequest,
) -> models.PatientInDB | None:
    # TODO: Update password correctly
    # TODO: Update provider correctly
    patients_collection = await db_manager.get_collection(
        config.PATIENTS_COLLECTION_NAME
    )

    patient_update_dict = patient_update.model_dump(
        exclude_unset=True, exclude_none=True
    )
    result = await patients_collection.find_one_and_update(
        filter, {"$set": patient_update_dict}, return_document=ReturnDocument.AFTER
    )
    if result:
        return models.PatientInDB(**result)


async def add_provider_to_patient(
    db_manager: core.database.DatabaseManager,
    patient_id: uuid.UUID,
    provider_id: uuid.UUID,
) -> models.PatientInDB | None:
    patients_collection = await db_manager.get_collection(
        config.PATIENTS_COLLECTION_NAME
    )

    result = await patients_collection.find_one_and_update(
        {"_id": patient_id},
        {"$addToSet": {"providers": provider_id}},
        return_document=ReturnDocument.AFTER,
    )

    # Add Provider relationship
    provider_in_db = await provider.services.get_provider(
        db_manager, {"_id": provider_id}
    )

    if provider_in_db:
        await db_manager.db[config.PROVIDERS_COLLECTION_NAME].update_one(
            {"_id": provider_in_db.id}, {"$addToSet": {"patients": patient_id}}
        )

    return models.PatientInDB(**result)
