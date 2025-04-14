from aiogram import Dispatcher
import asyncio

from core.init_bot import bot
from components.handlers.user_handlers import router as user_router
from database.init_db import init_database

import logging


logging.basicConfig(level=logging.INFO)

async def main():
    await init_database()
    
    dp = Dispatcher()
    dp.include_router(user_router)
    
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except:
        pass