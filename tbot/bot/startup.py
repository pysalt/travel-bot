import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from tbot.bot.resort_holiday_commands import router
from tbot.settings import settings


logger = logging.getLogger('bot')


dp = Dispatcher()
dp.include_router(router)


async def run_bot() -> None:
    bot = Bot(token=settings.bot.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await dp.start_polling(bot)
    logger.info('Bot started')
