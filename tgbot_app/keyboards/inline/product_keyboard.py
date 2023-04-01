from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from tgbot_app.keyboards.inline import chatgpt_cd
from tgbot_app.keyboards.inline.start_keyboard import main_menu_cd
from tgbot_app.utils.database import get_active_session

scu_cd = CallbackData('scu')
product_cd = CallbackData('product', 'field')


async def gen_product_kb(user_id):
    markup = InlineKeyboardMarkup(row_width=1)
    session = await get_active_session(user_id)

    if not session:
        markup.add(InlineKeyboardButton(text='SKU', callback_data=scu_cd.new()))

    else:
        markup.add(
            InlineKeyboardButton(text='Название', callback_data=product_cd.new(field='title')),
            InlineKeyboardButton(text='Характеристики', callback_data=product_cd.new(field='characteristics')),
            InlineKeyboardButton(text='Описание', callback_data=product_cd.new(field='description')),
            InlineKeyboardButton(text='SEO +', callback_data=product_cd.new(field='seo_dict')),
            InlineKeyboardButton(text='Стиль', callback_data=product_cd.new(field='style')),
            InlineKeyboardButton(text='GPT Магия', callback_data=chatgpt_cd.new(action='make', place='product')),
        )

    markup.add(InlineKeyboardButton(text='Назад', callback_data=main_menu_cd.new(action='main_menu')))

    return markup

