from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
from .models import Donation, Base
from datetime import datetime

DATABASE_URL = "sqlite+aiosqlite:///./donations.db"



engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def add_donation(user_id: int, amount: float, currency: str):
    async with async_session() as session:
        donation = Donation(user_id=user_id, amount=amount, currency=currency, timestamp=datetime.utcnow())
        session.add(donation)
        await session.commit()

async def get_total_donations(currency: str):
    async with async_session() as session:
        result = await session.execute(select(Donation).filter_by(currency=currency))
        donations = result.scalars().all()
        return sum(donation.amount for donation in donations)

async def get_donations_report():
    async with async_session() as session:
        result = await session.execute(select(Donation))
        donations = result.scalars().all()
        return donations

async def get_total_donations_by_currency():
    totals = {}
    currencies = ["USD", "EUR", "RUB", "UAH"]  # Список валют

    async with async_session() as session:
        for currency in currencies:
            result = await session.execute(select(Donation).filter_by(currency=currency))
            donations = result.scalars().all()
            totals[currency] = sum(donation.amount for donation in donations)

    return totals
