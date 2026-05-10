from typing import Any, Optional

from pydantic import AliasPath, BaseModel, Field
from pydantic.functional_validators import field_validator


class ServerPayload(BaseModel):
    image: str
    name: str
    command: str | list[str]
    auto_remove: bool

    @field_validator("command")
    @classmethod
    def ensure_list(cls, v: str | list[str]) -> list[str]:
        if isinstance(v, str):
            return v.split()
        return v

    @field_validator("name")
    @classmethod
    def strip_lslash(cls, v: str) -> str:
        """Ensure no leading slash is present."""
        return v.lstrip("/")


class ContainerResponse(BaseModel):
    id: str = Field(validation_alias="Id")
    image: str = Field(validation_alias=AliasPath("Config", "Image"))
    name: str = Field(validation_alias="Name")
    status: str = Field(validation_alias=AliasPath("State", "Status"))

    class Config:
        from_attributes = True
