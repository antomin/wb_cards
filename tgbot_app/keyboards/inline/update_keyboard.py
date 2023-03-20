# from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
# from aiogram.utils.callback_data import CallbackData
#
# from tgbot_app.keyboards.inline.product_keyboard import details_cd
#
# update_cd = CallbackData('update')
#
#
# async def gen_update_kb():
#     markup = InlineKeyboardMarkup(row_width=2)
#
#     markup.add(
#         InlineKeyboardButton(
#             text='Назад',
#             callback_data=details_cd.new(field='product_title', level='0', is_back='True')
#         ),
#         InlineKeyboardButton(
#             text='Да',
#             callback_data=update_cd.new()
#         )
#     )
#
#     return markup
