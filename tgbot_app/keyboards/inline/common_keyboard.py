from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

cancel_state_cd = CallbackData('cancel_state', 'place')


async def gen_cancel_kb(place):
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton(text='Отмена', callback_data=cancel_state_cd.new(place=place)))

    return markup
