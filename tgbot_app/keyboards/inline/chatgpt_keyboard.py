# from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
#
# from tgbot_app.keyboards.inline.product_keyboard import chatgpt_cd, details_cd
#
#
# async def gen_chatgpt_kb():
#     markup = InlineKeyboardMarkup(row_width=2)
#
#     markup.add(
#         InlineKeyboardButton(text='Назад', callback_data=details_cd.new(field='product_title', level='0',
#                                                                         is_back='True')),
#         InlineKeyboardButton(text='Уточнить', callback_data=chatgpt_cd.new(action='specify')),
#         InlineKeyboardButton(text='Сбросить диалог', callback_data=chatgpt_cd.new(action='reset')),
#     )
#
#     return markup
