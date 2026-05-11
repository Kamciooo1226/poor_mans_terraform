# Poor Man's Terraform

A pet/learning project simulating basic cloud infrastructure management — think AWS EC2, RDS etc. - but running locally on KVM virtual machines with Docker.

Spin up VMs that simulate availability zones, then use the REST API to deploy containers across them.

Do keep in mind that this is completely useless for the most part - it's just running Docker containers with unnecessary extra steps and constaints.

---

## Prerequisites

- [Vagrant](https://www.vagrantup.com/) with [vagrant-libvirt](https://github.com/vagrant-libvirt/vagrant-libvirt) plugin
- KVM/libvirt installed on the host
- [uv](https://docs.astral.sh/uv/) for Python dependency management
- Python 3.13+

---

## Setup

### 1. Start the VMs

Three VMs simulating availability zones are defined in the `Vagrantfile`:

```
az-1 → 10.10.10.150
az-2 → 10.10.10.151
az-3 → 10.10.10.152
```

Start them with:

```sh
vagrant up
```

Each VM will automatically install Docker and expose the Docker API over TCP on port `2375` (no TLS!)

### 2. Configure availability zones

Edit `src/poor_mans_terraform/config/az_conf.toml` to match your VM IPs:

```toml
[availability_zones]
az-1 = "tcp://10.10.10.150:2375"
az-2 = "tcp://10.10.10.151:2375"
az-3 = "tcp://10.10.10.152:2375"
```

If no AZ is specified in a request, the API falls back to the local Docker host.

### 3. Install dependencies and run

```sh
uv sync
uv run poor_mans_terraform
```

The API will be available at `http://localhost:8000`.
Interactive docs at `http://localhost:8000/docs`.

---

## API Reference

All endpoints accept an optional `az` query parameter to target a specific availability zone. If omitted, the local Docker host is used.

### Servers

```sh
# Create a server (supported variants: ubuntu, debian, alpine, rockylinux)
curl -X POST "http://localhost:8000/resources/servers?az=az-1" \
  -H "Content-Type: application/json" \
  -d '{"name": "myserver", "variant": "ubuntu"}'
```

### Relational Databases

```sh
# Create a PostgreSQL database (supported variants: postgres, mysql)
curl -X POST "http://localhost:8000/resources/databases/relational?az=az-2" \
  -H "Content-Type: application/json" \
  -d '{"name": "mypostgres", "variant": "postgres", "environment": {"POSTGRES_PASSWORD": "admin"}}'
```

### NoSQL Databases

```sh
# Create a MongoDB instance (supported variants: mongo, cockroachdb)
curl -X POST "http://localhost:8000/resources/databases/nosql?az=az-2" \
  -H "Content-Type: application/json" \
  -d '{"name": "mymongo", "variant": "mongo", "environment": {"MONGO_INITDB_ROOT_USERNAME": "admin", "MONGO_INITDB_ROOT_PASSWORD": "admin"}}'
```

### Vector Databases

```sh
# Create a Qdrant instance (supported variants: qdrant, chromadb)
curl -X POST "http://localhost:8000/resources/databases/vector?az=az-3" \
  -H "Content-Type: application/json" \
  -d '{"name": "myqdrant", "variant": "qdrant", "environment": {}}'
```

### Container Operations

These endpoints work for any container regardless of type.

```sh
# List all containers on an AZ
curl "http://localhost:8000/resources/?az=az-1"

# Get a specific container
curl "http://localhost:8000/resources/{id}?az=az-1"

# Stop a container
curl -X PATCH "http://localhost:8000/resources/{id}?az=az-1"

# Delete a container (must be stopped first)
curl -X DELETE "http://localhost:8000/resources/{id}?az=az-1"
```
