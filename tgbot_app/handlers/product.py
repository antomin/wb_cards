from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from tgbot_app.keyboards.inline import (gen_cancel_kb, gen_product_kb,
                                        main_menu_cd, product_cd, scu_cd)
from tgbot_app.loader import dp
from tgbot_app.utils.database import add_user_session, get_active_session
from tgbot_app.utils.text_variables import HELP_PRODUCT, NEW_SKU
from tgbot_app.utils.values_utils import get_value, update_data
from tgbot_app.utils.wb_parser import parse_wb


@dp.callback_query_handler(main_menu_cd.filter(action='product'))
async def product(callback: CallbackQuery):
    markup = await gen_product_kb()

    await callback.message.edit_text(text=HELP_PRODUCT, reply_markup=markup, disable_web_page_preview=True)


@dp.callback_query_handler(scu_cd.filter())
async def sku(callback: CallbackQuery, state: FSMContext):
    markup = await gen_cancel_kb('product')
    await state.set_state('new_scu')
    await callback.answer()
    msg = await callback.message.edit_text(text=NEW_SKU, reply_markup=markup)

    async with state.proxy() as data:
        data['prev_message_id'] = msg.message_id


@dp.message_handler(state='new_scu')
async def load_scu(message: Message, state: FSMContext):
    cancel_markup = await gen_cancel_kb('product')
    _sku = message.text

    await message.delete()

    async with state.proxy() as data:
        prev_message_id = data['prev_message_id']

    if _sku.isdigit():
        await dp.bot.edit_message_text(
            text='Загрузка данных...',
            chat_id=message.chat.id,
            message_id=prev_message_id,
        )

        data = await parse_wb(_sku)

        if not data:
            await dp.bot.edit_message_text(
                text='Неверный SKU. попробуйте ещё раз:',
                chat_id=message.chat.id,
                message_id=prev_message_id,
                reply_markup=cancel_markup
            )
            return

        await add_user_session(message.from_user.id, message.from_user.username, data)

        text = f'<b>Название:</b>\n{data["title"]}\n\n<b>Описание:</b>\n{data["description"][:100]}...'
        markup = await gen_product_kb()

        await dp.bot.edit_message_text(
            text=text,
            chat_id=message.chat.id,
            message_id=prev_message_id,
            reply_markup=markup
        )

        await state.reset_state()

    else:
        await message.answer('Неверный SKU. попробуйте ещё раз:', reply_markup=cancel_markup)


@dp.callback_query_handler(product_cd.filter())
async def show_product_details(callback: CallbackQuery, state: FSMContext, callback_data: dict):
    field = callback_data.get('field')

    value = await get_value(callback.from_user.id, field)

    if field == 'seo_plus':
        text = value + '\n\nВведите SEO слова через запятую:'
    elif field == 'important':
        text = value + '\n\nОпишите главные преимущества Вашего товара:'
    elif field == 'seo_dict':
        text = 'Раздел на доработке.'
    elif field == 'characteristics':
        text = value + '\n\nРаздел на доработке.'
    else:
        text = value + '\n\nВведите новые данные:'

    markup = await gen_cancel_kb('product')

    msg = await callback.message.edit_text(text=text, reply_markup=markup)

    await state.set_state('change_data')

    async with state.proxy() as data:
        data['field'] = field
        data['place'] = 'product'


# @dp.message_handler(state='change_data')
# async def save_new_details(message: Message, state: FSMContext):
#     user_id = message.from_user.id
#     markup = await gen_product_kb()
#
#     session = await get_active_session(user_id)
#     if not session:
#         await add_user_session(user_id, message.from_user.username, {})
#
#     value = message.text
#
#     async with state.proxy() as data:
#         field = data['field']
#         prev_message_id = data['prev_message_id']
#
#     if field not in ('characteristics', 'seo_dict'):
#         result = await update_data(user_id, field, value)
#     else:
#         result = True
#
#     if result:
#         text = 'Данные успешно изменены.' if field not in ('characteristics', 'seo_dict') else 'Раздел на доработке.'
#         await message.delete()
#
#         await dp.bot.edit_message_text(
#             text=text,
#             chat_id=message.chat.id,
#             message_id=prev_message_id,
#             reply_markup=markup
#         )
#         await state.reset_state()
#         return
#
#     await dp.bot.edit_message_text(
#         text='Ошибка при добавлении данных. Попробуйте ещё раз:',
#         chat_id=message.chat.id,
#         message_id=prev_message_id,
#         reply_markup=markup
#     )
