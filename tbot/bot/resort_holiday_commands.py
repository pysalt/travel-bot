from aiogram import html, Router, Bot
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from apscheduler.jobstores.base import JobLookupError
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from tbot.services.resort_holiday import ResortHolidayClient
from tbot.services.scheduler import generate_job_id
from tbot.settings import settings


router = Router(name='holiday_resort_router')
resort_client = ResortHolidayClient(base_url=settings.resort_holiday.url)


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    await message.answer(f'Hello, {html.bold(message.from_user.full_name)}!')


@router.message(Command('currency_today'))
async def get_current_currency(message: Message) -> None:
    """
    Return last currency from Holiday Resort API
    """
    await _send_currency_message(bot=message.bot, chat_id=message.chat.id)


@router.message(Command('currency_subscribe'))
async def subscribe_on_currency(message: Message, scheduler: AsyncIOScheduler) -> None:
    """
    Subscribe on last currency notifications from Holiday Resort API
    """
    scheduler.add_job(
        _send_currency_message,
        kwargs={'bot': message.bot, 'chat_id': message.chat.id},
        trigger=CronTrigger.from_crontab('1 10 * * *'),  # Every day at 10:01 a.m.
        id=_get_job_id_for_user(message.chat.id),
    )

    await message.answer('Вы подписались на курс валют')


@router.message(Command('currency_unsubscribe'))
async def unsubscribe_from_currency(
    message: Message, scheduler: AsyncIOScheduler
) -> None:
    """
    Unsubscribe from last currency notifications from Holiday Resort API
    """
    try:
        scheduler.remove_job(job_id=_get_job_id_for_user(message.chat.id))
    except JobLookupError:
        await message.answer('Вы не подписаны на курс валют')

    await message.answer('Вы успешно отписались')


async def _send_currency_message(bot: Bot, chat_id: int) -> None:
    currencies = await resort_client.get_current_currency()

    answer = 'Текущий курс валют у Resort Holiday:\n\n'
    for currency in currencies:
        answer += f'{currency.currencyISO}: {currency.rate}\n'

    await bot.send_message(chat_id, answer)


def _get_job_id_for_user(chat_id: int):
    return generate_job_id(key=str(chat_id))
