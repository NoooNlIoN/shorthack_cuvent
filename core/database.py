from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    AsyncEngine,
    create_async_engine,
    async_sessionmaker,
)

from core.config import settings
from core.table import Base


class DatabaseSessionManager:
    def __init__(self):
        self.engine: AsyncEngine | None = None
        self.session_maker: async_sessionmaker[AsyncSession] | None = None

    def init(self, database_url: str):
        self.engine = create_async_engine(
            database_url,
            echo=settings.debug,
            pool_size=20,
            max_overflow=10,
            pool_pre_ping=True,
        )
        self.session_maker = async_sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autoflush=False,
            autocommit=False,
        )

    async def close(self):
        if self.engine is None:
            return
        await self.engine.dispose()
        self.engine = None
        self.session_maker = None

    async def create_all(self):
        if self.engine is None:
            raise Exception("DatabaseSessionManager is not initialized")
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def drop_all(self):
        if self.engine is None:
            raise Exception("DatabaseSessionManager is not initialized")
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)


sessionmanager = DatabaseSessionManager()
sessionmanager.init(settings.database_url)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    if sessionmanager.session_maker is None:
        raise Exception("DatabaseSessionManager is not initialized")
    async with sessionmanager.session_maker() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

