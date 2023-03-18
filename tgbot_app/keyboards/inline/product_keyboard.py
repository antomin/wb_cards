from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from tgbot_app.common.database import get_active_session

scu_cd = CallbackData('scu')
product_cd = CallbackData('product', 'field', 'level')
cancel_state_cd = CallbackData('cancel_state')

details_cd = CallbackData('details', 'field', 'level', 'is_back')
change_detail_cd = CallbackData('change', 'field')

chatgpt_cd = CallbackData('chatgpt', 'action')


async def gen_product_kb(user_id):
    markup = InlineKeyboardMarkup(row_width=1)
    session = await get_active_session(user_id)

    if not session:
        markup.add(InlineKeyboardButton(text='SKU', callback_data=scu_cd.new()))

    markup.add(
        InlineKeyboardButton(text='Название', callback_data=product_cd.new(field='title', level='no')),
        InlineKeyboardButton(text='Характеристики', callback_data=product_cd.new(field='characteristics', level='0')),
        InlineKeyboardButton(text='Описание', callback_data=product_cd.new(field='description', level='0')),
        InlineKeyboardButton(text='SEO словарь', callback_data=product_cd.new(field='seo_dict', level='0')),
        InlineKeyboardButton(text='SEO +', callback_data=product_cd.new(field='seo_plus', level='0')),
        InlineKeyboardButton(text='Главное о товаре', callback_data=product_cd.new(field='important', level='0')),
        InlineKeyboardButton(text='Дополнительно', callback_data=product_cd.new(field='other_description', level='0')),
        InlineKeyboardButton(text='Помощь', callback_data=product_cd.new(field='help', level='no')),
        InlineKeyboardButton(text='Назад', callback_data=product_cd.new(field='back', level='no')),
    )

    return markup


async def gen_cancel_kb():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton(text='Отмена', callback_data=cancel_state_cd.new()))

    return markup


async def gen_details_kb(field):
    markup = InlineKeyboardMarkup(row_width=2)

    markup.add(
        InlineKeyboardButton(text='Назад', callback_data=product_cd.new(field=field, level='0')),
        InlineKeyboardButton(text='Назад', callback_data=product_cd.new(field=field, level='1')),
    )

    return markup

#
#
# async def gen_current_detail_kb(field):
#     markup = InlineKeyboardMarkup(row_width=2)
#
#     markup.add(
#         InlineKeyboardButton(
#             text='Назад',
#             callback_data=details_cd.new(field=field, level='0', is_back='True')
#         ),
#         InlineKeyboardButton(
#             text='Изменить',
#             callback_data=details_cd.new(field=field, level='1', is_back='False')
#         )
#     )
#
#     return markup
#
#

