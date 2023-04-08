from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from tgbot_app.keyboards.inline.creation_keyboard import chatgpt_cd
from tgbot_app.keyboards.inline.start_keyboard import main_menu_cd


async def gen_chatgpt_kb(place):
    markup = InlineKeyboardMarkup(row_width=1)

    markup.add(
        InlineKeyboardButton(text='Улучшить', callback_data=chatgpt_cd.new(action='specify', place=place)),
        InlineKeyboardButton(text='Назад', callback_data=main_menu_cd.new(action=place)),
    )

    return markup
