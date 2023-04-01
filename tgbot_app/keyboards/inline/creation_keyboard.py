from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from tgbot_app.keyboards.inline.start_keyboard import main_menu_cd

creation_cd = CallbackData('creation', 'field', 'level')
chatgpt_cd = CallbackData('chatgpt', 'action', 'place')


async def gen_creation_kb():
    markup = InlineKeyboardMarkup(row_width=2)

    markup.row(InlineKeyboardButton(text='Название', callback_data=creation_cd.new(field='title', level=1)))
    markup.row(InlineKeyboardButton(text='Главное в товаре', callback_data=creation_cd.new(field='important', level=1)))
    markup.row(InlineKeyboardButton(text='SKU +', callback_data=creation_cd.new(field='sku_plus', level=1)))
    markup.row(InlineKeyboardButton(text='SEO +', callback_data=creation_cd.new(field='seo_dict', level=1)))
    markup.row(
        InlineKeyboardButton(text='Назад', callback_data=main_menu_cd.new(action='main_menu')),
        InlineKeyboardButton(text='Дальше', callback_data=creation_cd.new(field='next', level=2)),
    )

    return markup


async def gen_creation_next_kb(session=True):
    markup = InlineKeyboardMarkup(row_width=1)

    if not session:
        markup.add(InlineKeyboardButton(text='Назад', callback_data=main_menu_cd.new(action='creation')))
        return markup

    markup.add(
        InlineKeyboardButton(text='Ключевые фразы', callback_data=creation_cd.new(field='seo_phrases', level=1)),
        InlineKeyboardButton(text='Ключевые слова', callback_data=creation_cd.new(field='keywords', level=1)),
        InlineKeyboardButton(text='Минус слова', callback_data=creation_cd.new(field='minus_words', level=1)),
        InlineKeyboardButton(text='Стиль', callback_data=creation_cd.new(field='style', level=1)),
        InlineKeyboardButton(text='GPT Магия', callback_data=chatgpt_cd.new(action='make', place='creation_next')),
        InlineKeyboardButton(text='Сбросить диалог',
                             callback_data=chatgpt_cd.new(action='reset', place='creation_next')),
        InlineKeyboardButton(text='Назад', callback_data=main_menu_cd.new(action='creation')),
    )

    return markup
