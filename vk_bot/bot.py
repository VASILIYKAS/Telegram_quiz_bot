import os
import logging
import asyncio

from dotenv import load_dotenv

import redis.asyncio as redis

import vk_api
from vk_api.longpoll import VkLongPoll

from open_questions import load_questions
from .handlers import handle_event



async def main():
    load_dotenv()

    vk_session = vk_api.VkApi(token=os.getenv("VK_BOT_TOKEN"))
    vk = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    redis_client = redis.Redis(
        host=os.getenv('REDIS_DB_HOST'),
        port=os.getenv('REDIS_DB_PORT'),
        decode_responses=True,
        username="default",
        password=os.getenv('REDIS_DB_PASSWORD'),
    )

    logging.basicConfig(level=logging.INFO)
    
    file_path = os.path.join(
        os.getenv('QUESTIONS_FOLDERS', 'questions'), 
        os.getenv('QUESTIONS_FILES', 'anime10.txt')
    )
    questions = load_questions(file_path)

    print("Бот ВК запущен!")

    for event in longpoll.listen():
        await handle_event(event, vk, redis_client, questions)


if __name__ == "__main__":
    asyncio.run(main())
