import os
from typing import AsyncGenerator

import dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

dotenv.load_dotenv()

URI = os.getenv("URI")

engine = create_async_engine(URI, echo=True)

DeclarativeBase = declarative_base()

async_session = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    class_=AsyncSession,
    expire_on_commit=False
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Создает сессию подключения к БД

    :return: None
    """
    async_session = sessionmaker(
        engine,
        class_=AsyncSession,  # type: ignore
        expire_on_commit=False,
    )

    async with async_session() as session:
        yield session
        await session.close()


async def create_tables():
    """
    Создание таблиц на основе моделей

    :return: None
    """
    async with engine.begin() as conn:
        await conn.run_sync(DeclarativeBase.metadata.create_all)
