from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from tgbot_app.keyboards.inline.start_keyboard import main_menu_cd

creation_cd = CallbackData('creation', 'field', 'level')


async def gen_creation_kb():
    markup = InlineKeyboardMarkup(row_width=2)

    markup.row(InlineKeyboardButton(text='Название', callback_data=creation_cd.new(field='title', level=1)))
    markup.row(InlineKeyboardButton(text='Главное в товаре', callback_data=creation_cd.new(field='important', level=1)))
    markup.row(InlineKeyboardButton(text='SKU +', callback_data=creation_cd.new(field='sku_plus', level=1)))
    markup.row(InlineKeyboardButton(text='SEO словарь', callback_data=creation_cd.new(field='seo_dict', level=1)))
    markup.row(
        InlineKeyboardButton(text='Назад', callback_data=main_menu_cd.new(action='main_menu')),
        InlineKeyboardButton(text='Дальше', callback_data=creation_cd.new(field='no', level=2)),
    )

    return markup
