from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from tgbot_app.keyboards.inline.start_keyboard import main_menu_cd

update_cd = CallbackData('update')


async def gen_update_kb():
    markup = InlineKeyboardMarkup(row_width=2)

    markup.add(
        InlineKeyboardButton(text='Назад', callback_data=main_menu_cd.new(action='main_menu')),
        InlineKeyboardButton(text='Да', callback_data=update_cd.new())
    )

    return markup
