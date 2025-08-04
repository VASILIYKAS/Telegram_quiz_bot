from aiogram.filters import CommandStart
from aiogram import Router, types, html
from keyboards import (
    menu_keyboard,
)


router = Router()


@router.message(CommandStart())
async def command_start_handler(message: types.Message) -> None:
    await message.answer(f"Здравствуйте, {html.bold(message.from_user.full_name)}!", reply_markup=menu_keyboard())
    

@router.message()
async def echo_handler(message: types.Message) -> None:
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.answer("Nice try!")



