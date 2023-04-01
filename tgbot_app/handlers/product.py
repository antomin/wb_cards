from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from tgbot_app.keyboards.inline import (gen_cancel_kb, gen_product_kb,
                                        gen_style_kb, main_menu_cd, product_cd,
                                        scu_cd)
from tgbot_app.loader import dp
from tgbot_app.utils.database import add_user_session
from tgbot_app.utils.text_variables import HELP_PRODUCT, NEW_SKU, STYLE_DESC
from tgbot_app.utils.values_utils import get_value
from tgbot_app.utils.wb_parser import parse_wb


@dp.callback_query_handler(main_menu_cd.filter(action='product'))
async def product(callback: CallbackQuery):
    markup = await gen_product_kb(callback.from_user.id)

    await callback.message.answer(text=HELP_PRODUCT, reply_markup=markup, disable_web_page_preview=True)
    await callback.answer()


@dp.callback_query_handler(scu_cd.filter())
async def sku(callback: CallbackQuery, state: FSMContext):
    markup = await gen_cancel_kb('product')
    await state.set_state('new_scu')

    await callback.message.answer(text=NEW_SKU, reply_markup=markup)
    await callback.answer()


@dp.message_handler(state='new_scu')
async def load_scu(message: Message, state: FSMContext):
    user_id = message.from_user.id
    cancel_markup = await gen_cancel_kb('product')
    _sku = message.text

    if _sku.isdigit():
        msg = await message.answer(text='Загрузка данных...')

        data = await parse_wb(_sku)

        if not data:
            await msg.edit_text(text='Неверный SKU. попробуйте ещё раз:', reply_markup=cancel_markup)
            return

        await add_user_session(user_id, message.from_user.username, data)

        text = f'<b>Название:</b>\n{data["title"]}\n\n<b>Описание:</b>\n{data["description"][:100]}...'
        markup = await gen_product_kb(user_id)

        await msg.edit_text(text=text, reply_markup=markup)

        await state.reset_state()

    else:
        await message.answer('Неверный SKU. попробуйте ещё раз:', reply_markup=cancel_markup)


@dp.callback_query_handler(product_cd.filter())
async def show_product_details(callback: CallbackQuery, state: FSMContext, callback_data: dict):
    field = callback_data.get('field')
    markup = await gen_cancel_kb('product')

    await state.set_state('change_data')
    async with state.proxy() as data:
        data['field'] = field
        data['place'] = 'product'

    value = await get_value(callback.from_user.id, field)

    if field == 'seo_dict':
        text = value + '\n\nВведите SEO слова через запятую:'
    elif field == 'important':
        text = value + '\n\nОпишите главные преимущества Вашего товара:'
    elif field == 'characteristics':
        text = value + '\n\n<b>Раздел на доработке!!!</b>'
    elif field == 'style':
        text = STYLE_DESC
        markup = await gen_style_kb('product')
        await state.reset_state()
    else:
        text = value + '\n\nВведите новые данные:'

    await callback.message.answer(text=text, reply_markup=markup)
    await callback.answer()
