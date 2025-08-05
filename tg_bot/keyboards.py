from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def menu_keyboard():
    return ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=False,
        keyboard=[
            [KeyboardButton(text="Новый вопрос"), KeyboardButton(text="Сдаться")],
            [KeyboardButton(text="Мой счёт")],
        ]
    )