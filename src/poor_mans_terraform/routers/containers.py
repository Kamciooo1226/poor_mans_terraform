from typing import List

from fastapi import APIRouter, HTTPException
from loguru import logger

from poor_mans_terraform.models import ContainerResponse, ServerPayload
from poor_mans_terraform.services.docker_manager import (
    create_container,
    delete_container,
    get_container,
    list_containers,
    stop_container,
)

router = APIRouter()


@router.get("/", response_model=List[ContainerResponse])
async def root():
    containers = list_containers(all_containers=True)
    return [c.attrs for c in containers]


@router.post("/create")
async def create(payload: ServerPayload) -> dict:
    try:
        container_id = create_container(payload.image, payload.name, payload.command)
        logger.info(f"status: success, container_id: {container_id}")
        return {"status": "success", "container_id": container_id}
    except ValueError as e:
        logger.exception(e)
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{id}")
async def get(id: str) -> dict:
    try:
        container_data = get_container(id)
        logger.info(f"status: success, container_info: {container_data}")
        return {"status": "success", "container_info": container_data}
    except ValueError as e:
        logger.exception(e)
        raise HTTPException(status_code=404, detail=str(e))


@router.patch("/{id}")
async def stop(id: str) -> dict:
    try:
        container_data = stop_container(id)
        logger.info(f"status: success, container_info: {container_data}")
        return {"status": "success", "container_info": container_data}
    except ValueError as e:
        logger.exception(e)
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{id}")
async def delete(id: str) -> dict:
    try:
        container_data = delete_container(id)
        logger.info(f"status: success, deleted: {container_data}")
        return {"status": "success", "deleted": container_data}
    except ValueError as e:
        logger.exception(e)
        raise HTTPException(status_code=404, detail=str(e))
    except RuntimeError as e:
        logger.exception(e)
        raise HTTPException(status_code=400, detail=str(e))
