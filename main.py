from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from docker_manager import (
    create_container,
    delete_container,
    get_container,
    stop_container,
)


class ServerPayload(BaseModel):
    image: str
    name: str
    command: str


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "hello"}


@app.post("/servers/create")
async def create(payload: ServerPayload) -> dict:
    container_id = create_container(payload.image, payload.name, payload.command)
    return {"status": "success", "container_id": container_id}


@app.get("/servers/list/{id}")
async def get(id: str) -> dict:
    try:
        container_data = get_container(id)
        return {"status": "success", "server_info": container_data}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.patch("/servers/update/{id}")
async def stop(id: str) -> dict:
    try:
        container_data = stop_container(id)
        return {"status": "success", "server_info": container_data}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.delete("/servers/delete/{id}")
async def delete(id: str) -> dict:
    try:
        container_delete = delete_container(id)
        return {"status": "success", "deleted": container_delete}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))


def main():
    ()


if __name__ == "__main__":
    main()
