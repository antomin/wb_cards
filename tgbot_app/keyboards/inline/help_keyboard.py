from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from tgbot_app.keyboards.inline.start_keyboard import main_menu_cd

help_cd = CallbackData('help', 'place')


async def gen_help_kb(place):
    markup = InlineKeyboardMarkup()

    if place == 'product':
        callback_data = main_menu_cd.new(action='product')
    else:
        callback_data = ''

    markup.add(InlineKeyboardButton(text='Назад', callback_data=callback_data))

    return markup
