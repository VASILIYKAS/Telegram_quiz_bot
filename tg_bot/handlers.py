import random
import re

from open_questions import load_questions
from .keyboards import menu_keyboard

from redis.asyncio import Redis

from aiogram.filters import Command, CommandStart
from aiogram import Router, types, html, F
from aiogram.fsm.state import State, StatesGroup, any_state
from aiogram.fsm.context import FSMContext


router = Router()


class QuizStates(StatesGroup):
    START = State()
    WAITING_QUESTION = State()
    WAITING_ANSWER = State()
    GIVE_UP = State()
    SHOW_SCORE = State()    
    
    
@router.message(CommandStart())
async def command_start_handler(message: types.Message, state: FSMContext):
    await message.answer(
        f"Здравствуйте, {html.bold(message.from_user.full_name)}!\n"
        'Для начала игры нажмите "Новый вопрос".', 
        reply_markup=menu_keyboard()
    )
    await state.set_state(QuizStates.WAITING_QUESTION)


async def save_user_question(redis_client: Redis, user_id: int, question: str):
    await redis_client.set(f"user:{user_id}:question", question)
    

@router.message(F.text == "Новый вопрос", QuizStates.WAITING_QUESTION)
async def new_question(message: types.Message, state: FSMContext, redis_client: Redis):
    questions = load_questions(message.bot['questions_file_path'])
    question, answer = random.choice(list(questions.items()))
    
    await save_user_question(redis_client, message.from_user.id, question)
    await message.answer(f"Вопрос: {question}")
    await state.set_state(QuizStates.WAITING_ANSWER)
    
    
@router.message(F.text == "Сдаться", any_state)
async def give_up_handler(message: types.Message, state: FSMContext, redis_client: Redis):
    user_question_key = f"user:{message.from_user.id}:question"
    question = await redis_client.get(user_question_key)
    if question:
        questions = load_questions(message.bot['questions_file_path'])
        correct_answer = questions.get(question)
        await message.answer(f"Ответ: {correct_answer}")
        await redis_client.delete(user_question_key)
        await state.set_state(QuizStates.WAITING_QUESTION)
    else:
        await message.answer('Вы ещё не начали игру! Нажмите "Новый вопрос".')
    
    
@router.message(F.text == "Мой счёт", any_state)
async def my_score_handler(message: types.Message, state: FSMContext, redis_client: Redis):
    score_key = f"user:{message.from_user.id}:score"
    score = await redis_client.get(score_key) or 0
    await message.answer(f"Ваш счёт: {int(score)} правильных ответов.")
    await state.set_state(QuizStates.WAITING_QUESTION)


@router.message(QuizStates.WAITING_ANSWER)
async def check_answer_handler(message: types.Message, state: FSMContext, redis_client: Redis):
    questions = load_questions(message.bot['questions_file_path'])
    user_question_key = f"user:{message.from_user.id}:question"
    question = await redis_client.get(user_question_key)
    if not question:
        await message.answer("Для начала нажмите 'Новый вопрос'.")
        await state.set_state(QuizStates.WAITING_QUESTION)
        return

    correct_answer = questions.get(question, '').lower().strip('"')
    clear_answer = re.sub(r'\d+\.', '', correct_answer)
    user_answer = message.text.lower().strip()

    if user_answer == clear_answer:
        await message.answer(
            'Правильно! Поздравляю!\n'
            'Для следующего вопроса нажми «Новый вопрос»',
            reply_markup=menu_keyboard()
        )
        await redis_client.delete(user_question_key)

        score_key = f"user:{message.from_user.id}:score"
        current_score = await redis_client.get(score_key) or 0
        new_score = int(current_score) + 1
        await redis_client.set(score_key, new_score)

        await state.set_state(QuizStates.WAITING_QUESTION)
    else:
        await message.answer('Неправильно… Попробуешь ещё раз?')