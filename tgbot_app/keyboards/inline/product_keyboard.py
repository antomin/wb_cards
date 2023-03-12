from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from tgbot_app.common.database import get_active_session

product_cd = CallbackData('product', 'is_new')
details_cd = CallbackData('details', 'field', 'level', 'is_back')
change_detail_cd = CallbackData('change', 'field')
cancel_cd = CallbackData('cancel')
chatgpt_cd = CallbackData('chatgpt', 'action')


async def gen_product_kb(user_id):
    markup = InlineKeyboardMarkup(row_width=1)
    session = await get_active_session(user_id)

    if not session:
        markup.add(InlineKeyboardButton(text='Загрузить SKU', callback_data=product_cd.new(is_new='True')))

        return markup

    markup.add(
        InlineKeyboardButton(
            text='Наименование',
            callback_data=details_cd.new(field='product_title', level='0', is_back='False')
        ),
        InlineKeyboardButton(
            text='Характеристики',
            callback_data=details_cd.new(field='product_characteristics', level='0', is_back='False')
        ),
        InlineKeyboardButton(
            text='Описание',
            callback_data=details_cd.new(field='product_description', level='0', is_back='False')
        ),
        InlineKeyboardButton(
            text='Дополнительно',
            callback_data=details_cd.new(field='other_descriptions', level='0', is_back='False')
        ),
        InlineKeyboardButton(
            text='SEO словарь',
            callback_data=details_cd.new(field='seo_dict', level='0', is_back='False')
        ),
        InlineKeyboardButton(
            text='ChatGPT магия',
            callback_data=chatgpt_cd.new(action='start')
        ),
    )

    return markup


async def gen_current_detail_kb(field):
    markup = InlineKeyboardMarkup(row_width=2)

    markup.add(
        InlineKeyboardButton(
            text='Назад',
            callback_data=details_cd.new(field=field, level='0', is_back='True')
        ),
        InlineKeyboardButton(
            text='Изменить',
            callback_data=details_cd.new(field=field, level='1', is_back='False')
        )
    )

    return markup


async def gen_cancel_kb():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton(text='Отмена', callback_data=cancel_cd.new()))

    return markup
