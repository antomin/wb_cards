from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.exceptions import MessageNotModified

from tgbot_app.common.database import add_user_session
from tgbot_app.common.text_variables import NEW_SKU
from tgbot_app.common.utils import get_value, update_data
from tgbot_app.common.wb_parser import parse_wb
from tgbot_app.keyboards.inline.product_keyboard import (cancel_cd, details_cd,
                                                         gen_cancel_kb,
                                                         gen_current_detail_kb,
                                                         gen_product_kb,
                                                         product_cd)
from tgbot_app.loader import dp


@dp.message_handler(lambda message: 'Товар' in message.text)
async def product(message: Message):
    keyboard = await gen_product_kb(message.from_user.id)
    await message.delete()
    await message.answer('Товар', reply_markup=keyboard)


@dp.callback_query_handler(product_cd.filter(is_new='True'))
async def product_handler(callback: CallbackQuery, state: FSMContext):
    await state.set_state('new_sku')
    await callback.answer()
    await callback.message.answer(text=NEW_SKU)


@dp.message_handler(state='new_sku')
async def add_new_sku(message: Message, state: FSMContext):
    new_sku = message.text

    if new_sku.isdigit():
        await message.answer('Загрузка данных...')
        data = await parse_wb(new_sku)

        if not data:
            await message.answer('Неверный SKU. попробуйте ещё раз:')
            return

        await add_user_session(message.from_user, data)
        await message.answer('Данные загружены.')
        await state.reset_state()

    else:
        await message.answer('Неверный SKU. попробуйте ещё раз:')


@dp.callback_query_handler(details_cd.filter(level='0'))
async def show_details(callback: CallbackQuery, callback_data: dict):
    field = callback_data.get('field')
    is_back = callback_data.get('is_back')
    text = await get_value(callback.from_user.id, field)

    if is_back == 'True':
        markup = await gen_product_kb(callback.from_user.id)
    else:
        markup = await gen_current_detail_kb(field)

    try:
        await callback.message.edit_text(text=text, reply_markup=markup)
    except MessageNotModified:
        await callback.answer()


@dp.callback_query_handler(details_cd.filter(level='1'))
async def change_details(callback: CallbackQuery, callback_data: dict, state: FSMContext):
    field = callback_data.get('field')
    await state.set_state('change_data')

    async with state.proxy() as data:
        data['field'] = field

    if field == 'product_characteristics':
        await callback.message.edit_text(
            text='Введите новые характеристики в формате <u>ключ: значение</u>. Каждая новая характеристика вводится с'
                 'новой строки:',
            reply_markup=await gen_cancel_kb()
        )
        await callback.answer()
        return

    if field == 'other_descriptions':
        await callback.message.edit_text(
            text='Введите через пробел SKU с желаемыми описаниями (максимум 3):',
            reply_markup=await gen_cancel_kb()
        )
        await callback.answer()
        return

    await callback.message.answer('Введите новые данные:', reply_markup=await gen_cancel_kb())
    await callback.answer()


@dp.message_handler(state='change_data')
async def save_new_details(message: Message, state: FSMContext):
    user_id = message.from_user.id
    value = message.text
    async with state.proxy() as data:
        field = data['field']

    if field == 'other_descriptions':
        await message.answer('Загрузка данных...')

    if await update_data(user_id, field, value):
        await message.answer(
            text='Данные успешно изменены.',
            reply_markup=await gen_product_kb(user_id)
        )
        await state.reset_state()
        return

    await message.answer(
        text='Ошибка при добавлении данных. Попробуйте ещё раз:',
        reply_markup=await gen_cancel_kb()
    )


@dp.callback_query_handler(cancel_cd.filter(), state='change_data')
async def cancel_changing(callback: CallbackQuery, state: FSMContext):
    await state.reset_state()
    await callback.message.edit_text(text='Отменено', reply_markup=await gen_product_kb(callback.from_user.id))
