from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.exceptions import MessageNotModified

from tgbot_app.common.database import add_user_session, get_active_session
from tgbot_app.common.text_variables import HELP_PRODUCT, NEW_SKU
from tgbot_app.common.utils import get_value, update_data
from tgbot_app.common.wb_parser import parse_wb
from tgbot_app.keyboards.inline import (gen_cancel_kb, gen_details_kb,
                                        gen_product_kb, main_menu_cd,
                                        product_cd, scu_cd)
from tgbot_app.loader import dp


@dp.message_handler(commands=['product'])
@dp.callback_query_handler(main_menu_cd.filter(action='product'))
async def product(callback: CallbackQuery | Message):
    markup = await gen_product_kb()

    if isinstance(callback, CallbackQuery):
        await callback.message.edit_text(text=HELP_PRODUCT, reply_markup=markup, disable_web_page_preview=True)
        return

    await callback.answer(text=HELP_PRODUCT, reply_markup=markup)


@dp.callback_query_handler(scu_cd.filter())
async def sku(callback: CallbackQuery, state: FSMContext):
    markup = await gen_cancel_kb('product')
    await state.set_state('new_scu')
    await callback.answer()
    await callback.message.edit_text(text=NEW_SKU, reply_markup=markup)


@dp.message_handler(state='new_scu')
async def load_scu(message: Message, state: FSMContext):
    cancel_markup = await gen_cancel_kb('product')
    _sku = message.text

    if _sku.isdigit():
        await message.answer('Загрузка данных...')

        data = await parse_wb(_sku)

        if not data:
            await message.answer('Неверный SKU. попробуйте ещё раз:', reply_markup=cancel_markup)
            return

        await add_user_session(message.from_user.id, message.from_user.username, data)

        text = f'<b>Название:</b>\n{data["title"]}\n\n<b>Описание:</b>\n{data["description"][:100]}...'
        markup = await gen_product_kb()

        await message.answer(text=text, reply_markup=markup)
        await state.reset_state()

    else:
        await message.answer('Неверный SKU. попробуйте ещё раз:', reply_markup=cancel_markup)


@dp.callback_query_handler(product_cd.filter(level='0'))
async def show_product_details(callback: CallbackQuery, callback_data: dict):
    field = callback_data.get('field')

    value = await get_value(callback.from_user.id, field)
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

    if field == 'seo_plus':
        text = 'Введите SEO слова через запятую:'
    elif field == 'important':
        text = 'Опишите главные преимущества Вашего товара:'
    else:
        text = 'Введите новые данные:'

    msg = await callback.message.edit_text(text=text, reply_markup=await gen_cancel_kb('product'))
    await callback.answer()

    await state.set_state('change_data')

    async with state.proxy() as data:
        data['field'] = field
        data['prev_message_id'] = msg.message_id


@dp.message_handler(state='change_data')
async def save_new_details(message: Message, state: FSMContext):
    user_id = message.from_user.id

    session = await get_active_session(user_id)
    if not session:
        await add_user_session(user_id, message.from_user.username, {})

    value = message.text

    async with state.proxy() as data:
        field = data['field']
        prev_message_id = data['prev_message_id']

    result = await update_data(user_id, field, value)

    if result:
        await message.delete()
        await dp.bot.edit_message_text(
            text='Данные успешно изменены.',
            chat_id=message.chat.id,
            message_id=prev_message_id,
            reply_markup=await gen_product_kb()
        )
        await state.reset_state()
        return

    await dp.bot.edit_message_text(
        text='Ошибка при добавлении данных. Попробуйте ещё раз:',
        chat_id=message.chat.id,
        message_id=prev_message_id,
        reply_markup=await gen_product_kb()
    )
