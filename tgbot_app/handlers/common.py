from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from tgbot_app.common.text_variables import HELP_PRODUCT
from tgbot_app.keyboards.inline import (cancel_state_cd, gen_chatgpt_kb,
                                        gen_product_kb)
from tgbot_app.loader import dp


@dp.callback_query_handler(cancel_state_cd.filter(), state='*')
async def cancel_changing(callback: CallbackQuery, state: FSMContext, callback_data: dict):
    place = callback_data.get('place')

    if place == 'product':
        markup = await gen_product_kb()
        text = HELP_PRODUCT
    elif place == 'chatgpt':
        markup = await gen_chatgpt_kb()
        text = 'Отменено.'
    else:
        markup = None
        text = 'Отменено.'

    await callback.answer()
    await state.reset_state()
    await callback.message.edit_text(text=text, reply_markup=markup, disable_web_page_preview=True)
