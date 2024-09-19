from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import Dispatcher
from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types.base import TelegramObject
from apscheduler.schedulers.asyncio import AsyncIOScheduler



def register_all_middlewares(dp: Dispatcher, scheduler):
    dp.update.outer_middleware(SchedulerMiddleware(scheduler))


class SchedulerMiddleware(BaseMiddleware):
    def __init__(self, scheduler: AsyncIOScheduler):
        self._scheduler = scheduler

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ):
        data['scheduler'] = self._scheduler
        return await handler(event, data)
