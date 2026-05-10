import docker
from docker.errors import APIError, ImageNotFound, NotFound

client = docker.from_env()


def create_container(image: str, name: str, command: str | list[str]) -> dict:
    try:
        container = client.containers.run(
            image=image, command=command, name=name, detach=True
        )
        return container.attrs
    except ImageNotFound:
        raise ValueError(f"Image {image} not found")
    except APIError as e:
        if e.response is not None and e.response.status_code == 409:
            raise ValueError(f"The container with provided name {name} already exist")
        raise


def list_containers(all_containers: bool = True) -> list:
    containers = client.containers.list(all=all_containers)
    return containers


def get_container(id: str) -> dict:
    try:
        container = client.containers.get(id)
        return container.attrs
    except NotFound:
        raise ValueError(f"The server with provided id: {id} does not exist")


def stop_container(id: str) -> dict:
    try:
        container = client.containers.get(id)
        container.stop()
        container.reload()
        return container.attrs
    except NotFound:
        raise ValueError(f"The server with provided id: {id} does not exist")


def delete_container(id: str) -> None:
    try:
        container = client.containers.get(id)
        if container.status == "running":
            raise RuntimeError("cannot remove a running container")
        container.remove()
    except NotFound:
        raise ValueError(f"The server with provided id: {id} does not exist")
