from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
import logging

from config import BOT_TOKEN
import handlers

logging.basicConfig(
    level = logging.INFO,
    format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def main():
    bot = Bot(
        token = BOT_TOKEN,
        default = DefaultBotProperties(parse_mode = ParseMode.HTML)
    )
    
    dp = Dispatcher()
    
    dp.include_router(handlers.router)
    
    await bot.delete_webhook(drop_pending_updates = True)
    logger.info("Бот запущен!")
    
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
        
if __name__ == '__main__':
    import asyncio
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Бот остановлен")