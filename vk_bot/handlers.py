import random
import re
from vk_api.longpoll import VkEventType

from .keyboards import menu_keyboard


def send_message(vk, user_id, text, keyboard=None):
    vk.messages.send(
        user_id=user_id,
        message=text,
        random_id=0,
        keyboard=keyboard
    )


async def handle_event(event, vk, redis_client, questions):
    if event.type != VkEventType.MESSAGE_NEW or not event.to_me:
        return

    user_id = event.user_id
    message = event.text.strip()

    if message == "Новый вопрос":
        question, _ = random.choice(list(questions.items()))
        await redis_client.set(f"user:{user_id}:question", question)
        send_message(vk, user_id, f"Вопрос: {question}", keyboard=menu_keyboard())

    elif message == "Сдаться":
        question = await redis_client.get(f"user:{user_id}:question")
        if question:
            correct_answer = questions.get(question)
            send_message(vk, user_id, f"Ответ:\n{correct_answer}")
            await redis_client.delete(f"user:{user_id}:question")
        else:
            send_message(vk, user_id, 'Вы ещё не начали игру! Нажмите "Новый вопрос".')

    elif message == "Мой счёт":
        score = await redis_client.get(f"user:{user_id}:score") or 0
        send_message(vk, user_id, f"Ваш счёт: {int(score)} правильных ответов.")

    else:
        question = await redis_client.get(f"user:{user_id}:question")
        if not question:
            send_message(vk, user_id, "Для начала нажмите 'Новый вопрос'.")
            return

        correct_answer= questions.get(question, '')

        correct_answer_clean = re.sub(
            r'^\d+\.\s*', '', correct_answer,
            flags=re.MULTILINE
        ).strip('"').lower()

        user_answer = message.lower().strip()

        if user_answer == correct_answer_clean:
            send_message(
                vk, user_id,
                "Правильно! Поздравляю!\nДля следующего вопроса нажми «Новый вопрос»",
                keyboard=menu_keyboard()
            )
            await redis_client.delete(f"user:{user_id}:question")

            score_key = f"user:{user_id}:score"
            current_score = await redis_client.get(score_key) or 0
            await redis_client.set(score_key, int(current_score) + 1)

        else:
            send_message(vk, user_id, "Неправильно… Попробуешь ещё раз?")
