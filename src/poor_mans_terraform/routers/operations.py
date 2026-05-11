from typing import List

from fastapi import APIRouter, HTTPException
from loguru import logger

from poor_mans_terraform.models.api import ContainerResponse
from poor_mans_terraform.services.docker_manager import (
    delete_container,
    get_client,
    get_container,
    list_containers,
    stop_container,
)

router = APIRouter()


@router.get("/", response_model=List[ContainerResponse])
async def list(az: str | None = None) -> List[ContainerResponse]:
    """Lists all resources running on the provided Availability Zone. If **az** is omitted your local machine is used to list containers."""
    client = get_client(az)
    containers = list_containers(client, all_containers=True)
    containers_validated = [
        ContainerResponse.model_validate(c.attrs) for c in containers
    ]
    logger.info(f"status: success, containers data: {containers_validated}")
    return containers_validated


@router.get("/{id}", response_model=ContainerResponse)
async def get(id: str, az: str | None = None) -> ContainerResponse:
    """Get a specific container by ID. If **az** is omitted your local machine is used to lookup the container."""
    try:
        client = get_client(az)
        container = get_container(client, id)
        container_validated = ContainerResponse.model_validate(container)
        logger.info(f"status: success, container_data: {container_validated}")
        return container_validated
    except ValueError as e:
        logger.exception(e)
        raise HTTPException(status_code=404, detail=str(e))


@router.patch("/{id}", response_model=ContainerResponse)
async def stop(id: str, az: str | None = None) -> ContainerResponse:
    """Stop a specific container by ID. If **az** is omitted your local machine is used to stop the container."""
    try:
        client = get_client(az)
        container = stop_container(client, id)
        container_validated = ContainerResponse.model_validate(container)
        logger.info(f"status: success, container_data: {container_validated}")
        return container_validated
    except ValueError as e:
        logger.exception(e)
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{id}", status_code=204)
async def delete(id: str, az: str | None = None) -> None:
    """Remove a specific container by ID. If **az** is omitted your local machine is used to remove the container."""
    try:
        client = get_client(az)
        delete_container(client, id)
        logger.info(f"status: success, deleted: {id}")
    except ValueError as e:
        logger.exception(e)
        raise HTTPException(status_code=404, detail=str(e))
    except RuntimeError as e:
        logger.exception(e)
        raise HTTPException(status_code=400, detail=str(e))
