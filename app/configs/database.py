import asyncio
import time
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import OperationalError
from app.configs.config import settings

DATABASE_URL = f"mysql+asyncmy://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}/{settings.DB_NAME}"

engine = create_async_engine(DATABASE_URL, echo=False, future=True)
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()


async def test_connection():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(lambda _: None)
        print("Database connection successful.")
    except OperationalError as e:
        print(f"Database connection failed: {e}")


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("All database tables created successfully.")


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
