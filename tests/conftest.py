import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from src.database import Base, get_db
from src.main import app


@pytest_asyncio.fixture(autouse=True)
async def db_init():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async def get_test_db():
        async with AsyncSession(engine) as session:
            yield session

    app.dependency_overrides[get_db] = get_test_db


@pytest_asyncio.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as c:
        yield c
