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
    COCKROACH = "cockroachdb"


class VectorDB(Enum):
    """Hardcoded latest images for simplicity."""

    QDRANT = "qdrant"
    CHROMA = "chromadb"


class Server(Container):
    def __init__(self, name: str, distro: Distro):
        super().__init__(name, variant=distro)


class RelationalDatabase(Container):
    def __init__(self, name: str, env: dict, dbtype: RelationalDB):
        super().__init__(name, variant=dbtype)
        self.env = env


class NoSQLDatabase(Container):
    def __init__(self, name: str, dbtype: NoSQLDB):
        super().__init__(name, variant=dbtype)


class VectorDatabase(Container):
    def __init__(self, name: str, dbtype: VectorDB):
        super().__init__(name, variant=dbtype)
