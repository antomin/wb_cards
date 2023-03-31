from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from tgbot_app.keyboards.inline import (creation_cd, gen_cancel_kb,
                                        gen_creation_kb, main_menu_cd)
from tgbot_app.loader import dp
from tgbot_app.utils.database import get_active_session
from tgbot_app.utils.text_variables import CREATION_MSG
from tgbot_app.utils.values_utils import get_value


@dp.callback_query_handler(main_menu_cd.filter(action='creation'))
async def start_creation(callback: CallbackQuery):
    markup = await gen_creation_kb()
    session = await get_active_session(callback.from_user.id)

    if session:
        text = f'<b>Главное о товаре:</b>\n{session.important}'
        if session.sku_plus:
            text += f'\n\n<b>Дополнительные SKU:</b>\n{session.sku_plus}.'
    else:
        text = CREATION_MSG

    await callback.message.answer(text=text, reply_markup=markup, disable_web_page_preview=True)
    await callback.answer()


@dp.callback_query_handler(creation_cd.filter(level='1'))
async def load_fields(callback: CallbackQuery, state: FSMContext, callback_data: dict):
    markup = await gen_cancel_kb('creation')
    field = callback_data.get('field')

    await state.set_state('change_data')
    async with state.proxy() as data:
        data['field'] = field
        data['place'] = 'creation'

    value = await get_value(callback.from_user.id, field)

    if field == 'important':
        text = value + '\n\nКратко опишите ключевые особенности товара:'
    elif field == 'title':
        text = value + '\n\nНапишите наименование товара:'
    elif field == 'sku_plus':
        text = value + '\n\nВведите через запитую до 5 SCU карточек с хорошим описанием:'
    else:
        text = value + '\n\nДанные генерируются на основе введённой информации. Но вы можете их изменить:'

    await callback.message.answer(text=text, reply_markup=markup)
    await callback.answer()


