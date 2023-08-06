# pylint: skip-file
from sqlalchemy.ext.asyncio import AsyncSession

from .connectionmanager import connections
from .connection import Connection
from .connectionmanager import ConnectionManager
from .declarative import declarative_base
from .repository import Repository


__all__ = [
    'Connection',
    'ConnectionManager',
    'Repository',
    'add',
    'connect',
    'declarative_base',
    'disconnect',
    'get',
    'session',
    'setup_databases',
]


def add(name: str, **opts) -> None:
    """Add a new connection using the given parameters"""
    connections.add(name, opts)


async def connect(*args, **kwargs) -> None:
    """Connect all database connections that are specified in the default
    connection manager.
    """
    return await connections.connect(*args, **kwargs)


async def disconnect() -> None:
    """Disconnect all database connections that are specified in the default
    connection manager.
    """
    return await connections.disconnect()


def get(name: str) -> Connection:
    """Return the named connection `name`."""
    return connections.get(name)


def session(self, name: str) -> AsyncSession:
    """Create a new :class:`sqlalchemy.ext.asyncio.AsyncSession`
    instance for the named connection `name`.
    """
    connection = get(name)
    if not connection.is_connected():
        raise RuntimeError(f"Connection '{name}' is not established.")
    return connection.get_session()
