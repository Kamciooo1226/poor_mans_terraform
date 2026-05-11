from fastapi import APIRouter, HTTPException
from loguru import logger

from poor_mans_terraform.models.api import (
    ServerPayload,
    ServerResponse,
)
from poor_mans_terraform.models.containers import Distro, Server
from poor_mans_terraform.services.docker_manager import create_container, get_client

router = APIRouter()


@router.post("", response_model=ServerResponse, status_code=201)
async def create(payload: ServerPayload, az: str | None = None) -> ServerResponse:
    """Run a container with provided distro. If **az** is omitted your local machine is used to run the container."""
    try:
        client = get_client(az)
        server = Server(name=payload.name, distro=Distro(payload.variant))
        container = create_container(
            client, server.resolve_image(), server.name, server.command
        )
        merged = container | {"variant": server.variant, "az": az}
        server_response = ServerResponse.model_validate(merged)
        logger.info(f"status: success, container_data: {server_response}")
        return server_response
    except ValueError as e:
        logger.exception(e)
        raise HTTPException(status_code=404, detail=str(e))
