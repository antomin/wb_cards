from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from tgbot_app.keyboards.inline.help_keyboard import help_cd
from tgbot_app.keyboards.inline.start_keyboard import main_menu_cd

scu_cd = CallbackData('scu')
product_cd = CallbackData('product', 'field', 'level')
cancel_state_cd = CallbackData('cancel_state')


async def gen_product_kb():
    markup = InlineKeyboardMarkup(row_width=2)

    markup.add(InlineKeyboardButton(text='SKU', callback_data=scu_cd.new()))

    markup.add(
        InlineKeyboardButton(text='Название', callback_data=product_cd.new(field='title', level='0')),
        InlineKeyboardButton(text='Характеристики', callback_data=product_cd.new(field='characteristics', level='0')),
        InlineKeyboardButton(text='Описание', callback_data=product_cd.new(field='description', level='0')),
        InlineKeyboardButton(text='SEO словарь', callback_data=product_cd.new(field='seo_dict', level='0')),
        InlineKeyboardButton(text='SEO +', callback_data=product_cd.new(field='seo_plus', level='0')),
        InlineKeyboardButton(text='Главное о товаре', callback_data=product_cd.new(field='important', level='0')),
        InlineKeyboardButton(text='Дополнительно', callback_data=product_cd.new(field='other_description', level='0')),
        InlineKeyboardButton(text='Помощь', callback_data=help_cd.new(place='product')),
        InlineKeyboardButton(text='Назад', callback_data=main_menu_cd.new(action='main_menu')),
    )

    return markup


async def gen_cancel_kb():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton(text='Отмена', callback_data=cancel_state_cd.new()))

    return markup


async def gen_details_kb(field):
    markup = InlineKeyboardMarkup(row_width=2)

    if field in ['characteristics', 'seo_dict']:
        change_btn = InlineKeyboardButton(text='На доработке', callback_data=main_menu_cd.new(action='product'))
    else:
        change_btn = InlineKeyboardButton(text='Изменить', callback_data=product_cd.new(field=field, level='1'))

    markup.add(
        InlineKeyboardButton(text='Назад', callback_data=main_menu_cd.new(action='product')),
        change_btn,
    )

    return markup
