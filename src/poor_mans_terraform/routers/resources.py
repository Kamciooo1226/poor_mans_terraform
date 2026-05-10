from typing import List

from fastapi import APIRouter, HTTPException
from loguru import logger

from poor_mans_terraform.models.api import ContainerResponse, ServerPayload
from poor_mans_terraform.services.docker_manager import (
    create_container,
    delete_container,
    get_container,
    list_containers,
    stop_container,
)

router = APIRouter()


@router.get("/", response_model=List[ContainerResponse])
async def root() -> List[ContainerResponse]:
    containers = list_containers(all_containers=True)
    containers_validated = [
        ContainerResponse.model_validate(c.attrs) for c in containers
    ]
    logger.info(f"status: success, containers data: {containers_validated}")
    return containers_validated


@router.post("/create", response_model=ContainerResponse, status_code=201)
async def create(payload: ServerPayload) -> ContainerResponse:
    try:
        container = create_container(payload.image, payload.name, payload.command)
        container_validated = ContainerResponse.model_validate(container)
        logger.info(f"status: success, container_data: {container_validated}")
        return container_validated
    except ValueError as e:
        logger.exception(e)
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{id}", response_model=ContainerResponse)
async def get(id: str) -> ContainerResponse:
    try:
        container = get_container(id)
        container_validated = ContainerResponse.model_validate(container)
        logger.info(f"status: success, container_data: {container_validated}")
        return container_validated
    except ValueError as e:
        logger.exception(e)
        raise HTTPException(status_code=404, detail=str(e))


@router.patch("/{id}", response_model=ContainerResponse)
async def stop(id: str) -> ContainerResponse:
    try:
        container = stop_container(id)
        container_validated = ContainerResponse.model_validate(container)
        logger.info(f"status: success, container_data: {container_validated}")
        return container_validated
    except ValueError as e:
        logger.exception(e)
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{id}", status_code=204)
async def delete(id: str) -> None:
    try:
        delete_container(id)
        logger.info(f"status: success, deleted: {id}")
    except ValueError as e:
        logger.exception(e)
        raise HTTPException(status_code=404, detail=str(e))
    except RuntimeError as e:
        logger.exception(e)
        raise HTTPException(status_code=400, detail=str(e))
