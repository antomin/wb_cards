from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from tgbot_app.common.database import add_user_session
from tgbot_app.common.text_variables import NEW_SKU
from tgbot_app.common.wb_parser import parse_wb
from tgbot_app.keyboards.inline.product_keyboard import (gen_product_keyboard,
                                                         product_cd)
from tgbot_app.loader import dp


@dp.message_handler(lambda message: 'Товар' in message.text)
async def product_handler(message: Message):
    keyboard = await gen_product_keyboard(message.from_user.id)
    await message.delete()
    await message.answer('Товар', reply_markup=keyboard)


@dp.callback_query_handler(product_cd.filter(is_new='True'))
async def product_handler(callback: CallbackQuery, state: FSMContext, callback_data: dict):
    # is_new = bool(callback_data.get('is_new'))
    # text = 'Нет загруженных товаров' if is_new else 'Ваш товар'
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
        await message.answer('Неверный SKU. попробуйте ущё раз:')
