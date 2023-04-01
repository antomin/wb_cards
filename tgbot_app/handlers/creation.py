from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from tgbot_app.keyboards.inline import (creation_cd, gen_cancel_kb,
                                        gen_creation_kb, gen_creation_next_kb,
                                        gen_style_kb, main_menu_cd)
from tgbot_app.loader import dp
from tgbot_app.utils.database import get_active_session
from tgbot_app.utils.text_variables import CREATION_MSG, STYLE_DESC
from tgbot_app.utils.values_utils import get_value


@dp.callback_query_handler(main_menu_cd.filter(action='creation'))
async def start_creation(callback: CallbackQuery):
    markup = await gen_creation_kb()

    await callback.message.answer(text=CREATION_MSG, reply_markup=markup, disable_web_page_preview=True)
    await callback.answer()


@dp.callback_query_handler(creation_cd.filter(level='2'))
async def next_creation(callback: CallbackQuery):
    user_id = callback.from_user.id
    session = await get_active_session(user_id)

    if not session:
        text = 'Нет никаких данных о товаре. Вернитесь назад и введите данные.'
        markup = await gen_creation_next_kb(session=False)
    else:
        text = f'<b>{session.title}</b>'
        if session.important:
            text += f'\n\n<b>Главное о товаре:</b>\n{session.important}'
        if session.sku_plus:
            text += f'\n\n<b>Дополнительные SKU:</b>\n{session.sku_plus}.'
        markup = await gen_creation_next_kb()

    await callback.message.answer(text=text, reply_markup=markup)
    await callback.answer()


@dp.callback_query_handler(creation_cd.filter(level='1'))
async def load_fields(callback: CallbackQuery, state: FSMContext, callback_data: dict):
    field = callback_data.get('field')
    if field in ('keywords', 'seo_phrases', 'minus_words', 'style'):
        place = 'creation_next'
    else:
        place = 'creation'
    markup = await gen_cancel_kb(place)

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
        text = value + '\n\nВведите через запятую до 5 SCU карточек с хорошим описанием:'
    elif field == 'style':
        text = STYLE_DESC
        markup = await gen_style_kb('creation')
        await state.reset_state()
    else:
        text = value + '\n\nДанные генерируются на основе введённой информации. Но вы можете их изменить:'

    await callback.message.answer(text=text, reply_markup=markup)
    await callback.answer()


