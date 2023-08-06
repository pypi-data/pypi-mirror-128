"""Declares :class:`Repository`."""
import sqlalchemy
from sqlalchemy.ext.asyncio import AsyncSession

from .connection import Connection
from .connectionmanager import connections


class Repository:
    """A repository implementation that uses a relational database as its
    storage backend.
    """
    db_alias: str = 'self'

    @property
    def session(self) -> AsyncSession:
        """Return the session that wraps the current transaction."""
        assert self.__session is not None # nosec
        return self.__session

    def new(self, **kwargs):
        """Return  a new :class:`Repository` instance."""
        return type(self)(
            *self.__initargs,
            **{**self.__initkwargs, **kwargs}
        )

    def __init__(self, session=None, *args, **kwargs):
        self.__session = session
        self.__transaction = None
        self.__initargs = args
        self.__initkwargs = kwargs
        self._setup(*args, **kwargs)

    def _setup(self, db_alias: str = 'self', *args, **kwargs):
        self.db_alias = db_alias
        self.setup(db_alias=db_alias, *args, **kwargs)

    def setup(self, db_alias: str = 'self', *args, **kwargs):
        """Hook that is called during instance initialization."""
        pass

    @property
    def connection(self) -> Connection:
        """Return the default database connection as specified by
        :attr:`db_alias`.
        """
        return connections.get(self.db_alias)

    def atomic(self):
        """Ensures that the statements executed within the context
        block are included in a single transaction.
        """
        return self.new(session=self.get_session())

    async def execute(self, query, *args, **kwargs):
        if isinstance(query, str):
            query = sqlalchemy.text(query)
        return await self.__session.execute(query, *args, **kwargs)

    def get_session(self, *args, **kwargs):
        """Return a :class:`sqlalchemy.ext.asyncio.AsyncSession`
        instance configured with the default database connection.
        """
        return self.connection.get_session(*args, **kwargs)

    async def __aenter__(self):
        assert self.__transaction is None # nosec
        self.__transaction = await self.__session.begin()
        return self

    async def __aexit__(self, cls, exception, traceback):
        if self.__transaction is not None:
            await self.__transaction.commit()\
                if exception is None else\
                await self.__transaction.rollback()
        await self.__session.close()
