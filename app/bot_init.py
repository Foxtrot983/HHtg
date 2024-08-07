import logging

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from .state_storage import SqlAlchemyStorage
from .config import BOT_TOKEN
from .handlers import router

log = logging.getLogger(__name__)


async def aiogram_main():
    log.info("Bot start")
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=SqlAlchemyStorage())
    bot.parse_mode = ParseMode.HTML
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())