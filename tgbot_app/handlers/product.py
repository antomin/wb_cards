from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.exceptions import MessageNotModified

from tgbot_app.common.database import add_user_session, get_active_session
from tgbot_app.common.text_variables import NEW_SKU
from tgbot_app.common.utils import get_value, update_data
from tgbot_app.common.wb_parser import parse_wb
from tgbot_app.keyboards.inline import (cancel_state_cd, gen_cancel_kb,
                                        gen_details_kb, gen_product_kb,
                                        main_menu_cd, product_cd, scu_cd)
from tgbot_app.loader import dp


@dp.callback_query_handler(main_menu_cd.filter(action='product'))
async def product(callback: CallbackQuery):
    user_id = callback.from_user.id
    markup = await gen_product_kb(user_id)
    await callback.message.edit_text(text='Меню товара:', reply_markup=markup)


@dp.callback_query_handler(scu_cd.filter())
async def sku(callback: CallbackQuery, state: FSMContext):
    markup = await gen_cancel_kb()
    await state.set_state('new_scu')
    await callback.answer()
    await callback.message.edit_text(text=NEW_SKU, reply_markup=markup)


@dp.message_handler(state='new_scu')
async def load_scu(message: Message, state: FSMContext):
    user_id = message.from_user.id
    cancel_markup = await gen_cancel_kb()
    _sku = message.text

    if _sku.isdigit():
        await message.answer('Загрузка данных...')

        data = await parse_wb(_sku)

        if not data:
            await message.answer('Неверный SKU. попробуйте ещё раз:', reply_markup=cancel_markup)
            return

        await add_user_session(user_id, message.from_user.username, data)

        text = f'<b>Название:</b>\n{data["title"]}\n\n<b>Описание:</b>\n{data["description"][:100]}...'
        markup = await gen_product_kb(user_id)

        await message.answer(text=text, reply_markup=markup)
        await state.reset_state()

    else:
        await message.answer('Неверный SKU. попробуйте ещё раз:', reply_markup=cancel_markup)


@dp.callback_query_handler(product_cd.filter(level='0'))
async def show_product_details(callback: CallbackQuery, callback_data: dict):
    user_id = callback.from_user.id
    field = callback_data.get('field')

    session = await get_active_session(user_id)
    if not session:
        await add_user_session(user_id, callback.from_user.username, {})

    value = await get_value(user_id, field)
    markup = await gen_details_kb(field)

    if field == 'seo_dict':
        value = 'Раздел на доработке.'

    try:
        await callback.message.edit_text(text=value, reply_markup=markup)
    except MessageNotModified:
        await callback.answer()


@dp.callback_query_handler(product_cd.filter(level='1'))
async def edit_product_details(callback: CallbackQuery, state: FSMContext, callback_data: dict):
    field = callback_data.get('field')

    await state.set_state('change_data')

    async with state.proxy() as data:
        data['field'] = field

    if field == 'seo_plus':
        text = 'Введите SEO слова через запятую:'
    elif field == 'important':
        text = 'Опишите главные преимущества Вашего товара:'
    else:
        text = 'Введите новые данные:'

    await callback.message.answer(text=text, reply_markup=await gen_cancel_kb())
    await callback.answer()


@dp.message_handler(state='change_data')
async def save_new_details(message: Message, state: FSMContext):
    user_id = message.from_user.id
    value = message.text

    async with state.proxy() as data:
        field = data['field']

    result = await update_data(user_id, field, value)

    if result:
        await message.answer(text='Данные успешно изменены.', reply_markup=await gen_product_kb(user_id))
        await state.reset_state()
        return

    await message.answer(
        text='Ошибка при добавлении данных. Попробуйте ещё раз:',
        reply_markup=await gen_cancel_kb()
    )


@dp.callback_query_handler(cancel_state_cd.filter(), state='*')
async def cancel_changing(callback: CallbackQuery, state: FSMContext):
    markup = await gen_product_kb(callback.from_user.id)
    await callback.answer()
    await state.reset_state()
    await callback.message.edit_text(text='Отменено.', reply_markup=markup)



# @dp.callback_query_handler(details_cd.filter(level='1'))
# async def change_details(callback: CallbackQuery, callback_data: dict, state: FSMContext):
#     field = callback_data.get('field')
#     await state.set_state('change_data')
#
#     async with state.proxy() as data:
#         data['field'] = field
#
#     if field == 'product_characteristics':
#         await callback.message.edit_text(
#             text='Введите новые характеристики в формате <u>ключ: значение</u>. Каждая новая характеристика вводится с'
#                  'новой строки:',
#             reply_markup=await gen_cancel_kb()
#         )
#         await callback.answer()
#         return
#
#     if field == 'other_descriptions':
#         await callback.message.edit_text(
#             text='Введите через пробел SKU с желаемыми описаниями (максимум 3):',
#             reply_markup=await gen_cancel_kb()
#         )
#         await callback.answer()
#         return
#
#     await callback.message.answer('Введите новые данные:', reply_markup=await gen_cancel_kb())
#     await callback.answer()
#
#
# @dp.message_handler(state='change_data')
# async def save_new_details(message: Message, state: FSMContext):
#     user_id = message.from_user.id
#     value = message.text
#     async with state.proxy() as data:
#         field = data['field']
#
#     if field == 'other_descriptions':
#         await message.answer('Загрузка данных...')
#
#     if await update_data(user_id, field, value):
#         await message.answer(
#             text='Данные успешно изменены.',
#             reply_markup=await gen_product_kb(user_id)
#         )
#         await state.reset_state()
#         return
#
#     await message.answer(
#         text='Ошибка при добавлении данных. Попробуйте ещё раз:',
#         reply_markup=await gen_cancel_kb()
#     )
#
#
# @dp.callback_query_handler(cancel_cd.filter(), state='change_data')
# async def cancel_changing(callback: CallbackQuery, state: FSMContext):
#     await state.reset_state()
#     await callback.message.edit_text(text='Отменено', reply_markup=await gen_product_kb(callback.from_user.id))
