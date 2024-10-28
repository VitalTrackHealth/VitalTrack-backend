"""
Global models interactions with MongoDB.

'InDB' is add to class names to add more distinction from schemas.
"""

import pydantic
import uuid

from . import utils


class ModelInDBBase(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(populate_by_name=True)


class AuthenticatedEntity(pydantic.BaseModel):
    id: uuid.UUID = pydantic.Field(alias="_id")
    username: str = pydantic.Field(...)
    salt: bytes = pydantic.Field(...)
    password_hash: bytes = pydantic.Field(...)

    def check_password(self, password: str):
        return utils.verify_password(password.encode("utf-8"), self.password_hash)

    def change_password(self, password: str):
        self.salt = utils.generate_salt()
        self.password_hash = utils.get_password_hash(self.salt, password)
