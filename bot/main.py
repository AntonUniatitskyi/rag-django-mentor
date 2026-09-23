import asyncio
import logging
from aiogram import Bot, Dispatcher
from .handlers.mentor import router
import config
from aiogram.types import BotCommand

async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=config.BOT_TOKEN)
    await bot.set_my_commands([
        BotCommand(command="start", description="Почати роботу"),
        BotCommand(command="new", description="Нова розмова (очистити історію)"),
    ])
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())