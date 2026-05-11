from enum import Enum

from fastapi import APIRouter

from poor_mans_terraform.routers import operations
from poor_mans_terraform.routers.databases import nosql, relational, vector
from poor_mans_terraform.routers.servers import servers

routers: list[tuple[APIRouter, str, list[str | Enum]]] = [
    (servers.router, "/resources/servers", ["servers"]),
    (relational.router, "/resources/databases/relational", ["databases"]),
    (nosql.router, "/resources/databases/nosql", ["databases"]),
    (vector.router, "/resources/databases/vector", ["databases"]),
    (operations.router, "/resources", ["containers"]),
]
