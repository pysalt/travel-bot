import asyncio
import logging
import sys

from tbot.bot.startup import run_bot

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
asyncio.run(run_bot())
