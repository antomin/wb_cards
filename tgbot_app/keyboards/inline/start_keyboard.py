from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

main_menu_cd = CallbackData('main', 'action')


async def gen_main_kb():
    markup = InlineKeyboardMarkup(row_width=1)

    markup.add(
        InlineKeyboardButton(text='Товар', callback_data=main_menu_cd.new(action='product')),
        InlineKeyboardButton(text='ChatGPT магия', callback_data=main_menu_cd.new(action='chatgpt')),
        InlineKeyboardButton(text='Аккаунт', callback_data=main_menu_cd.new(action='account')),
        InlineKeyboardButton(text='Обновить', callback_data=main_menu_cd.new(action='update')),
    )

    return markup
