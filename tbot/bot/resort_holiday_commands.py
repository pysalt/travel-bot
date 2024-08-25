from aiogram import html, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from tbot.services.resort_holiday import ResortHolidayClient
from tbot.settings import settings


router = Router(name='holiday_resort_router')
resort_client = ResortHolidayClient(base_url=settings.resort_holiday.url)


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")


@router.message(Command('currency_today'))
async def get_current_currency(message: Message) -> None:
    """
    Return last currency from Holiday Resort API
    """
    currencies = await resort_client.get_current_currency()

    answer = 'Текущий курс валют у Resort Holiday:\n\n'
    for currency in currencies:
        answer += f'{currency.currencyISO}: {currency.rate}\n'

    await message.answer(answer)
