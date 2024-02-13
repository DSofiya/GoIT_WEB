import contextlib

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from src.conf.config import config


class DatabaseSessionManager:
    def __init__(self, url: str):
        self._engine: AsyncEngine | None = create_async_engine(url)
        self._session_maker: async_sessionmaker | None = async_sessionmaker(
            autocommit=False, autoflush=False, bind=self._engine
        )

    @contextlib.asynccontextmanager
    async def session(self):
        """
        The session function is a context manager that provides a transactional scope around a series of operations.
            It will automatically rollback the session if an exception occurs, or commit otherwise.
            
        
        :param self: Represent the instance of the class
        :return: A coroutine
        :doc-author: Trelent
        """
        if self._session_maker is None:
            raise Exception("Session is not initialized")
        session = self._session_maker()
        try:
            yield session
        except Exception as err:
            print(err)
            await session.rollback()
        finally:
            await session.close()


sessionmanager = DatabaseSessionManager(config.DB_URL)


async def get_db():
    """
    The get_db function is a coroutine that returns an async context manager.
    The context manager yields a database session, which can be used to query the database.
    When the block of code exits, the session is automatically closed.
    
    :return: A context manager that yields a database session
    :doc-author: Trelent
    """
    async with sessionmanager.session() as session:
        yield session
