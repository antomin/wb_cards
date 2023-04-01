from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from tgbot_app.keyboards.inline.creation_keyboard import (chatgpt_cd,
                                                          creation_cd)
from tgbot_app.keyboards.inline.start_keyboard import main_menu_cd


async def gen_chatgpt_kb(place):
    markup = InlineKeyboardMarkup(row_width=1)
    callback_data = creation_cd.new(field='next', level=2) if place == 'creation_next' else '0'
    markup.add(
        InlineKeyboardButton(text='Улучшить', callback_data=chatgpt_cd.new(action='specify', place=place)),
        InlineKeyboardButton(text='Назад', callback_data=callback_data),
    )

    # markup = InlineKeyboardMarkup(row_width=1)
    #
    # if not session:
    #     markup.add(
    #         InlineKeyboardButton(text='Назад', callback_data=main_menu_cd.new(action='main_menu')),
    #     )
    #
    #     return markup
    #
    # markup.row(
    #     InlineKeyboardButton(text='Создать описание', callback_data=chatgpt_cd.new(action='make')),
    #     InlineKeyboardButton(text='Добавить SEO+', callback_data=chatgpt_cd.new(action='make_seo')),
    # ).add(
    #     InlineKeyboardButton(text='Стиль', callback_data=chatgpt_cd.new(action='style')),
    #     InlineKeyboardButton(text='Сбросить диалог', callback_data=chatgpt_cd.new(action='reset')),
    #     InlineKeyboardButton(text='Помощь', callback_data=help_cd.new(place='chatgpt')),
    #     InlineKeyboardButton(text='Назад', callback_data=main_menu_cd.new(action='main_menu')),
    # )

    return markup


# async def gen_chatgpt_sub_kb():
#     markup = InlineKeyboardMarkup(row_width=1)
#
#     markup.add(
#         InlineKeyboardButton(text='Улучшить', callback_data=chatgpt_cd.new(action='specify')),
#         InlineKeyboardButton(text='Назад', callback_data=main_menu_cd.new(action='chatgpt')),
#     )
#
#     return markup

