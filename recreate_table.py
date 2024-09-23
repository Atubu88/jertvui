import asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from database.models import Base, Donation

DATABASE_URL = "sqlite+aiosqlite:///./donations.db"

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def recreate_table():
    # Удаляем таблицу
    async with engine.begin() as conn:
        print("Удаляем таблицу donations...")
        await conn.run_sync(Base.metadata.drop_all)

    # Создаем таблицу заново с новыми полями
    async with engine.begin() as conn:
        print("Создаем таблицу donations заново...")
        await conn.run_sync(Base.metadata.create_all)

    print("Таблица donations была пересоздана.")

# Запуск асинхронной функции
if __name__ == "__main__":
    asyncio.run(recreate_table())
