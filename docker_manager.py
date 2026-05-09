import docker
from docker.errors import DockerException, NotFound

client = docker.from_env()


def create_container(image: str, name: str, command: str) -> str | None:
    container = client.containers.run(
        image=image, command=command, name=name, detach=True
    )
    return container.id


def get_container(id: str) -> dict:
    try:
        container = client.containers.get(id)
        return {
            "id": container.id,
            "image": container.attrs["Config"]["Image"],
            "name": container.name,
            "status": container.status,
        }
    except NotFound:
        raise ValueError(f"The server with provided id: {id} does not exist")


def stop_container(id: str) -> dict:
    try:
        container = client.containers.get(id)
        container.stop()
        container.reload()
        return {
            "id": container.id,
            "image": container.attrs["Config"]["Image"],
            "name": container.name,
            "status": container.status,
        }
    except NotFound:
        raise ValueError(f"The server with provided id: {id} does not exist")


def delete_container(id: str) -> str:
    try:
        container = client.containers.get(id)
        if container.status == "running":
            raise RuntimeError("cannot stop a running container")
        container.remove()
        return id
    except NotFound:
        raise ValueError(f"The server with provided id: {id} does not exist")
