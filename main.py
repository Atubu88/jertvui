import asyncio
from aiogram import Bot, Dispatcher
from config import API_TOKEN
from handlers import start, donate, info, report
from database.db import init_db


async def main():
    await init_db()

    bot = Bot(token=API_TOKEN)
    dp = Dispatcher()

    dp.include_router(start.router)
    dp.include_router(donate.router)
    dp.include_router(info.router)
    dp.include_router(report.router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
