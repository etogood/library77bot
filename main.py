import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from config_reader import config
from handlers import basic_router, club_application_router

bot = Bot(token=config.bot_token.get_secret_value(), parse_mode=ParseMode.HTML)

async def main():
    logging.basicConfig(
        level=logging.INFO, 
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s")
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(basic_router)
    dp.include_router(club_application_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    asyncio.run(main())
    
