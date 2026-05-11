import tomllib
from pathlib import Path
from tomllib import TOMLDecodeError

import docker
from docker.client import DockerClient
from docker.errors import APIError, ImageNotFound, NotFound
from loguru import logger

CONFIG_PATH = Path(__file__).parent.parent / "config" / "az_conf.toml"

try:
    with open(CONFIG_PATH, "rb") as config:
        AZ_CONFIG = tomllib.load(config)
        AZ_CLIENTS = {
            key: DockerClient(value)
            for key, value in AZ_CONFIG["availability_zones"].items()
        }
except (FileNotFoundError, TOMLDecodeError, KeyError) as e:
    if isinstance(e, FileNotFoundError):
        logger.error(f"Configuration file: {CONFIG_PATH} could not be found.")
    elif isinstance(e, TOMLDecodeError):
        logger.error(f"Parsing error while reading configuration file: {CONFIG_PATH}")
    elif isinstance(e, KeyError):
        logger.error(
            f"availability_zones key cound not be found while reading configuration file: {CONFIG_PATH}"
        )
    AZ_CLIENTS = {}


def get_client(az: str | None = None) -> DockerClient:
    """Look up AZ values to create a DockerClient. If az argument is not provided, or specified value is not found it falls back to host DockerClient for simplicity.
    In order to use AZs one would need to create VMs (Vagrantfile provided for ease of use)."""

    client = AZ_CLIENTS.get(az)
    if client is None:
        logger.error(
            f"The specified AZ '{az}' was not found, falling back to the host DockerClient"
        )
        return docker.from_env()
    return client


def create_container(
    client: DockerClient,
    image: str,
    name: str,
    command: str | list[str] | None = None,
    environment: dict | None = None,
) -> dict:
    """Create a container on the DockerClient:
    - Server class containers need a command to run in the container, otherwise they'd exit. The command is hardcoded within the class for simplicity.
    - Database class containers need environment provided with user/pass, depending on the db type and engine.
    """
    try:
        container = client.containers.run(
            image=image,
            command=command,
            name=name,
            detach=True,
            environment=environment,
        )
        return container.attrs
    except ImageNotFound:
        raise ValueError(f"Image {image} not found")
    except APIError as e:
        if e.response is not None and e.response.status_code == 409:
            raise ValueError(f"The container with provided name {name} already exist")
        raise


def list_containers(client: DockerClient, all_containers: bool = True) -> list:
    containers = client.containers.list(all=all_containers)
    return containers


def get_container(client: DockerClient, id: str) -> dict:
    try:
        container = client.containers.get(id)
        return container.attrs
    except NotFound:
        raise ValueError(f"The container with provided id: {id} does not exist")


def stop_container(client: DockerClient, id: str) -> dict:
    try:
        container = client.containers.get(id)
        container.stop()
        container.reload()
        return container.attrs
    except NotFound:
        raise ValueError(f"The container with provided id: {id} does not exist")


def delete_container(client: DockerClient, id: str) -> None:
    try:
        container = client.containers.get(id)
        if container.status == "running":
            raise RuntimeError("Cannot remove a running container")
        container.remove()
    except NotFound:
        raise ValueError(f"The container with provided id: {id} does not exist")
