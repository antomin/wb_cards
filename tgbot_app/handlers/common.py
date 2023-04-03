from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from tgbot_app.handlers.chatgpt import chat_gpt_creation
from tgbot_app.handlers.creation import next_creation, start_creation
from tgbot_app.handlers.product import product
from tgbot_app.keyboards.inline import (cancel_state_cd, gen_chatgpt_kb,
                                        gen_creation_kb, gen_creation_next_kb,
                                        gen_product_kb, style_cd)
from tgbot_app.loader import dp
from tgbot_app.utils.database import add_user_session, get_active_session
from tgbot_app.utils.text_variables import CREATION_MSG, HELP_PRODUCT
from tgbot_app.utils.values_utils import update_data


@dp.message_handler(state='change_data')
async def save_fields(message: Message, state: FSMContext):
    user_id = message.from_user.id
    value = message.text
    async with state.proxy() as data:
        field = data.get('field')
        place = data.get('place')

    if place == 'creation':
        markup = await gen_creation_kb()
    elif place == 'product':
        markup = await gen_product_kb(user_id)
    else:
        markup = await gen_creation_next_kb()

    session = await get_active_session(user_id)
    if not session:
        await add_user_session(user_id, message.from_user.username, {})

    if field == 'sku_plus':
        value = ', '.join([scu.strip() for scu in value.split(',') if scu.isdigit()])

    if field == 'characteristics':
        await message.answer('Раздел "Характеристики" находится на доработке.', reply_markup=markup)
        await state.reset_state()
        return

    await update_data(user_id, field, value)

    await message.answer('Данные успешно обновлены.', reply_markup=markup)
    await state.reset_state()


@dp.callback_query_handler(cancel_state_cd.filter(), state='*')
async def cancel_changing(callback: CallbackQuery, state: FSMContext, callback_data: dict):
    place = callback_data.get('place')

    funcs = {'product': product, 'creation': start_creation, 'creation_next': next_creation}

    await chat_gpt_creation(callback, callback_data) if place == 'chatgpt' else await funcs[place](callback)

    await state.reset_state()
    await callback.answer()


@dp.callback_query_handler(style_cd.filter())
async def save_style(callback: CallbackQuery, callback_data: dict):
    user_id = callback.from_user.id
    place = callback_data.get('place')
    markup = await gen_creation_next_kb() if place == 'creation' else await gen_product_kb(user_id)
    value = callback_data.get('value')
    await update_data(user_id, 'style', value)

    await callback.message.answer(f'Вы изменили стиль описания на <b>{value}</b>.', reply_markup=markup)
    await callback.answer()
