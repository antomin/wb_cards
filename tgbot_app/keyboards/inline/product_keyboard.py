from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from tgbot_app.keyboards.inline.help_keyboard import help_cd
from tgbot_app.keyboards.inline.start_keyboard import main_menu_cd

scu_cd = CallbackData('scu')
product_cd = CallbackData('product', 'field')


async def gen_product_kb():
    markup = InlineKeyboardMarkup(row_width=2)

    markup.add(InlineKeyboardButton(text='SKU', callback_data=scu_cd.new()))

    markup.add(
        InlineKeyboardButton(text='Название', callback_data=product_cd.new(field='title')),
        InlineKeyboardButton(text='Характеристики', callback_data=product_cd.new(field='characteristics')),
        InlineKeyboardButton(text='Описание', callback_data=product_cd.new(field='description')),
        InlineKeyboardButton(text='SEO словарь', callback_data=product_cd.new(field='seo_dict')),
        InlineKeyboardButton(text='SEO +', callback_data=product_cd.new(field='seo_plus')),
        InlineKeyboardButton(text='Главное о товаре', callback_data=product_cd.new(field='important')),
        InlineKeyboardButton(text='Дополнительно', callback_data=product_cd.new(field='other_description')),
        InlineKeyboardButton(text='Помощь', callback_data=help_cd.new(place='product')),
        InlineKeyboardButton(text='Назад', callback_data=main_menu_cd.new(action='main_menu')),
    )

    return markup

