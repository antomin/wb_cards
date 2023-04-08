from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from django.conf import settings

from tgbot_app.keyboards.inline import (creation_cd, gen_cancel_kb,
                                        gen_creation_kb, gen_creation_next_kb,
                                        gen_style_kb, main_menu_cd)
from tgbot_app.loader import dp
from tgbot_app.utils.database import fetch_data, get_active_session
from tgbot_app.utils.seo_utils import get_seo_dictionary, get_word_frequencies
from tgbot_app.utils.text_variables import CREATION_MSG, STYLE_DESC
from tgbot_app.utils.values_utils import get_raw_text, get_value, update_data


@dp.callback_query_handler(main_menu_cd.filter(action='creation'))
async def start_creation(callback: CallbackQuery):
    markup = await gen_creation_kb()

    await callback.message.answer(text=CREATION_MSG, reply_markup=markup, disable_web_page_preview=True)
    await callback.answer()


@dp.callback_query_handler(main_menu_cd.filter(action='creation_next'))
async def next_creation(callback: CallbackQuery):
    user_id = callback.from_user.id
    session = await get_active_session(user_id)

    if not session or not session.title or not session.important:
        text = 'Не хватает данных о товаре. Вернитесь назад и внесите обязательные поля: ' \
               '<b>Наименование</b> и <b>Главное о товаре</b>.'
        markup = await gen_creation_next_kb(session=False)
    else:
        text = f'<b>{session.title}</b>\n\n<b>Главное о товаре:</b>\n{session.important}'
        if session.sku_plus:
            text += f'\n\n<b>Дополнительные SKU:</b>\n{session.sku_plus}.'
        markup = await gen_creation_next_kb()

        if session.is_updated:
            msg = await callback.message.answer('Загрузка данных c WB...')

            raw_text = session.title + ' ' + session.important

            if session.sku_plus:
                scu_list = session.sku_plus.split(', ')
                raw_text += ' ' + await get_raw_text(scu_list)

            await msg.edit_text('Данные с WB загружены.\nАнализируем ключевые слова...')

            word_frequencies = await get_word_frequencies(raw_text)

            msg = await msg.edit_text('Данные с WB загружены.\nКлючевые слова собраны.\nВыбираем SEO-фразы...')

            seo_phrases = await fetch_data(word_frequencies)
            await update_data(
                user_id,
                'seo_phrases', ', '.join([item.phrase async for item in seo_phrases[:settings.SEO_PHRASES_LIMIT]])
            )

            await msg.edit_text('Данные с WB загружены.\nКлючевые слова собраны.\nSEO-фразы выбраны.\n'
                                'Составляем Ваш SEO-словарь...')

            seo_dict = await get_seo_dictionary(seo_phrases, limit=settings.SEO_DICT_LIMIT)
            await update_data(user_id, 'seo_dict', ', '.join(seo_dict))

            await msg.edit_text(text='Данные с WB загружены.\nКлючевые слова собраны.\nSEO-фразы выбраны.\n'
                                'Ваш SEO-словарь составлен.')

            await update_data(user_id, 'is_updated', False)

    await callback.message.answer(text=text, reply_markup=markup)
    await callback.answer()


@dp.callback_query_handler(creation_cd.filter())
async def load_fields(callback: CallbackQuery, state: FSMContext, callback_data: dict):
    field = callback_data.get('field')
    if field in ('seo_dict', 'seo_phrases', 'minus_words', 'style'):
        place = 'creation_next'
    else:
        place = 'creation'
    markup = await gen_cancel_kb(place)

    await state.set_state('change_data')
    async with state.proxy() as data:
        data['field'] = field
        data['place'] = place

    value = await get_value(callback.from_user.id, field)

    if field == 'important':
        text = value + '\n\nКратко опишите ключевые особенности товара:'
    elif field == 'title':
        text = value + '\n\nНапишите наименование товара:'
    elif field == 'sku_plus':
        text = value + '\n\nВведите через запятую до 5 SCU карточек с хорошим описанием:'
    elif field == 'style':
        text = STYLE_DESC
        markup = await gen_style_kb('creation')
        await state.reset_state()
    else:
        text = value + '\n\nДанные генерируются на основе введённой информации. Но вы можете их изменить:'

    await callback.message.answer(text=text, reply_markup=markup)
    await callback.answer()


