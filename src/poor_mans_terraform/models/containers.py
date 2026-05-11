from enum import Enum


class Container:
    def __init__(self, name: str, variant: Enum):
        self.name = name
        self.variant = variant

    def resolve_image(self) -> str:
        return self.variant.value


class Distro(Enum):
    """Hardcoded latest images for simplicity."""

    UBUNTU = "ubuntu"
    DEBIAN = "debian"
    ALPINE = "alpine"
    ROCKY = "rockylinux"


class RelationalDB(Enum):
    """Hardcoded latest images for simplicity."""

    POSTGRESQL = "postgres"
    MYSQL = "mysql"


class NoSQLDB(Enum):
    """Hardcoded latest images for simplicity."""

    MONGO = "mongo"
    COCKROACH = "cockroachdb/cockroach"


class VectorDB(Enum):
    QDRANT = "qdrant/qdrant"
    CHROMA = "chromadb/chroma"


class Server(Container):
    def __init__(self, name: str, distro: Distro):
        super().__init__(name, variant=distro)
        self.command = "tail -f /dev/null"


class RelationalDatabase(Container):
    def __init__(self, name: str, environment: dict, dbtype: RelationalDB):
        super().__init__(name, variant=dbtype)
        self.environment = environment


class NoSQLDatabase(Container):
    def __init__(self, name: str, environment: dict, dbtype: NoSQLDB):
        super().__init__(name, variant=dbtype)
        self.environment = environment


class VectorDatabase(Container):
    def __init__(self, name: str, environment: dict, dbtype: VectorDB):
        super().__init__(name, variant=dbtype)
        self.environment = environment
