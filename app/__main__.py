import asyncio
import sys

from .bot_init import aiogram_main
import logging

loop = asyncio.get_event_loop()
logging.basicConfig(level=logging.INFO, stream=sys.stdout)
loop.create_task(aiogram_main())
loop.run_forever()