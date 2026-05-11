from pydantic import AliasPath, BaseModel, Field
from pydantic.functional_validators import field_validator

from poor_mans_terraform.models.containers import (
    Distro,
    NoSQLDB,
    RelationalDB,
    VectorDB,
)


class ServerPayload(BaseModel):
    name: str
    variant: Distro

    @field_validator("name")
    @classmethod
    def strip_lslash(cls, v: str) -> str:
        """Ensure no leading slash is present."""
        return v.lstrip("/")


class DatabasePayload(BaseModel):
    name: str
    environment: dict

    @field_validator("name")
    @classmethod
    def strip_lslash(cls, v: str) -> str:
        """Ensure no leading slash is present."""
        return v.lstrip("/")


class RelationalDbPayload(DatabasePayload):
    variant: RelationalDB


class NoSQLDbPayload(DatabasePayload):
    variant: NoSQLDB


class VectorDbPayload(DatabasePayload):
    variant: VectorDB


class ContainerResponse(BaseModel):
    id: str = Field(validation_alias="Id")
    image: str = Field(validation_alias=AliasPath("Config", "Image"))
    name: str = Field(validation_alias="Name")
    status: str = Field(validation_alias=AliasPath("State", "Status"))

    @field_validator("name")
    @classmethod
    def strip_lslash(cls, v: str) -> str:
        """Ensure no leading slash is present."""
        return v.lstrip("/")

    class Config:
        from_attributes = True


class ServerResponse(ContainerResponse):
    variant: Distro
    az: str | None


class RelationalDbResponse(ContainerResponse):
    variant: RelationalDB
    az: str | None


class NoSQLDbResponse(ContainerResponse):
    variant: NoSQLDB
    az: str | None


class VectorDbResponse(ContainerResponse):
    variant: VectorDB
    az: str | None
