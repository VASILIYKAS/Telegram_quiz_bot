import asyncio
import logging
import sys
import os

from textwrap import dedent
from dotenv import load_dotenv
from questions_loader import load_questions
from .handlers import router

import redis.asyncio as redis

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand


async def set_menu_commands(bot: Bot):
    await bot.set_my_commands([
        BotCommand(command="start", description="Запустить бота"),
        BotCommand(command="help", description="Получить подробную информацию о боте")
    ])


async def startup(redis_client):
    try:
        await redis_client.ping()
        logging.info("Подключение к Redis успешно!")
    except redis.RedisError as e:
        logging.error(f"Ошибка подключения к Redis: {e}")
        raise
    
    
async def main() -> None:
    load_dotenv()
    
    bot = Bot(token=os.environ['TG_BOT_TOKEN'], default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    
    if not bot.token:
        print(dedent("""\
            Ошибка: Не указан TG_BOT_TOKEN.
            Убедитесь, что он задан в переменных окружения.
        """))
        return

    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    
    dp = Dispatcher()
    dp.include_router(router)
    
    redis_client = redis.Redis(
        host=os.environ['REDIS_DB_HOST'],
        port=os.environ['REDIS_DB_PORT'],
        decode_responses=True,
        username="default",
        password=os.environ['REDIS_DB_PASSWORD'],
    )
    
    file_path = os.path.join(
        os.getenv('QUESTIONS_FOLDERS', 'questions'), 
        os.getenv('QUESTIONS_FILES', 'anime10.txt')
    )
    
    questions = load_questions(file_path)
    
    dp['redis_client'] = redis_client
    dp['questions'] = questions
    
    await startup(redis_client)
    await set_menu_commands(bot)
    
    print("Бот запущен!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())