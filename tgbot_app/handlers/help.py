from aiogram.types import CallbackQuery, Message

from tgbot_app.common.text_variables import HELP_PRODUCT
from tgbot_app.keyboards.inline import gen_help_kb, help_cd
from tgbot_app.loader import dp


@dp.callback_query_handler(help_cd.filter(place='product'))
async def help_product(callback: CallbackQuery, callback_data: dict):
    markup = await gen_help_kb(callback_data.get('place'))
    await callback.message.edit_text(text=HELP_PRODUCT, reply_markup=markup, disable_web_page_preview=True)


# @dp.message_handler(commands=['help'])
# async def product_handler(message: Message):
#     await message.answer('Помощь ла-ла-ла!!!')
