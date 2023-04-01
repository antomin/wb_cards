from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

cancel_state_cd = CallbackData('cancel_state', 'place')
style_cd = CallbackData('style', 'value', 'place')


async def gen_cancel_kb(place):
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton(text='Отмена', callback_data=cancel_state_cd.new(place=place)))

    return markup


async def gen_style_kb(place):
    markup = InlineKeyboardMarkup(row_width=1)

    markup.add(
        InlineKeyboardButton(text='Обычный', callback_data=style_cd.new(value='обычный', place=place)),
        InlineKeyboardButton(text='Творческий', callback_data=style_cd.new(value='творческий', place=place)),
        InlineKeyboardButton(text='Формальный', callback_data=style_cd.new(value='формальный', place=place)),
    )

    return markup
