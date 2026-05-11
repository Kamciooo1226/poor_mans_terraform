import uvicorn
from fastapi import FastAPI

from poor_mans_terraform.config.logger_conf import setup_logging
from poor_mans_terraform.routers import routers

setup_logging()

description = """
## Servers

Run docker containers with hardcoded distros and latest images.
 - Supported distros:
    - Ubuntu
    - Debian
    - Alipne
    - Rocky

## Databases

Run docker containers with a hardcoded list of supported database engines including:
   - Relational databases:
       - PostgreSQL
       - MySQL
   - NoSQL databases:
       - MongoDB
       - CockroachDB
   - Vector databases:
       - Qdrant
       - Chroma

## Availability Zones

These are just some random VMs running on your machine. If az value is omitted, the app will run containers on your local machine.

List all resources, stop containers and delete them. Have fun.
"""

app = FastAPI(
    title="Poor Mans Terraform",
    description=description,
    summary="Useless API to run Docker containers with extra steps and constraints!",
    version="1.0.0",
)

for router, prefix, tags in routers:
    app.include_router(router, prefix=prefix, tags=tags)


def main():
    uvicorn.run("poor_mans_terraform.main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    main()
