from aiogram import Bot, Dispatcher
from config import TOKEN
from handlers import router
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from middlewares import SchedulerMiddleware
import asyncio



bot = Bot(TOKEN)
disp = Dispatcher()

async def main():
    disp.include_router(router)
    scheduler = AsyncIOScheduler()
    disp.update.middleware(SchedulerMiddleware(scheduler))
    scheduler.start()
    await disp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())