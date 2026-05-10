import uvicorn
from fastapi import APIRouter, FastAPI, HTTPException
from loguru import logger

from poor_mans_terraform.logger_conf import setup_logging
from poor_mans_terraform.routers import containers

setup_logging()


app = FastAPI()
app.include_router(containers.router, prefix="/containers", tags=["containers"])


def main():
    uvicorn.run("poor_mans_terraform.main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    main()
