"""This package implements the tentaclio athena client """
from tentaclio import *  # noqa

from .clients.athena_client import AthenaClient


# Add DB registry
DB_REGISTRY.register("awsathena+rest", AthenaClient)  # type: ignore
