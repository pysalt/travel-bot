import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from tbot.bot.middleware import register_all_middlewares
from tbot.bot.resort_holiday_commands import router
from tbot.services.storage import get_storage
from tbot.settings import settings


logger = logging.getLogger('bot')


async def run_bot() -> None:
    storage = get_storage(
        host=settings.mongo.host,
        port=settings.mongo.port,
        username=settings.mongo.username,
        password=settings.mongo.password,
    )
    scheduler = AsyncIOScheduler()

    bot = Bot(token=settings.bot.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    dp = Dispatcher(storage=storage)
    dp.include_router(router)
    register_all_middlewares(dp, scheduler)

    try:
        scheduler.start()
        logger.info('Bot starting')
        await dp.start_polling(bot)
    finally:
        await dp.storage.close()
        await bot.session.close()
