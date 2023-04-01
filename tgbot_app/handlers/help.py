# from aiogram.types import CallbackQuery
#
# from tgbot_app.keyboards.inline import gen_help_kb, help_cd
# from tgbot_app.loader import dp
# from tgbot_app.utils.text_variables import HELP_CHATGPT, HELP_PRODUCT
#
#
# @dp.callback_query_handler(help_cd.filter())
# async def help_product(callback: CallbackQuery, callback_data: dict):
#     place = callback_data.get('place')
#     markup = await gen_help_kb(place)
#
#     if place == 'product':
#         text = HELP_PRODUCT
#     else:
#         text = HELP_CHATGPT
#
#     await callback.message.edit_text(text=text, reply_markup=markup, disable_web_page_preview=True)
