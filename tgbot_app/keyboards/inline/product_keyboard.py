from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from tgbot_app.common.database import get_active_session

product_cd = CallbackData('product', 'is_new')


def make_callback_data(is_new):
    return product_cd.new(is_new=is_new)


async def gen_product_keyboard(user_id):
    markup = InlineKeyboardMarkup()
    open_session = await get_active_session(user_id)

    if not open_session:
        markup.add(InlineKeyboardButton(
            text='Загрузить SKU',
            callback_data=make_callback_data(is_new='True')
        ))

        return markup


