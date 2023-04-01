from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from tgbot_app.keyboards.inline.creation_keyboard import (chatgpt_cd,
                                                          creation_cd)
from tgbot_app.keyboards.inline.start_keyboard import main_menu_cd


async def gen_chatgpt_kb(place):
    markup = InlineKeyboardMarkup(row_width=1)
    callback_data = creation_cd.new(field='next', level=2) if place == 'creation_next' else main_menu_cd.new(
        action='product')
    markup.add(
        InlineKeyboardButton(text='Улучшить', callback_data=chatgpt_cd.new(action='specify', place=place)),
        InlineKeyboardButton(text='Назад', callback_data=callback_data),
    )

    return markup
