from fastapi import APIRouter, HTTPException
from loguru import logger

from poor_mans_terraform.models.api import (
    RelationalDbPayload,
    RelationalDbResponse,
)
from poor_mans_terraform.models.containers import RelationalDatabase
from poor_mans_terraform.services.docker_manager import create_container, get_client

router = APIRouter()


@router.post("", response_model=RelationalDbResponse, status_code=201)
async def create(
    payload: RelationalDbPayload, az: str | None = None
) -> RelationalDbResponse:
    """Run a container with provided database engine. If **az** is omitted your local machine is used to run the container."""
    try:
        client = get_client(az)
        database = RelationalDatabase(
            name=payload.name, environment=payload.environment, dbtype=payload.variant
        )
        container = create_container(
            client, database.resolve_image(), database.name, None, database.environment
        )
        merged = container | {"variant": database.variant, "az": az}
        database_response = RelationalDbResponse.model_validate(merged)
        logger.info(f"status: success, container_data: {database_response}")
        return database_response
    except ValueError as e:
        logger.exception(e)
        raise HTTPException(status_code=404, detail=str(e))
