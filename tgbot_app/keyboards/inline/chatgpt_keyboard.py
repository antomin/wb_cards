from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from tgbot_app.keyboards.inline.help_keyboard import help_cd
from tgbot_app.keyboards.inline.start_keyboard import main_menu_cd

chatgpt_cd = CallbackData('chatgpt', 'action')
chatgpt_style_cd = CallbackData('style', 'value')


async def gen_chatgpt_kb(session=True):
    markup = InlineKeyboardMarkup(row_width=1)

    if not session:
        markup.add(
            InlineKeyboardButton(text='Назад', callback_data=main_menu_cd.new(action='main_menu')),
        )

        return markup

    markup.row(
        InlineKeyboardButton(text='Создать описание', callback_data=chatgpt_cd.new(action='make')),
        InlineKeyboardButton(text='Добавить SEO+', callback_data=chatgpt_cd.new(action='make_seo')),
    ).add(
        InlineKeyboardButton(text='Стиль', callback_data=chatgpt_cd.new(action='style')),
        InlineKeyboardButton(text='Сбросить диалог', callback_data=chatgpt_cd.new(action='reset')),
        InlineKeyboardButton(text='Помощь', callback_data=help_cd.new(place='chatgpt')),
        InlineKeyboardButton(text='Назад', callback_data=main_menu_cd.new(action='main_menu')),
    )

    return markup


async def gen_chatgpt_sub_kb():
    markup = InlineKeyboardMarkup(row_width=1)

    markup.add(
        InlineKeyboardButton(text='Улучшить', callback_data=chatgpt_cd.new(action='specify')),
        InlineKeyboardButton(text='Назад', callback_data=main_menu_cd.new(action='chatgpt')),
    )

    return markup


async def gen_chatgpt_style_kb():
    markup = InlineKeyboardMarkup(row_width=1)

    markup.add(
        InlineKeyboardButton(text='Обычный', callback_data=chatgpt_style_cd.new(value='обычный')),
        InlineKeyboardButton(text='Творческий', callback_data=chatgpt_style_cd.new(value='творческий')),
        InlineKeyboardButton(text='Формальный', callback_data=chatgpt_style_cd.new(value='формальный')),
    )

    return markup
